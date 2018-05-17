from django.db import models

# Create your models here.

class User(models.Model):
    userNo = models.IntegerField(default=0x01)
    ip = models.CharField(null=True, max_length = 100)

class UrlLog(models.Model):
    user = models.ForeignKey(User)
    url = models.CharField(default=0x02, max_length = 100)
    urlArgs = models.TextField(null=True)
    time = models.DateTimeField()