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

logger = logging.getLogger(__package__)


@view_config(route_name="home", renderer="home.mako")
def home(request):
    return {}


@view_config(route_name='trackers', renderer='json')
def trackers(request):
    """Returns a list of tracker identifiers the user has access to"""
    cur = request.db.cursor()
    return {'trackers': fetchTrackers(cur)}


def fetchTrackers(cur):
    cur.execute("""
        SELECT DISTINCT device_info_serial as id
        FROM gps.ee_tracker_limited
        ORDER BY device_info_serial
    """)
    return list(cur)


def fetchTrack(cur, trackerId, start, end):
    # TODO accelartion freq is hardcoded
    freq = 20.0

    sql2 = """
    SELECT
    timezone('zulu', date_time) date_time,
    round(s.latitude::numeric, 5) lat,
    round(s.longitude::numeric, 5) lon,
    s.altitude,
    s.altitude altitude_asl,
    elevation.srtm_getvalue(s.location) AS ground_elevation,
    --s.pressure,
    s.temperature,
    --s.gps_fixtime, s.positiondop,
    --s.h_accuracy, s.v_accuracy, s.x_speed, s.y_speed, s.z_speed, s.speed_accuracy,
    --s.vnorth, s.veast, s.vdown,
    round(s.speed::numeric, 5) AS speed,
    --s.speed3d,
    round(s.direction, 2) AS direction
    ,round(mod(s.direction - lag(s.direction) over (order by device_info_serial, date_time), 180.0), 2) AS delta_direction
    ,round((
      ST_Length_Spheroid(ST_MakeLine(location, lag(location) over (order by device_info_serial, date_time)), 'SPHEROID["WGS 84",6378137,298.257223563]')
      /
      EXTRACT(EPOCH FROM (date_time - lag(date_time) over (order by device_info_serial, date_time)))
     )::numeric, 5) as tspeed
    ,round(degrees(ST_Azimuth(location, lag(location) over (order by device_info_serial, date_time)))::numeric, 2) tdirection
    ,aa.x_acceleration, aa.y_acceleration , aa.z_acceleration
    ,aa.time_acceleration
    FROM
    gps.ee_tracking_speed_limited s
    LEFT JOIN
    (
    SELECT date_time
    , array_agg(time_acceleration) time_acceleration
    , array_agg(x_acceleration) x_acceleration
    , array_agg(y_acceleration) y_acceleration
    , array_agg(z_acceleration) z_acceleration
    FROM
    (
    SELECT
    device_info_serial, date_time
    , round(a.index/%s, 4) time_acceleration
    , round(CAST ((x_acceleration-x_o)/x_s AS numeric), 4) x_acceleration
    , round(CAST ((y_acceleration-y_o)/y_s AS numeric), 4) y_acceleration
    , round(CAST ((z_acceleration-z_o)/z_s AS numeric), 4) z_acceleration
    FROM gps.ee_acceleration_limited a
    JOIN (
      SELECT DISTINCT device_info_serial, x_o,x_s,y_o,y_s,z_o,z_s
      FROM gps.ee_tracker_limited d
    ) tu USING (device_info_serial)
    WHERE
    device_info_serial = %s AND date_time BETWEEN %s AND %s
    -- order in sub-select so array_agg is ordered
    ORDER BY date_time, index
    ) a
    GROUP BY date_time
    ) aa USING (date_time)
    WHERE
    device_info_serial = %s AND date_time BETWEEN %s AND %s
    AND userflag != 1 AND longitude IS NOT NULL
    """

    cur.execute(sql2, (freq, trackerId, start, end, trackerId, start, end))
    return cur


@view_config(route_name='tracker', renderer='json')
def tracker(request):
    """Returns gps+accel data of tracker in a certain time range"""
    cur = request.db.cursor()
    trackerId = int(request.matchdict['id'])
    start = parse_date(request.matchdict['start']).isoformat()
    end = parse_date(request.matchdict['end']).isoformat()
    return fetchTrack(cur, trackerId, start, end)
