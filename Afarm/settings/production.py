from .base import *

DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["abuadfarm-production.up.railway.app", "abuadfarm.herokuapp.com"]
CSRF_TRUSTED_ORIGIN = ["https://abuadfarm-production.up.railway.app", "https://abuadfarm.herokuapp.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PGDATABASE'),
        'USER':os.environ.get('PGUSER'),
        'PASSWORD':os.environ.get('PGPASSWORD'),
        'HOST':os.environ.get('PGHOST'),
        'PORT':os.environ.get('PGPORT')

}
}