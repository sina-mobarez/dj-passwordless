from __future__ import absolute_import, unicode_literals
import os
from core.logger import logger
from celery import Celery
from celery import signals

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    worker_log_format='[%(asctime)s] [%(levelname)s] [%(process)d] [%(task_name)s(%(task_id)s)] %(message)s',
    worker_log_color=True,
)
app.autodiscover_tasks()


@signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    logger.info('Celery is start succeeded')

@signals.task_success.connect
def on_task_success(sender=None, **kwargs):
    logger.info(f'Task {sender.name} succeeded')

@signals.task_failure.connect
def on_task_failure(sender=None, exception=None, traceback=None, **kwargs):
    logger.error(f'Task {sender.name} failed: {exception}')