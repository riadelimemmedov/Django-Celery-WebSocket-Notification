from  __future__  import absolute_import,unicode_literals
import os
from time import timezone

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','channels_celery_project.settings')

app = Celery('channels_celery_project')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Baku')

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))