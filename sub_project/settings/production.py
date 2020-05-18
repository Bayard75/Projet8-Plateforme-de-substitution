from . import *

DEBUG = False
ALLOWED_HOSTS = ['35.180.25.7']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
        'NAME': 'purbeurre', # le nom de notre base de données créée précédemment
        'USER': 'ubuntu', # attention : remplacez par votre nom d'utilisateur !!
        'PASSWORD': 'purbeurre',
        'HOST': '',
        'PORT': '5432',
    }
}