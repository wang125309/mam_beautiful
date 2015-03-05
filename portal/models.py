from django.db import models

# Create your models here.

class User(models.Model):
    openid = models.CharField(max_length=256)
    nickname = models.CharField(max_length=256,null=True)
    headimgurl = models.CharField(max_length=256,null=True)
    pos = models.IntegerField(null=True)
    power = models.IntegerField(null=True)
    code = models.CharField(max_length=256,null=True)
    count = models.IntegerField(null=True)
    phone = models.CharField(max_length=256,null=True)
    times = models.IntegerField(null=True)
    dateline = models.CharField(max_length=64)
    def __unicode__(self):
        return self.openid
class Code(models.Model):
    openid = models.CharField(max_length=256)
    dateline = models.CharField(max_length=64)
    code = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    used = models.CharField(max_length=32)
class Bonus(models.Model):
    openid = models.CharField(max_length=256)
    dateline = models.CharField(max_length=64,null=True)
    phone = models.CharField(max_length=256,null=True)
    total_money = models.IntegerField(null=True)
    apple_money = models.IntegerField(null=True)
    iphone = models.IntegerField(null=True)
    times = models.IntegerField(null=True)
    code = models.CharField(max_length=32,null=True)
    help_count = models.IntegerField(null=True)
    user = models.ForeignKey(User)
    help_count_last = models.IntegerField(null=True)   
    def __unicode__(self):
        return self.openid
class Help(models.Model):
    openid = models.CharField(max_length=256)
    toopenid = models.CharField(max_length=256)
    prize = models.CharField(max_length=128)
    dateline = models.CharField(max_length=64)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.openid
class Wx(models.Model):
	access_token = models.CharField(max_length=256)
	js_ticket = models.CharField(max_length=256)
class UserHistory(models.Model):
    openid = models.CharField(max_length=256)
    user = models.ForeignKey(User)
    dateline = models.CharField(max_length=256)
 
