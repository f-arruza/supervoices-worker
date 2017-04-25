web: gunicorn Supervoices.wsgi --log-file -
worker: python manage.py celery -A Supervoices worker -l info
