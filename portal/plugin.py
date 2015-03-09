from models import *
from django.http import JsonResponse,HttpResponseRedirect
import random
import json
import requests
import logging
import time
import hashlib
logger = logging.getLogger(__name__)
address = 'blow'

def wx_login(appid,secret,code):
	r = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token?appid="+appid+"&secret="+secret+"&code="+code+"&grant_type=authorization_code")
	access_res = r.json()
	#r = requests.get("https://api.weixin.qq.com/sns/oauth2/refresh_token?appid="+appid+"&grant_type=refresh_token&refresh_token="+access_res['refresh_token'])
	#access_res = r.json()
	r = requests.get("https://api.weixin.qq.com/sns/userinfo?access_token="+access_res['access_token']+"&openid="+access_res['openid']+"&lang=zh_CN")
	r.encoding = 'utf8'
	return r.json()
def get_access_token(appid,secret):
	r = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+appid+"&secret="+secret)
	res = r.json()
	w = Wx.objects.get(id=1)
	if w :
		w.access_token = res['access_token']
	else:
		w = Wx(access_token=res['access_token'])
	w.save()
	return res['access_token']
def get_js_ticket(access_token,appid,secret):
	r = requests.get("https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token="+access_token+"&type=jsapi")
	res = r.json()
	if res['errcode'] != 0:
		access_token = get_access_token(appid,secret)
		r = requests.get("https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token="+access_token+"&type=jsapi")
		res = r.json()
		w = Wx.objects.get(id=1)
		w.js_ticket = res['ticket']
		w.access_token = access_token
		w.save()
		return res['ticket']
	else:
		w = Wx.objects.get(id=1)
		w.js_ticket = res['ticket']
		w.save()
		return res['ticket']
def sign(js_ticket,url):
	s = "nameLR9969"
	timestamp = int(time.time())
	fullurl = "jsapi_ticket=" + js_ticket + "&noncestr=" + s +"&timestamp=" + str(timestamp) + "&url=" +url
	print fullurl
	sha1obj = hashlib.sha1()
	sha1obj.update(fullurl)
	hash = sha1obj.hexdigest()
	print hash
	return {
		"hash":hash,
		"timestamp":timestamp
	}
def base_access_token(appid,secret):
    access_token = get_access_token(appid,secret)
    js_ticket = get_js_ticket(access_token,appid,secret)
    sign(js_ticket,"http://www.360youtu.com/"+address+"/public")
    return {
			"access_token":access_token,
			"js_ticket":js_ticket
    }



