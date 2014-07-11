eEcology-Annotation-WS
======================

Webservice for eEcology Annotation project.

Start development server
-------------------------

    cp development.ini-dist development.ini
    # adjust database settings
    . env/bin/activate
    pserve development.ini

NGINX develop config
--------------------

Using a hardcoded user.

        location /aws {
                gzip on;
                gzip_types application/json;
                gzip_proxied any;
                proxy_set_header REMOTE_USER <user with tracker rights>;
                proxy_pass http://127.0.0.1:6565;
        }

Apache production config
------------------------

Put WS and UI behind auth and follow instructions at https://services.e-ecology.sara.nl/redmine/projects/uvagps/wiki/Apache_authentication_against_DB .

Timeout
~~~~~~~

Configure apache to allow for longer request handling by addding to httpd config:

    Timeout 300
    ProxyTimeout 300

Required permissions for user
-----------------------------

0. User needs a eEcology DB account.
1. The user should have `gps_limited` roles.
2. The user should have access to one or more trackers.
3. Then it should work.

Api documentation
-----------------

The api documentation can be found in [apiary.apib](apiary.apib).
Generate html version of api with

    npm install aglio
    aglio -i apiary.apib -o api.html
