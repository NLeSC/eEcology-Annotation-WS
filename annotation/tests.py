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
from annotation.uploads import UploadViews
from pyramid.httpexceptions import HTTPFound


class ConnectTests(unittest.TestCase):
    pass


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        request = testing.DummyRequest()
        response = views.home(request)
        self.assertEqual(response, {})

    def test_trackers(self):
        request = testing.DummyRequest()
        cursor = UserList([{'id': 355}])
        cursor.execute = Mock()
        request.db = Mock()
        request.db.cursor.return_value = cursor

        response = views.trackers(request)

        expected = {'trackers': [{'id': 355}]}
        self.assertEquals(response, expected)
        expected_sql = """
        SELECT DISTINCT device_info_serial as id
        FROM gps.ee_tracker_limited
        JOIN gps.ee_track_session_limited USING (device_info_serial)
        ORDER BY device_info_serial
    """
        cursor.execute.assert_called_with(expected_sql)

    def test_tracker(self):
        request = testing.DummyRequest()
        request.db = Mock()
        cursor = Mock()
        request.db.cursor.return_value = cursor
        request.matchdict = {'id': '355',
                             'start': '2010-06-28T00:00:00Z',
                             'end': '2010-06-29T00:00:00Z'}

        views.tracker(request)

        binds = (20.0,
                 355,
                 '2010-06-28T00:00:00+00:00',
                 '2010-06-29T00:00:00+00:00',
                 355,
                 '2010-06-28T00:00:00+00:00',
                 '2010-06-29T00:00:00+00:00')
        cursor.execute.assert_called_with(ANY, binds)


class AnnotationTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()

    def tearDown(self):
        testing.tearDown()

    def test_datetime_adaptor(self):
        obj = datetime(2010, 6, 28, 0, 0, 0, 0, UTC)
        result = annotation.datetime_adaptor(obj, self.request)
        self.assertEquals(result, '2010-06-28T00:00:00+00:00')

    def test_timedelta_adaptor(self):
        obj = timedelta(seconds=65)
        result = annotation.timedelta_adaptor(obj, self.request)
        self.assertEquals(result, '0:01:05')

    def test_decimal_adaptor(self):
        obj = Decimal('0.1234')
        result = annotation.decimal_adaptor(obj, self.request)
        self.assertEquals(result, 0.1234)

    def test_cursor_adaptor(self):
        obj = (1, 2, 3)
        result = annotation.cursor_adaptor(obj, self.request)
        self.assertEquals(result, [1, 2, 3])


class UploadViewsTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()
        self.request.db = Mock()
        self.cursor = Mock()
        self.request.db.cursor.return_value = self.cursor

    def tearDown(self):
        testing.tearDown()

    def test_constructor_nourlparameters_tableIsEmpty(self):
        views = UploadViews(self.request)

        self.assertEquals(views.table, '')

    def test_constructor_url_parameters_trackerAndTableFilled(self):
        self.request.matchdict['table'] = 'mytable'

        views = UploadViews(self.request)

        self.assertEquals(views.table, 'mytable')

    def test_uploads_notableselected(self):
        views = UploadViews(self.request)

        response = views.uploads()

        expected_response = {'trackers': [], 'table': ''}
        self.assertEqual(response, expected_response)

    def test_uploads_selectedtable_listsoftrackers(self):
        self.request.params['table'] = 'mytable'
        views = UploadViews(self.request)
        rows = [{
                 'id': 355,
                 'start': datetime(2010, 6, 28, 0, 0, 0, 0, UTC),
                 'end': datetime(2010, 6, 28, 12, 0, 0, 0, UTC),
                 'count:': 1,
                 }]
        self.cursor.fetchall.return_value = rows
        self.cursor.fetchone.return_value = {'date_time': datetime(2010, 6, 28, 10, 0, 0, 0, UTC), 'count': 1}

        response = views.uploads()

        expected = {'table': 'mytable',
                    'trackers': [{'count:': 1,
                                  'end': datetime(2010, 6, 28, 12, 0, 0, 0, UTC),
                                  'first_page': datetime(2010, 6, 28, 10, 0, 0, 0, UTC),
                                  'id': 355,
                                  'last_page': datetime(2010, 6, 28, 10, 0, 0, 0, UTC),
                                  'page_size': 500,
                                  'size': 1,
                                  'start': datetime(2010, 6, 28, 0, 0, 0, 0, UTC)
                                  }]
                    }
        self.assertEqual(response, expected)

    def test_uploads_windowtoosmall_listsoftrackers(self):
        self.request.params['table'] = 'mytable'
        views = UploadViews(self.request)
        rows = [{
                 'id': 355,
                 'start': datetime(2010, 6, 28, 0, 0, 0, 0, UTC),
                 'end': datetime(2010, 6, 28, 12, 0, 0, 0, UTC),
                 'count:': 1,
                 }]
        self.cursor.fetchall.return_value = rows
        views.track_size = Mock(return_value=1)
        self.cursor.fetchone.return_value = None

        response = views.uploads()

        expected = {'table': 'mytable',
                    'trackers': [{'count:': 1,
                                  'end': datetime(2010, 6, 28, 12, 0, 0, 0, UTC),
                                  'first_page': datetime(2010, 6, 28, 12, 0, 0, 0, UTC),
                                  'id': 355,
                                  'last_page': datetime(2010, 6, 28, 0, 0, 0, 0, UTC),
                                  'page_size': 500,
                                  'size': 1,
                                  'start': datetime(2010, 6, 28, 0, 0, 0, 0, UTC)
                                  }]
                    }
        self.assertEqual(response, expected)


    def test_upload(self):
        self.request.matchdict['table'] = 'mytable'
        self.request.params['id'] = '355'
        self.request.params['start'] = '2010-06-27T00:00:00+00:00'
        self.request.params['end'] = '2010-06-29T00:00:00+00:00'
        self.config.add_route('annotations.csv', '/uploads/{table}/annotations.csv')
        views = UploadViews(self.request)
        rows = [{
                 'id': 3,
                 'label': 'flying',
                 'color': 'rgb(0,0,255)',
                 }]
        self.cursor.fetchall.return_value = rows

        response = views.upload()

        expected_response = {'annotations_url': '/uploads/mytable/annotations.csv',
                             'classes': '[{"color": "rgb(0,0,255)", "id": 3, "label": "flying"}]',
                             'end': '2010-06-29T00:00:00+00:00',
                             'start': '2010-06-27T00:00:00+00:00',
                             'tracker_id': 355,
                             }
        self.assertEqual(response, expected_response)

    def test_upload_withoutselection(self):
        self.request.matchdict['table'] = 'mytable'
        self.config.add_route('uploads.html', '/uploads.html')
        views = UploadViews(self.request)

        response = views.upload()

        expected_response = HTTPFound('/uploads.html?table=mytable')
        self.assertIsInstance(response, HTTPFound)
        self.assertEqual(response.location, expected_response.location)

    def test_annotations_as_csv(self):
        self.request.matchdict['table'] = 'mytable'
        self.request.params['id'] = '355'
        self.request.params['start'] = '2010-06-27T00:00:00+00:00'
        self.request.params['end'] = '2010-06-29T00:00:00+00:00'
        views = UploadViews(self.request)
        rows = [{
                 'device_info_serial': 355,
                 'date_time': datetime(2010, 6, 28, 0, 0, 0, 0, UTC),
                 'class_id': 3
                 }]
        self.cursor.fetchall.return_value = rows

        response = views.annotations_as_csv()

        expected_body = 'device_info_serial,date_time,class_id\n355,2010-06-28T00:00:00+00:00Z,3\n'
        self.assertEqual(response.body, expected_body)
