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

import re

from conftest import flaky_filter
from flaky import flaky
import pytest


# Mark all test cases in this class as flaky, so that if errors occur they
# can be retried. This is useful when databases are temporarily unavailable.
@flaky(rerun_filter=flaky_filter)
# Tell pytest to use both the app and model fixtures for all test cases.
# This ensures that configuration is properly applied and that all database
# resources created during tests are cleaned up. These fixtures are defined
# in conftest.py
@pytest.mark.usefixtures('app', 'model')
class TestCrudActions(object):

    def test_list(self, app, model):
        for i in range(1, 12):
            model.create({'name': u'package_module {0}'.format(i)})

        with app.test_client() as c:
            rv = c.get('/package_modules/')

        assert rv.status == '200 OK'

        body = rv.data.decode('utf-8')
        assert 'package_module 1' in body, "Should show package_modules"
        assert len(re.findall('<h4>package_module', body)) == 10, (
            "Should not show more than 10 package_modules")
        assert 'More' in body, "Should have more than one page"

    def test_add(self, app):
        data = {
            'name': 'Test package_module',
            'user': 'Test user',
            'publishedDate': 'Test Date Published',
            'description': 'Test Description'
        }

        with app.test_client() as c:
            rv = c.post('/package_modules/add', data=data, follow_redirects=True)

        assert rv.status == '200 OK'
        body = rv.data.decode('utf-8')
        assert 'Test package_module' in body
        assert 'Test user' in body
        assert 'Test Date Published' in body
        assert 'Test Description' in body

    def test_edit(self, app, model):
        existing = model.create({'name': "Temp name"})

        with app.test_client() as c:
            rv = c.post(
                '/package_modules/%s/edit' % existing['id'],
                data={'name': 'Updated name'},
                follow_redirects=True)

        assert rv.status == '200 OK'
        body = rv.data.decode('utf-8')
        assert 'Updated name' in body
        assert 'Temp name' not in body

    def test_delete(self, app, model):
        existing = model.create({'name': "Temp name"})

        with app.test_client() as c:
            rv = c.get(
                '/package_modules/%s/delete' % existing['id'],
                follow_redirects=True)

        assert rv.status == '200 OK'
        assert not model.read(existing['id'])
