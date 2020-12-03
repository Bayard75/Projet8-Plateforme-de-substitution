import os
#from . import *
import json
import requests
'''
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
'''
search_url = f'https://fr.openfoodfacts.org/cgi/search.pl?search_terms=&search_simple=1&action=process&page=1&json=True'
response = requests.get(search_url)
data = response.json()
for product in data['products']:
    try:
        stores = product['stores_tags']
        print(stores)
        print(type(stores))
    except:
        pass