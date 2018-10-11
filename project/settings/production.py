# Production settings

from .base import *

# Settings file
config.read('/etc/shutterize/settings.ini')

# Read secret key
SECRET_KEY = config.get('keys','SECRET_KEY')

# Disable debug for production
DEBUG = False

ALLOWED_HOSTS = ['18.222.117.200', 'ec2-18-222-117-200.us-east-2.compute.amazonaws.com', 'jmblinds.shutterize.io', 'dummy.shutterize.io']

# Server database
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.mysql',
    'OPTIONS': {
        'read_default_file': '/etc/shutterize/settings.ini',
    },
}
}

# collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
