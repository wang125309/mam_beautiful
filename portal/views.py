from django.shortcuts import render
import json
import requests
import logging
from plugin import *
# Create your views here.
logger = logging.getLogger(__name__)
appid = "wxa57abe5e5e6fae56"
secret = "40ba84cbf0be7df4287cc0a3ef586912"

def login(request):
	return render(request,"login.html")

def index(request):
	#try:
	#	request.session['openid']
	#except Exception,e:
#		person_information = wx_login(appid,secret,request.GET['code'])
		#refrash session
#		request.session['openid'] = person_information['openid']
	return render(request,"index.html")

def bonus(request):
	#prize = bonus_get(request.session['openid'],50,50,50)
	prize = "first"
	return render(request,"bonus.html",{
		"prize":prize
	})
