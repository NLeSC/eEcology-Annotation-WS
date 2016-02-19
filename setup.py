import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'pyramid',
    'psycopg2',
    'mock',
    'waitress',
    'nose',
    'coverage',
    'iso8601',
    'gunicorn',
    'simplejson',
    'pyramid_mako',
    'paste',
    ]

exec(open('annotation/version.py').read())

setup(name='Annotation',
      version=__version__,
      description='Annotation',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Programming Language :: Python :: 2.7",
        ],
      author='Stefan Verhoeven',
      author_email='s.verhoeven@esciencecenter.nl',
      url='https://github.com/NLeSC/eEcology-Annotation-WS',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="annotation",
      entry_points="""\
      [paste.app_factory]
      main = annotation:main
      """,
      )
