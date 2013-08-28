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
        cursor = UserList([{'id':1}])
        cursor.close = Mock()
        cursor.execute = Mock()
        db = Mock()
        db.cursor = Mock(return_value=cursor)
        request.db = db

        result = views.trackers(request)

        sql = 'SELECT device_info_serial as id '
        sql += 'FROM gps.uva_device ORDER BY device_info_serial'
        cursor.execute.assert_called_with(sql)
        cursor.close.assert_called_with()
        self.assertEqual(result, {'trackers': [{'id':1}]})
