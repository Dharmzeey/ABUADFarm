from .base import *

DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOST = ["abuadfarm-production.up.railway.app"]
CSRF_TRUSTED_ORIGIN = ["https://abuadfarm-production.up.railway.app"]