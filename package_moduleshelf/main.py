# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

import firestore
from flask import current_app, flash, Flask, Markup, redirect, render_template
from flask import request, url_for
from google.cloud import error_reporting
import google.cloud.logging
import storage

import Flask-RESTful

from flask_restful_swagger import swagger

import pandas as pd
import ast

import Packages
import Reset
import Package
import PackageRating
import Authenticate

# [START upload_image_file]
def upload_image_file(img):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not img:
        return None

    public_url = storage.upload_file(
        img.read(),
        img.filename,
        img.content_type
    )

    current_app.logger.info(
        'Uploaded file %s as %s.', img.filename, public_url)

    return public_url
# [END upload_image_file]


app = Flask(__name__)
app.config.update(
    SECRET_KEY='secret',
    MAX_CONTENT_LENGTH=1000000,
    ALLOWED_EXTENSIONS=set(['zip']),
    CLOUD_STORAGE_BUCKET = 'ece461-p2-t3-files'
)

app.debug = False
app.testing = False

api = swagger.docs(Api(app), apiVersion='1.0')
api.add_resource(Packages, '/packages')
api.add_resource(Reset, '/reset')
api.add_resource(Packages.get_package_by_ID(id), '/package/{id}')
api.add_resource(Package, '/package')
api.add_resource(PackageRating.rate_by_ID(id), '/package/{id}/rate')
api.add_resource(Authenticate, '/authenticate')
api.add_resource(Packages.get_package_by_Name(Name), '/package/byName/{Name}')
api.add_resource(Packages.delete_package_by_Name(Name), '/package/byName/{Name}')

# Configure logging
if not app.testing:
    logging.basicConfig(level=logging.INFO)
    client = google.cloud.logging.Client()
    # Attaches a Google Stackdriver logging handler to the root logger
    client.setup_logging()


@app.route('/')
def list():
    start_after = request.args.get('start_after', default=1)
    package_modules, last_name = firestore.next_page(start_after=start_after)

    return render_template('list.html', package_modules=package_modules, last_name=last_name)


@app.route('/package_modules/<package_module_id>')
def view(package_module_id):
    package_module = firestore.read(package_module_id)
    return render_template('view.html', package_module=package_module)


@app.route('/package_modules/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
        image_url = upload_image_file(request.files.get('image'))

        if image_url:
            data['imageUrl'] = image_url

        package_module = firestore.create(data)

        return redirect(url_for('.view', package_module_id=package_module['id']))

    return render_template('form.html', action='Add', package_module={})


@app.route('/package_modules/<package_module_id>/edit', methods=['GET', 'POST'])
def edit(package_module_id):
    package_module = firestore.read(package_module_id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
        image_url = upload_image_file(request.files.get('image'))

        if image_url:
            data['imageUrl'] = image_url

        package_module = firestore.update(data, package_module_id)

        return redirect(url_for('.view', package_module_id=package_module['id']))

    return render_template('form.html', action='Edit', package_module=package_module)


@app.route('/package_modules/<package_module_id>/delete')
def delete(package_module_id):
    firestore.delete(package_module_id)
    return redirect(url_for('.list'))


@app.route('/logs')
def logs():
    logging.info('Hey, you triggered a custom log entry. Good job!')
    flash(Markup('''You triggered a custom log entry. You can view it in the
        <a href="https://console.cloud.google.com/logs">Cloud Console</a>'''))
    return redirect(url_for('.list'))


@app.route('/errors')
def errors():
    raise Exception('This is an intentional exception.')


# Add an error handler that reports exceptions to Stackdriver Error
# Reporting. Note that this error handler is only used when debug
# is False
@app.errorhandler(500)
def server_error(e):
    client = error_reporting.Client()
    client.report_exception(
        http_context=error_reporting.build_flask_context(request))
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
