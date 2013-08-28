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

import psycopg2
import psycopg2.extras
from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.events import subscriber


def dbsession(dsn):
    return psycopg2.connect(dsn, cursor_factory=psycopg2.extras.DictCursor)


def _connect(request):
    settings = request.registry.settings
    conn = request.registry.dbsession(settings['dsn'])

    def cleanup(_):
        conn.close()

    request.add_finished_callback(cleanup)
    return conn


@subscriber(NewRequest)
def new_request(event):
    request = event.request
    request.set_property(_connect, 'db', reify=True)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('trackers', '/aws/trackers')
    config.add_route('tracker', '/aws/tracker/{id}/{start}/{end}')
    config.scan()
    return config.make_wsgi_app()
