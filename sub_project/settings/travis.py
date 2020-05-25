import os
from . import *

DEBUG = False

DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     os.environ.get('DB_NAME'),
            'USER':     os.environ.get('DB_USER'),
            'PASSWORD': '',
            'HOST':     'localhost',
            'PORT':     '',
        }
}
