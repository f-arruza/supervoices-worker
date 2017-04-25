from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

app = Celery('Supervoices')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# Iniciar Celery
# celery -A Supervoices worker -l info

# Iniciar Celery-Beats
# celery -A Supervoices beat -S djcelery.schedulers.DatabaseScheduler
