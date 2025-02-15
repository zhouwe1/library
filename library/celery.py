import os
from celery import Celery
from celery.schedules import crontab
from .const import NOTIFY

# 设置环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'library.settings')

# 实例化
app = Celery('library')
app.conf.timezone = 'Asia/Shanghai'
app.conf.enable_utc = False
# namespace='CELERY' 作用是允许你在 Django 配置文件中对 Celery 进行配置,但所有 Celery 配置项必须以 CELERY开头，防止冲突
app.config_from_object('django.conf:settings', namespace="CELERY")
# 自动从 Django 的已注册 app 中发现任务
app.autodiscover_tasks()



app.conf.beat_schedule = {
    'send_cmd': {
        'task': 'borrow.tasks.notify_expired_in_days',
        'schedule':crontab(hour=NOTIFY.notify_hour.value, minute=NOTIFY.notify_minute.value),
        'args': (NOTIFY.notify_expired_in_days.value,),
    }
}