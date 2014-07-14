# Copyright 2013 Netherlands eScience Center
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from UserList import UserList
from datetime import datetime, timedelta
from decimal import Decimal
import unittest
from iso8601.iso8601 import UTC
from mock import Mock, ANY
from pyramid import testing
import annotation.views as views
import annotation
from annotation.uploads import Upload

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_trackers(self):
        request = testing.DummyRequest()
        request.user = 'me'
        cursor = UserList([{'id': 355}])
        cursor.execute = Mock()
        request.db = Mock()
        request.db.cursor.return_value = cursor

        response = views.trackers(request)

        expected = {'trackers': [{'id': 355}]}
        self.assertEquals(response, expected)
        expected_sql = """
        SELECT device_info_serial as id
        FROM gps.uva_device
        JOIN gps.uva_access_device USING (device_info_serial)
        WHERE username=%s
        ORDER BY device_info_serial
    """
        cursor.execute.assert_called_with(expected_sql, ('me',))

    def test_tracker(self):
        request = testing.DummyRequest()
        request.user = 'me'
        request.db = Mock()
        cursor = Mock()
        request.db.cursor.return_value = cursor
        request.matchdict = {'id': '355', 'start': '2010-06-28T00:00:00Z', 'end': '2010-06-29T00:00:00Z'}

        views.tracker(request)

        binds = (20.0, 355, '2010-06-28T00:00:00+00:00', '2010-06-29T00:00:00+00:00', 355, '2010-06-28T00:00:00+00:00', '2010-06-29T00:00:00+00:00', 'me')
        cursor.execute.assert_called_with(ANY, binds)

class AnnotationTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()

    def tearDown(self):
        testing.tearDown()

    def test_datetime_adaptor(self):
        obj = datetime(2010, 6, 28, 0, 0, 0, 0, UTC)
        self.assertEquals(annotation.datetime_adaptor(obj, self.request), '2010-06-28T00:00:00+00:00')

    def test_timedelta_adaptor(self):
        obj = timedelta(seconds=65)
        self.assertEquals(annotation.timedelta_adaptor(obj, self.request), '0:01:05')

    def test_decimal_adaptor(self):
        obj = Decimal('0.1234')
        self.assertEquals(annotation.decimal_adaptor(obj, self.request), 0.1234)

    def test_cursor_adaptor(self):
        obj = (1, 2, 3)
        self.assertEquals(annotation.cursor_adaptor(obj, self.request), [1, 2, 3])

class UploadsTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()
        self.request.db = Mock()

    def tearDown(self):
        testing.tearDown()

    def test_constructor_nourlparameters_trackerIsEmpty(self):
        upload = Upload(self.request)

        self.assertEquals(upload.tracker_id, 0)

    def test_constructor_nourlparameters_tableIsEmpty(self):
        upload = Upload(self.request)

        self.assertEquals(upload.table, '')

    def test_constructor_url_parameters_trackerAndTableFilled(self):
        self.request.matchdict['table'] = 'mytable'
        self.request.matchdict['tracker'] = 1234

        upload = Upload(self.request)

        self.assertEquals(upload.table, 'mytable')
        self.assertEquals(upload.tracker_id, 1234)

    def test_upload_html(self):
        upload = Upload(self.request)

        response = upload.upload_html()

        expected_response = {'tracker_id': 0, 'table': ''}
        self.assertEqual(response, expected_response)
