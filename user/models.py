from django.db import models
from django.utils.timezone import now
# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=32)  # 姓名
    id_code = models.CharField(max_length=18)  # 身份证号
    phone = models.CharField(max_length=16)  # 手机号
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField()
