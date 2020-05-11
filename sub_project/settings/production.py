import os
from .base import *
DEBUG = False

SECRET_KEY = os.environ.get('SUB_PROJECT_SK')

ALLOWED_HOSTS = ['*']