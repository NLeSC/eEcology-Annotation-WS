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
from pyramid.view import view_config

logger = logging.getLogger(__package__)


@view_config(route_name="home", renderer="home.mako")
def home(request):
    return {}


@view_config(route_name='trackers', renderer='json')
def trackers(request):
    """Returns a list of tracker identifiers the user has access to"""
    cur = request.db.cursor()
    return {'trackers': fetch_trackers(cur)}


def fetch_trackers(cur):
    cur.execute("""
        SELECT DISTINCT device_info_serial as id
        FROM gps.ee_tracker_limited
        JOIN gps.ee_track_session_limited USING (device_info_serial)
        ORDER BY device_info_serial
    """)
    return list(cur)


def fetch_track(cur, tracker_id, start, end):
    # TODO accelartion freq is hardcoded
    freq = 20.0

    sql2 = """
    SELECT
    timezone('zulu', date_time) date_time
    , round(s.latitude::numeric, 5) lat
    , round(s.longitude::numeric, 5) lon
    , s.altitude
    , s.altitude altitude_asl
    , s.altitude - s.altitude_agl AS ground_elevation
    , s.temperature
    , round(s.speed_2d::numeric, 5) AS speed
    , round((
      ST_Length_Spheroid(ST_MakeLine(location, lag(location) over (order by device_info_serial, date_time)), 'SPHEROID["WGS 84",6378137,298.257223563]')
      /
      EXTRACT(EPOCH FROM (date_time - lag(date_time) over (order by device_info_serial, date_time)))
     )::numeric, 5) as tspeed
    , round(s.direction, 2) AS idirection
    , round(degrees(ST_Azimuth(lag(location) over (order by device_info_serial, date_time), location))::numeric, 2) tdirection
    , round(mod(s.direction - lag(s.direction) over (order by device_info_serial, date_time), 180.0), 2) AS delta_idirection
    , round(degrees(
        ST_Azimuth(location, lead(location) over (order by device_info_serial, date_time)) -
        ST_Azimuth(lag(location) over (order by device_info_serial, date_time), location)
    )::numeric %% 180.0, 2) AS delta_tdirection
    , aa.time_acceleration
    , aa.x_acceleration, aa.y_acceleration, aa.z_acceleration
    FROM
    gps.ee_tracking_speed_limited s
    LEFT JOIN
    (
    SELECT device_info_serial, date_time
    , array_agg(round(a.index/%s, 4) ORDER BY date_time, index) time_acceleration
    , array_agg(round(((x_acceleration-x_o)/x_s)::numeric, 4) ORDER BY date_time, index) x_acceleration
    , array_agg(round(((y_acceleration-y_o)/y_s)::numeric, 4) ORDER BY date_time, index) y_acceleration
    , array_agg(round(((z_acceleration-z_o)/z_s)::numeric, 4) ORDER BY date_time, index) z_acceleration
    FROM gps.ee_acceleration_limited a
    JOIN (
      SELECT
    DISTINCT device_info_serial
    , x_o, x_s
    , y_o, y_s
    , z_o, z_s
      FROM gps.ee_tracker_limited d
    ) tu USING (device_info_serial)
    WHERE
    device_info_serial = %s AND date_time BETWEEN %s AND %s
    GROUP BY device_info_serial, date_time
    ) aa USING (device_info_serial, date_time)
    WHERE
    device_info_serial = %s AND date_time BETWEEN %s AND %s
    AND userflag != 1 AND longitude IS NOT NULL
    ORDER BY date_time
    """

    logger.debug('Fetching track data for id:{0}, start:{1}, end:{2}'.format(tracker_id, start, end))
    cur.execute(sql2, (freq, tracker_id, start, end, tracker_id, start, end))
    return cur


@view_config(route_name='tracker', renderer='json')
def tracker(request):
    """Returns gps+accel data of tracker in a certain time range"""
    cur = request.db.cursor()
    tracker_id = int(request.matchdict['id'])
    start = parse_date(request.matchdict['start']).isoformat()
    end = parse_date(request.matchdict['end']).isoformat()
    return fetch_track(cur, tracker_id, start, end)
