# Copyright 2015 Google Inc.
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

from package_moduleshelf import get_model, oauth2, storage, tasks
from flask import Blueprint, current_app, redirect, render_template, request, \
    session, url_for


crud = Blueprint('crud', __name__)


def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url


@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    package_modules, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        package_modules=package_modules,
        next_page_token=next_page_token)


@crud.route("/mine")
@oauth2.required
def list_mine():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    package_modules, next_page_token = get_model().list_by_user(
        user_id=session['profile']['id'],
        cursor=token)

    return render_template(
        "list.html",
        package_modules=package_modules,
        next_page_token=next_page_token)


@crud.route('/<id>')
def view(id):
    package_module = get_model().read(id)
    return render_template("view.html", package_module=package_module)


@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
        image_url = upload_image_file(request.files.get('image'))

        if image_url:
            data['imageUrl'] = image_url

        # If the user is logged in, associate their profile with the new package_module.
        if 'profile' in session:
            data['createdBy'] = session['profile']['name']
            data['createdById'] = session['profile']['email']

        package_module = get_model().create(data)

        q = tasks.get_package_modules_queue()
        q.enqueue(tasks.process_package_module, package_module['id'])

        return redirect(url_for('.view', id=package_module['id']))

    return render_template("form.html", action="Add", package_module={})


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    package_module = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        image_url = upload_image_file(request.files.get('image'))

        if image_url:
            data['imageUrl'] = image_url

        package_module = get_model().update(data, id)

        q = tasks.get_package_modules_queue()
        q.enqueue(tasks.process_package_module, package_module['id'])

        return redirect(url_for('.view', id=package_module['id']))

    return render_template("form.html", action="Edit", package_module=package_module)


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
