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

import os
import re

import google.auth
import main
import pytest
import requests
from six import BytesIO


credentials, project_id = google.auth.default()
os.environ['GOOGLE_CLOUD_PROJECT'] = project_id


@pytest.yield_fixture
def app(request):
    """This fixture provides a Flask app instance configured for testing.

    It also ensures the tests run within a request context, allowing
    any calls to flask.request, flask.current_app, etc. to work."""
    app = main.app

    with app.test_request_context():
        yield app


@pytest.yield_fixture
def firestore():

    import firestore
    """This fixture provides a modified version of the app's Firebase model that
    tracks all created items and deletes them at the end of the test.

    Any tests that directly or indirectly interact with the database should use
    this to ensure that resources are properly cleaned up.
    """

    # Ensure no package_modules exist before running the tests. This typically helps if
    # tests somehow left the database in a bad state.
    delete_all_package_modules(firestore)

    yield firestore

    # Delete all package_modules that we created during tests.
    delete_all_package_modules(firestore)


def delete_all_package_modules(firestore):
    while True:
        package_modules, _ = firestore.next_page(limit=50)
        if not package_modules:
            break
        for package_module in package_modules:
            firestore.delete(package_module['id'])


def test_list(app, firestore):
    for i in range(1, 12):
        firestore.create({'name': u'package_module {0}'.format(i)})

    with app.test_client() as c:
        rv = c.get('/')

    assert rv.status == '200 OK'

    body = rv.data.decode('utf-8')
    assert 'package_module 1' in body, "Should show package_modules"
    assert len(re.findall('<h4>package_module', body)) <= 10, (
        "Should not show more than 10 package_modules")
    assert 'More' in body, "Should have more than one page"


def test_add(app):
    data = {
        'name': 'Test package_module',
        'user': 'Test user',
        'publishedDate': 'Test Date Published',
        'description': 'Test Description'
    }

    with app.test_client() as c:
        rv = c.post('package_modules/add', data=data, follow_redirects=True)

    assert rv.status == '200 OK'
    body = rv.data.decode('utf-8')
    assert 'Test package_module' in body
    assert 'Test user' in body
    assert 'Test Date Published' in body
    assert 'Test Description' in body


def test_edit(app, firestore):
    existing = firestore.create({'name': "Temp name"})

    with app.test_client() as c:
        rv = c.post(
            'package_modules/%s/edit' % existing['id'],
            data={'name': 'Updated name'},
            follow_redirects=True)

    assert rv.status == '200 OK'
    body = rv.data.decode('utf-8')
    assert 'Updated name' in body
    assert 'Temp name' not in body


def test_delete(app, firestore):
    existing = firestore.create({'name': "Temp name"})

    with app.test_client() as c:
        rv = c.get(
            'package_modules/%s/delete' % existing['id'],
            follow_redirects=True)

    assert rv.status == '200 OK'
    assert not firestore.read(existing['id'])


def test_upload_image(app):
    data = {
        'name': 'Test package_module',
        'user': 'Test user',
        'publishedDate': 'Test Date Published',
        'description': 'Test Description',
        'image': (BytesIO(b'hello world'), 'hello.jpg')
    }

    with app.test_client() as c:
        rv = c.post('package_modules/add', data=data, follow_redirects=True)

    assert rv.status == '200 OK'
    body = rv.data.decode('utf-8')

    img_tag = re.search('<img.*?src="(.*)"', body).group(1)

    r = requests.get(img_tag)
    assert r.status_code == 200
    assert r.text == 'hello world'


def test_upload_bad_file(app):
    data = {
        'name': 'Test package_module',
        'user': 'Test user',
        'publishedDate': 'Test Date Published',
        'description': 'Test Description',
        'image': (BytesIO(b'<?php phpinfo(); ?>'),
                  '1337h4x0r.php')
    }

    with app.test_client() as c:
        rv = c.post('/package_modules/add', data=data, follow_redirects=True)

    # check we weren't pwned
    assert rv.status == '400 BAD REQUEST'
