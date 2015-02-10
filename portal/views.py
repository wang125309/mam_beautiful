from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
import logging
from models import *
from plugin import *
# Create your views here.
logger = logging.getLogger(__name__)
appid = "wxa57abe5e5e6fae56"
secret = "40ba84cbf0be7df4287cc0a3ef586912"

def login(request):
	return render(request,"login.html")

def index(request):
	try:
		request.session['openid']
		request.session['nickname']
	except Exception,e:
		person_information = wx_login(appid,secret,request.GET['code'])
		#refrash session
		request.session['openid'] = person_information['openid']
		request.session['nickname'] = person_information['nickname']
	return render(request,"index.html")
def click(request):
	return JsonResponse({
		"num" : Calculate.objects.get(id=1).total
	})
def wxconfig(request):
	url = request.POST['url']
	js_ticket = Wx.objects.get(id=1).js_ticket
	s = sign(js_ticket,url)
	json = {
			"debug":true,
		"appId":appid,
		"timestamp":s['timestamp'],
		"nonceStr":'nameLR9969',
		"signature":s['hash'],
		"jsApiList":['onMenuShareAppMessage','onMenuShareTimeline']
	}
	print json
	return JsonResponse(json)
def update_access_token(request):
	get_js_ticket(get_access_token(appid,secret),appid,secret)
	return JsonResponse({
		"status":"success"
	})
def bonus(request):
	prize = bonus_get(request.session['openid'],request.session['nickname'])
	cal = Calculate.objects.get(id=1)
	cal.total = cal.total + 1
	cal.save()
	return render(request,"bonus.html",{
		"prize":prize,
		"cal":cal.total
	})
def edit(request):
	name = request.POST['name']
	phone = request.POST['phone']
	province = request.POST['province']
	city = request.POST['city']
	area = request.POST['area']
	address = request.POST['address']
	if not name.strip() or not phone.strip() or not province.strip() or not city.strip() or not area.strip() or not address.strip():
		return JsonResponse({"status":"empty error"})
	if len(phone.strip()) != 11:
		return JsonResponse({"status":"phone error"})
	user = User.objects.get(openid=request.session['openid'])
	user.name = name
	user.phone = phone
	user.province = province
	user.city = city
	user.area = area
	user.address = address
	user.save()
	return JsonResponse({"status":"correct"})
