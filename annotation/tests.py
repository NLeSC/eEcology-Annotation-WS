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

from datetime import datetime
import unittest
from UserList import UserList
from mock import Mock
from pyramid import testing
import annotation.views as views


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
        expected_sql = 'SELECT device_info_serial as id '
        expected_sql += 'FROM gps.uva_device '
        expected_sql += 'JOIN uva_access_device USING (device_info_serial) '
        expected_sql += 'WHERE username=%s '
        expected_sql += 'ORDER BY device_info_serial'
        cursor.execute.assert_called_with(expected_sql, 'me')

    def test_fetchTrackers(self):
        rows = [{'id':1}]
        cursor = UserList(rows)
        cursor.execute = Mock()

        result = views.fetchTrackers(cursor, 'me')

        sql = 'SELECT device_info_serial as id '
        sql += 'FROM gps.uva_device '
        sql += 'JOIN uva_access_device USING (device_info_serial) '
        sql += 'WHERE username=%s '
        sql += 'ORDER BY device_info_serial'
        cursor.execute.assert_called_with(sql, 'me')
        self.assertEqual(result, [{'id':1}])

    def test_fetchAcceleration(self):
        rows = [{
                 'date_time': datetime(2013,8,29,10,0,0),
                 'index': 0,
                 'x_acceleration': 1.0,
                 'y_acceleration': 1.0,
                 'z_acceleration': 1.0,
                 }, {
                 'date_time': datetime(2013,8,29,10,0,0),
                 'index': 1,
                 'x_acceleration': 2.0,
                 'y_acceleration': 3.0,
                 'z_acceleration': 4.0,
                 }]
        cursor = UserList(rows)
        cursor.execute = Mock()
        trackerId = 1234
        start = datetime(2013,8,29,9,0,0)
        end = datetime(2013,8,29,11,0,0)

        results = views.fetchAcceleration(cursor, 'me', trackerId, start, end)

        expected = {
                    datetime(2013,8,29,10,0,0): [{
                                                  'time': 0.0,
                                                  'x_acceleration': 1.0,
                                                  'y_acceleration': 1.0,
                                                  'z_acceleration': 1.0,
                                                  }, {
                                                  'time': 0.05,
                                                  'x_acceleration': 2.0,
                                                  'y_acceleration': 3.0,
                                                  'z_acceleration': 4.0,
                                                  }]
                    }
        self.assertEqual(results, expected)

