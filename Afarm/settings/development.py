from .base import *
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = True

# ALLOWED_HOSTS = ["localhost", '*.ngrok.io']
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.ngrok.io']

# THIS IS THE ONLY SITE THAT WILL ALLOW CSRF ACCESS
# I CREATED IT MYSELF
CSRF_TRUSTED_ORIGINS = ["https://127.0.0.1", 'https://*.ngrok.io']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'afarm',
    #     'USER': 'postgres',
    #     'PASSWORD': 'Azeezat1@',
    #     'HOST': '127.0.0.1',
    #     'PORT': '',
    # }
}
