from .base import *

DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["abuadfarm-production.up.railway.app"]
CSRF_TRUSTED_ORIGIN = ["https://abuadfarm-production.up.railway.app"]

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}