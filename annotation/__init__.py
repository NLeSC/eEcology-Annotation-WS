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
import psycopg2
import psycopg2.extras
from pyramid.authentication import RemoteUserAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS, DENY_ALL
from pyramid.security import unauthenticated_userid

logger = logging.getLogger(__package__)


def dbsession(dsn):
    return psycopg2.connect(dsn, cursor_factory=psycopg2.extras.DictCursor)


def _connect(request):
    settings = request.registry.settings
    conn = dbsession(settings['dsn'])

    def cleanup(_):
        conn.close()

    request.add_finished_callback(cleanup)
    return conn


@subscriber(NewRequest)
def new_request(event):
    request = event.request
    request.set_property(_connect, 'db', reify=True)


def get_user(request):
    return unauthenticated_userid(request)


class RootFactory(object):
    __acl__ = [(Allow, Authenticated, 'view'), DENY_ALL]

    def __init__(self, request):
        pass


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_request_method(get_user, 'user', reify=True)
    authen = RemoteUserAuthenticationPolicy('HTTP_REMOTE_USER')
    config.set_authentication_policy(authen)
    config.set_default_permission('view')
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_root_factory(RootFactory)
    config.add_route('trackers', '/aws/trackers')
    config.add_route('tracker', '/aws/tracker/{id}/{start}/{end}')
    config.scan()
    return config.make_wsgi_app()
