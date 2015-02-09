eEcology-Annotation-WS
======================

[![Build Status](https://travis-ci.org/NLeSC/eEcology-Annotation-WS.svg?branch=master)](https://travis-ci.org/NLeSC/eEcology-Annotation-WS)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/NLeSC/eEcology-Annotation-WS/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/NLeSC/eEcology-Annotation-WS/?branch=master)
[![Code Coverage](https://scrutinizer-ci.com/g/NLeSC/eEcology-Annotation-WS/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/NLeSC/eEcology-Annotation-WS/?branch=master)

Webservice for eEcology Annotation project.

Start development server
-------------------------

    python setup.py develop
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
                auth_basic "Restricted";
                auth_basic_user_file aws.users;
                proxy_set_header REMOTE_USER $remote_user;
                proxy_pass http://127.0.0.1:6565;
        }

The `aws.users` contains user/password combi created with htpasswd.

Apache production config
------------------------

Put WS and UI behind auth and follow instructions at https://services.e-ecology.sara.nl/redmine/projects/uvagps/wiki/Apache_authentication_against_DB .
The application needs the `REMOTE_USER` and `HTTP_AUTHORIZATION` environment variables so it can use those credentials to connect to the database.

User interface
--------------

The web user interface is in the `annotation/static/TrackAnnot` folder.
That folder has compiled/minimized javascript, the source/un-minimized version can be found in the  https://github.com/NLeSC/eEcology-Annotation-UI repository.

Timeouts
--------

The fetch track data from the database can take a while to do. The webserver can timeout, causing the fetching to stopped prematurely.

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

Docker build
------------

### Construct image

1. Install User interface in `annotation/static/TrackAnnot` folder.
2. `sudo docker build -t sverhoeven/annotation:1.0.0-db3 .`
3. Export or push to registry

### Run container

1. Import or pull from registry
2. `sudo docker run -p 6565:6565 --env DB_HOST=db.e-ecology.sara.nl -d --name annotation sverhoeven/annotation:1.0.0-db3`

Error log is available with `sudo docker logs annotation`.
Access log can be read using `sudo docker exec annotation /bin/less /usr/src/app/access.log`.

Web application will run on http://localhost:6565/aws/

Copyrights & Disclaimers
------------------------

eEcology script wrapper is copyrighted by the Netherlands eScience Center and releases under
the Apache License, Version 2.0.

See <http://www.esciencecenter.nl> for more information on the Netherlands
eScience Center.

See the "LICENSE" and "NOTICE" files for more information.
