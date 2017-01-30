import os
import socket

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Running in Travis CI?
if os.environ.get('TRAVIS'):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://travis:@localhost/haralyzer_api_test'
# Running in wercker world?
elif os.environ.get('WERCKER'):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:{0}@{1}/haralyzer_api_test'.format(
                                os.environ.get('MYSQL_ENV_MYSQL_ROOT_PASSWORD'),
                                os.environ.get('MYSQL_PORT_3306_TCP_ADDR'))
    REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR')

else:
    REDIS_HOST = 'redis'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:{0}@{1}/haralyzer_api_test'.format(
                                os.environ.get('MYSQL_ENV_MYSQL_ROOT_PASSWORD'),
                                'mysql')

    # Local development, get this working later
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(
    #    os.path.join(BASE_DIR, 'data-dev.db'))

# Enables app debugging and renders stack traces to response
DEBUG = True
# Enables app testing mode
TESTING = True
# Enables the storage of raw HAR data in a redis store. This is not required,
# but is recommended and enabled by default, as it will allow you to update
# "in flight" if necessary. This is because all of the child 'page' objects are
# created by parsing and analyzing the HAR data. As of right now, the HAR data
# is not used in the code at all, but in the future, the page objects will seek
# details from the HAR data if they are NULL.
STORE_HAR_DATA = True
# Redis settings
