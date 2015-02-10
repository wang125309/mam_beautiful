from django.db import models

# Create your models here.

class User(models.Model):
	openid = models.CharField(max_length=64)
	prize = models.CharField(max_length=32)
	name = models.CharField(max_length=128)
	phone = models.CharField(max_length=64)
	province = models.CharField(max_length=128)
	city = models.CharField(max_length=128)
	area = models.CharField(max_length=128)
	address = models.CharField(max_length=256)
	nickname = models.CharField(max_length=256)
	dateline = models.CharField(max_length=64)
	
class Calculate(models.Model):
	bonusnum = models.IntegerField()
	total = models.IntegerField()
	percent = models.IntegerField()
	firstpercent = models.IntegerField()

class Wx(models.Model):
	access_token = models.CharField(max_length=256)
	js_ticket = models.CharField(max_length=256)
