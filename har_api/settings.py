import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(BASE_DIR,
                                                              'data-dev.db'))

# Enables app debugging and renders stack traces to response
DEBUG = True
# Enables app testing mode
TESTING = True
