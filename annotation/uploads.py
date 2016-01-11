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
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
import simplejson

logger = logging.getLogger(__package__)


class UploadViews(object):
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

    def fetch_classes(self):
        cursor = self.db.cursor()
        sql_template = "SELECT DISTINCT class_id AS id, class_name AS label, 'rgb(' || floor(class_red*255) ||',' || floor(class_green*255) || ',' || floor(class_blue*255) || ')' AS color FROM {table} ORDER BY class_id"
        sql = sql_template.format(table=self.table)
        cursor.execute(sql)
        return cursor.fetchall()

    def fetch_trackers(self):
        cursor = self.db.cursor()
        sql_template = """SELECT
          device_info_serial AS id,
          TIMEZONE('zulu', MIN(date_time)) AS start,
          TIMEZONE('zulu', MAX(date_time)) AS end,
        COUNT(*) AS count
        FROM "{table}"
        GROUP BY device_info_serial
        ORDER BY device_info_serial
        """
        sql = sql_template.format(table=self.table)
        cursor.execute(sql)
        trackers = cursor.fetchall()
        for tracker in trackers:
            tracker['size'] = self.track_size(tracker['id'], tracker['start'], tracker['end'])
            tracker['page_size'] = 500
            tracker['first_page'] = self.ts_track_after(tracker['id'], tracker['start'], tracker['end'], tracker['page_size'])
            tracker['last_page'] = self.ts_track_before(tracker['id'], tracker['start'], tracker['end'], tracker['page_size'])
        return trackers

    def fetch_annotations_as_csv(self, tracker_id, start, end):
        cursor = self.db.cursor()
        sql_template = '''SELECT
          device_info_serial,
          date_time,
          class_id
        FROM "{table}"
        WHERE
          device_info_serial=%(tracker)s
        AND
          date_time BETWEEN %(start)s AND %(end)s
        ORDER BY
          device_info_serial, date_time
        '''
        logger.debug('Fetching annotations for id:{0}, start:{1}, end:{2}'.format(tracker_id, start, end))
        sql = sql_template.format(table=self.table)
        cursor.execute(sql, {'tracker': tracker_id,
                             'start': start,
                             'end': end,
                             })
        annotations = ['device_info_serial,date_time,class_id']
        for a in cursor.fetchall():
            annotations.append(str(a['device_info_serial']) + ',' + a['date_time'].isoformat() + 'Z,' + str(a['class_id']))
        return "\n".join(annotations) + "\n"

    def track_size(self, tracker_id, start, end):
        cursor = self.db.cursor()
        sql = '''SELECT
          COUNT(*) AS count
        FROM gps.ee_tracking_speed_limited
        WHERE
          device_info_serial=%(tracker)s
        AND
          date_time BETWEEN %(start)s AND %(end)s
        '''
        cursor.execute(sql, {'tracker': tracker_id,
                             'start': start,
                             'end': end,
                             })
        result = cursor.fetchone()
        return result['count']

    def ts_track_after(self, tracker_id, start, end, count):
        cursor = self.db.cursor()
        sql = '''SELECT
          date_time
        FROM gps.ee_tracking_speed_limited
        WHERE
          device_info_serial=%(tracker)s
        AND
          date_time BETWEEN %(start)s AND %(end)s
        ORDER BY date_time
        LIMIT 1
        OFFSET %(count)s
        '''
        cursor.execute(sql, {'tracker': tracker_id,
                             'start': start,
                             'end': end,
                             'count': count,
                             })

        result = cursor.fetchone()
        if result:
            return result['date_time']
        else:
            return end

    def ts_track_before(self, tracker_id, start, end, count):
        cursor = self.db.cursor()
        sql = '''SELECT
          date_time
        FROM gps.ee_tracking_speed_limited
        WHERE
          device_info_serial=%(tracker)s
        AND
          date_time BETWEEN %(start)s AND %(end)s
        ORDER BY date_time DESC
        LIMIT 1
        OFFSET %(count)s
        '''
        cursor.execute(sql, {'tracker': tracker_id,
                             'start': start,
                             'end': end,
                             'count': count,
                             })
        result = cursor.fetchone()
        if result:
            return result['date_time']
        else:
            return start

    @view_config(route_name='uploads.html', renderer='uploads.mako')
    def uploads(self):
        '''
        Page with form to select table with annotations.

        Query parameters:
        - table: Postgresql schema and table seperated by a dot, eg myschema.mytable
        '''
        table = self.request.params.get('table', '')
        if table == '':
            return {'trackers': [], 'table': ''}
        else:
            self.table = table

        trackers = self.fetch_trackers()

        return {'trackers': trackers, 'table': self.table}

    @view_config(route_name='annotations.html', renderer='upload.mako')
    def upload(self):
        '''
        Page with eEcology Annotation UI with annotations loaded from databases.

        Query parameters:
        - id: tracker id,
        - start: start of time range in ISO8601 format
        - end: end of time range in ISO8601 format
        '''
        if not set(['id', 'start', 'end']).issubset(self.request.params.keys()):
            return HTTPFound(self.request.route_path('uploads.html', _query={'table': self.table}))
        tracker_id = int(self.request.params.get('id', 0))
        start = parse_date(self.request.params['start']).isoformat()
        end = parse_date(self.request.params['end']).isoformat()
        classes = self.fetch_classes()
        annotations_url = self.request.route_path('annotations.csv',
                                                  table=self.table,
                                                  )
        return {'tracker_id': tracker_id,
                'start': start,
                'end': end,
                'classes': simplejson.dumps(classes),
                'annotations_url': annotations_url,
                }

    @view_config(route_name='annotations.csv')
    def annotations_as_csv(self):
        '''
        Returns annotations from a table with a tracker and time range selection.

        Query parameters:
        - id: tracker id,
        - start: start of time range in ISO8601 format
        - end: end of time range in ISO8601 format
        '''
        tracker_id = self.request.params.get('id', 0)
        start = parse_date(self.request.params['start']).isoformat()
        end = parse_date(self.request.params['end']).isoformat()
        csv = self.fetch_annotations_as_csv(tracker_id, start, end)
        return Response(csv, content_type='text/csv')
