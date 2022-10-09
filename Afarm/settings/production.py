from .base import *

DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["abuadfarm-production.up.railway.app", "abuadfarm.herokuapp.com"]
CSRF_TRUSTED_ORIGIN = ["https://abuadfarm-production.up.railway.app", "https://abuadfarm.herokuapp.com"]

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': '',
    #     'USER': '',
    #     'PASSWORD': '',
    #     'HOST': '',
    #     'PORT': '',
    # }
    'default':{}
}

import django_heroku
django_heroku.settings(locals())