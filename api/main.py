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
import google.cloud.logging
import storage

import Flask-RESTful
from flask_restful_swagger import swagger

import Packages
import Reset
import Package
import PackageRating
import Authenticate


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
    client = google.cloud.logging.Client(project='ece461-p2-t3')
    # Attaches a Google Stackdriver logging handler to the root logger
    client.setup_logging()
