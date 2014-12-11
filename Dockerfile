FROM python:2-onbuild
MAINTAINER Stefan Verhoeven "s.verhoeven@esciencecenter.nl"
EXPOSE 6565
ENV DB_HOST db.e-ecology.sara.nl
RUN python setup.py develop
CMD gunicorn --env DB_HOST=$DB_HOST --paste docker.ini
