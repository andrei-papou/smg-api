from .base import *

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

SECRET_KEY = os.environ.get('SECRET_KEY', '34ff3@d33(()OD#J*DJSSNjdjwd2#31')

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
