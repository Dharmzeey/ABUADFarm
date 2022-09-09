release: python manage.py migrate
web: gunicorn Afarm.wsgi
python manage.py collectstatic --noinput