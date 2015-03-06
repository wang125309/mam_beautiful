from django.db import models

# Create your models here.

class User(models.Model):
    openid = models.CharField(max_length=256)
    nickname = models.CharField(max_length=256,null=True)
    headimgurl = models.CharField(max_length=256,null=True)
    code = models.CharField(max_length=256)
    phone = models.CharField(max_length=256,null=True)
    times = models.IntegerField(null=True)
    dateline = models.CharField(max_length=64)
    total_height = models.IntegerField()
class Help(models.Model):
    openid = models.CharField(max_length=256)
    toopenid = models.CharField(max_length=256)
    dateline = models.CharField(max_length=64)
    height = models.IntegerField()
    
