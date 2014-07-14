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

import logging
from iso8601 import parse_date
from iso8601.iso8601 import UTC
from pyramid.view import view_config
from pyramid.response import Response

logger = logging.getLogger(__package__)

class Upload(object):
    """
    Serves annotations from a table with following structure::

        CREATE TABLE classification.annotation_538_movement
        (
          device_info_serial integer NOT NULL,
          date_time timestamp without time zone NOT NULL,
          first_index integer NOT NULL,
          class_id integer,
          class_name character varying(255),
          class_red double precision,
          class_green double precision,
          class_blue double precision,
          CONSTRAINT annotation_538_movement_pkey PRIMARY KEY (device_info_serial, date_time, first_index)
        );
    """

    def __init__(self, request):
        self.request = request
        self.db = request.db
        self.table = request.matchdict.get('table', '')
        self.tracker_id = request.matchdict.get('tracker', 0)

    def fetch_classifications(self):
        cursor = self.db.cursor()
        sql_template = "SELECT DISTINCT class_id AS id, class_name AS label, 'rgb(' || floor(class_red*255) ||',' || floor(class_green*255) || ',' || floor(class_blue*255) || ')' AS color FROM {table} ORDER BY class_id"
        sql = sql_template.format(table=self.table)
        cursor.execute(sql)
        return cursor.fetchall()

    def fetch_trackers(self):
        cursor = self.db.cursor()
        sql_template = 'SELECT device_info_serial AS id, MIN(date_time) AS start, MAX(date_time) AS end FROM {table} GROUP BY device_info_serial ORDER BY device_info_serial'
        sql = sql_template.format(table=self.table)
        cursor.execute(sql)
        trackers = cursor.fetchall()
        for tracker in trackers:
            tracker['annotations'] = self.request.route_path('annotations.csv', table=self.table, tracker=tracker['id'])
        return trackers

    @view_config(route_name='uploads.html', renderer='uploads.mako')
    def index(self):
        table = self.request.params.get('table', '')
        if table == '':
            return {'trackers': [], 'table': ''}
        else:
            self.table = table

        trackers = self.fetch_trackers()
        return {'trackers': trackers, 'table': self.table}

    @view_config(route_name='upload.html', renderer='upload.mako')
    def upload_html(self):
        return {'tracker_id': self.tracker_id, 'table': self.table}

    @view_config(route_name='meta.json', renderer='json')
    def meta_json(self):
        classifications = self.fetch_classifications()
        trackers = self.fetch_trackers()
        return {'classifications': classifications, 'trackers': trackers}

    @view_config(route_name='annotations.csv')
    def annotations(self):
        cursor = self.db.cursor()
        sql_template = 'SELECT device_info_serial AS id, date_time AS ts, class_id AS class FROM {table} WHERE device_info_serial=%(tracker)s ORDER BY device_info_serial, date_time'
        sql = sql_template.format(table=self.table)
        cursor.execute(sql, {'tracker': self.tracker_id})
        annotations = ['id,ts,class']
        for a in cursor.fetchall():
            annotations.append(str(a['id']) + ',' + a['ts'].isoformat() + 'Z,' + str(a['class']))
        return Response("\n".join(annotations), content_type="text/csv")


