# Quick-start development settings - unsuitable for production

from .base import *

# Settings file
config.read('/usr/local/etc/shutterize/settings.ini')

# Read secret key
SECRET_KEY = config.get('keys','SECRET_KEY')

# Only for development
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'users.local', '.users.local']

# local database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/usr/local/etc/shutterize/settings.ini',
        },
    }
}
