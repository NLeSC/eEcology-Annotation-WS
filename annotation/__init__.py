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
import decimal
import logging
import psycopg2
import simplejson
from psycopg2.extras import RealDictCursor
from pyramid.authentication import RemoteUserAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS, DENY_ALL
from pyramid.security import unauthenticated_userid
from pyramid.renderers import JSON

logger = logging.getLogger(__package__)


def dbsession(dsn):
    return psycopg2.connect(dsn, cursor_factory=RealDictCursor)

def request_credentials(request):
    """Returns the username/password from the authorization header with Basic Authentication.

    When authorization header is missing it returns (None, None) tuple.
    """
    if 'HTTP_AUTHORIZATION' not in request.environ:
        logger.warn('No HTTP_AUTHORIZATION found, using empty credentials')
        return (None, None)
    (method, auth) = request.environ['HTTP_AUTHORIZATION'].split(' ', 1)
    if method.lower() != 'basic':
        err = 'Can only request credentials from Basic Authentication'
        raise NotImplementedError(err)
    (username, password) = auth.strip().decode('base64').split(':', 1)
    return (username, password)

def _connect(request):
    settings = request.registry.settings
    (username, password) = request_credentials(request)
    dsn = settings['dsn'].format(username=username, password=password)
    conn = dbsession(dsn)

    def cleanup(_):
        conn.close()

    request.add_finished_callback(cleanup)
    return conn


@subscriber(NewRequest)
def new_request(event):
    """Make db connection available as request.db"""
    request = event.request
    request.set_property(_connect, 'db', reify=True)


def get_user(request):
    return unauthenticated_userid(request)


class RootFactory(object):
    __acl__ = [(Allow, Authenticated, 'view'), DENY_ALL]

    def __init__(self, request):
        pass


def datetime_adaptor(obj, request):
    return obj.isoformat()
def timedelta_adaptor(obj, request):
    return str(obj)
def decimal_adaptor(obj, request):
    return float(obj)
def cursor_adaptor(obj, request):
    # would like to use yield, but json lib doesnt do iterators so unroll cursor into list
    return list(obj)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    config.add_request_method(get_user, 'user', reify=True)
    authen = RemoteUserAuthenticationPolicy('HTTP_REMOTE_USER')
    config.set_authentication_policy(authen)
    config.set_default_permission('view')
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_root_factory(RootFactory)

    # The default json renderer is pure python try other implementations
    # Benchmarks with 760/2013-05-31T00:00:00Z/2013-08-09T00:00:00Z
    # json = 41s
    # simplejson = 26s
    # omnijson = ~ incorrect response no adaptor support
    # ujson = ~ incorrect response no adaptor support
    # yajl = ~ incorrect response no adaptor support
    # jsonlib2 = 58s
    # jsonlib =  61s
    # anyjson = ~ incorrect response no adaptor support
    # Conclusion use simplejson
    json_renderer = JSON(serializer=simplejson.dumps)
    json_renderer.add_adapter(datetime.datetime, datetime_adaptor)
    json_renderer.add_adapter(datetime.timedelta, timedelta_adaptor)
    json_renderer.add_adapter(decimal.Decimal, decimal_adaptor)
    json_renderer.add_adapter(RealDictCursor, cursor_adaptor)
    config.add_renderer('json', json_renderer)

    config.add_static_view('aws/static', 'annotation:static')
    config.add_route('home', '/aws/')
    config.add_route('trackers', '/aws/trackers')
    config.add_route('tracker', '/aws/tracker/{id}/{start}/{end}')
    config.add_route('uploads.html', '/aws/uploads.html')
    config.add_route('meta.json', '/aws/uploads/{table}/meta.json')
    config.add_route('upload.html', '/aws/uploads/{table}/{tracker}/annotations.html')
    config.add_route('annotations.csv', '/aws/uploads/{table}/{tracker}/annotations.csv')
    config.scan()
    return config.make_wsgi_app()
