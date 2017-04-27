web: gunicorn Supervoices.wsgi --log-file -
worker: NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program python manage.py celery -A Supervoices worker -l info
