eEcology-Annotation-WS
======================

Webservice for eEcology Annotation project.

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

Bla

