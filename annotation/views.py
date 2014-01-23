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

import datetime
import logging
from iso8601 import parse_date
from iso8601.iso8601 import UTC
from pyramid.view import view_config

logger = logging.getLogger(__package__)


@view_config(route_name='trackers', renderer='json')
def trackers(request):
    cur = request.db.cursor()
    return {'trackers': fetchTrackers(cur, request.user)}


def fetchTrackers(cur, username):
    data = []
    cur.execute("SELECT device_info_serial as id FROM gps.uva_device JOIN gps.uva_access_device USING (device_info_serial) WHERE username=%s ORDER BY device_info_serial", (username,))
    for row in cur:
        row = dict(row)
        data.append(row)

    return data


def fetchAcceleration(cur, username, trackerId, start, end, freq=20.0):
    accels = {}
    sql1 = 'SELECT date_time, index, (x_acceleration-x_o)/x_s x_acceleration, '
    sql1 += '(y_acceleration-y_o)/y_s y_acceleration, (z_acceleration-z_o)/z_s z_acceleration '
    sql1 += 'FROM gps.uva_acceleration101 '
    sql1 += 'JOIN gps.uva_device USING (device_info_serial) '
    sql1 += 'JOIN gps.uva_access_device USING (device_info_serial)'
    sql1 += 'WHERE device_info_serial=%s and date_time BETWEEN %s AND %s AND username=%s '
    sql1 += 'ORDER BY date_time, index'
    cur.execute(sql1, (trackerId, start, end, username,))
    for row in cur:
        y = row['date_time']
        e = y.replace(tzinfo=UTC)
        z = e.isoformat()
        row['date_time'] = z
        if row['date_time'] not in accels:
            accels[row['date_time']] = []
        try:
            accels[row['date_time']].append({'time': int(row['index'])/freq,  # use 20Hz as freq
                                             "xa": row["x_acceleration"],
                                             "ya": row["y_acceleration"],
                                             "za": row["z_acceleration"]})
        except ValueError:
            continue

    return accels


def fetchTrack(cur, username, trackerId, start, end):
    sql2 = 'SELECT date_time, s.latitude, s.longitude, s.altitude, s.pressure, '
    sql2 += 's.temperature, s.gps_fixtime, s.positiondop, '
    sql2 += 's.h_accuracy, s.v_accuracy, s.x_speed, s.y_speed, s.z_speed,s.speed_accuracy, '
    sql2 += 's.vnorth, s.veast, s.vdown, s.speed, s.speed3d, s.direction, '
    sql2 += 't.speed as tspeed, t.direction as tdirection '
    sql2 += 'FROM gps.uva_tracking_speed s '
    sql2 += 'JOIN gps.get_uvagps_track_speed(%s, %s, %s) t USING (device_info_serial, date_time) '
    sql2 += 'JOIN gps.uva_access_device USING (device_info_serial) '
    sql2 += 'WHERE device_info_serial = %s AND '
    sql2 += 'date_time BETWEEN %s AND %s AND userflag != %s AND username=%s '
    sql2 += 'ORDER BY date_time'
    cur.execute(sql2, (trackerId, start, end, trackerId, start, end, "1", username,))
    return cur


def fetch(cur, username, trackerId, start, end):
    accels = fetchAcceleration(cur, username, trackerId, start, end)
    rows = fetchTrack(cur, username, trackerId, start, end)

    data = []
    for row in rows:
        row = dict(row)
        row['date_time'] = row['date_time'].replace(tzinfo=UTC).isoformat()
        if row['date_time'] in accels:
            row['accels'] = accels[row['date_time']]
        try:
            row['latitude'] = round(float(row['latitude']), 4)
            row['longitude'] = round(float(row['longitude']), 4)
            for x in ['altitude', 'temperature',
                      "gps_fixtime", "positiondop",
                      "h_accuracy", "v_accuracy",
                      "x_speed", "y_speed", "z_speed",
                      "speed_accuracy",
                      "vnorth", "veast", "vdown",
                      "speed", "speed3d", "direction",
                      "tspeed", "tdirection",
                      ]:
                if row[x] is not None:
                    row[x] = float(row[x])
            data.append(row)
        except ValueError:
            continue
        except TypeError:
            continue

    return data


@view_config(route_name='tracker', renderer='json')
def tracker(request):
    cur = request.db.cursor()
    trackerId = int(request.matchdict['id'])
    start = parse_date(request.matchdict['start']).isoformat()
    end = parse_date(request.matchdict['end']).isoformat()
    return fetch(cur, request.user, trackerId, start, end)
