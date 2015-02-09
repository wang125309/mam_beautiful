from models import *
import random
import json
import requests
import logging
import redis
import time
logger = logging.getLogger(__name__)

def wx_login(appid,secret,code):
	r = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token?appid="+appid+"&secret="+secret+"&code="+code+"&grant_type=authorization_code")
	access_res = r.json()
	r = requests.get("https://api.weixin.qq.com/sns/oauth2/refresh_token?appid="+appid+"&grant_type=refresh_token&refresh_token="+access_res['refresh_token'])
	access_res = r.json()
	r = requests.get("https://api.weixin.qq.com/sns/userinfo?access_token="+access_res['access_token']+"&openid="+access_res['openid']+"&lang=zh_CN")
	return r.json()

def bonus_get(openid,percent,first_prize_percent,bonusnum):
	bonus_list = User.objects.all()
	for i in bonus_list:
		if i.openid == openid:
			return "NONE"
	else:
		ran = random.randint(0,100)
		if ran < percent :
			ran_per = random.randint(0,100)
			prize = "NONE"
			if ran_per < first_prize_percent:
				prize = "first"
			else:
				prize = "second"
			u = User(openid=openid,prize=prize,dateline=time.time())
			u.save()
			return prize
		else:
			return "NONE"
	
	
