from .base import *

ALLOWED_HOSTS = ['0.0.0.0']

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smg_db',
        'USER': 'admin',
        'PASSWORD': 'homm1994',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
