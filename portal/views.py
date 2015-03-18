# coding=utf8
from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
import json
import requests
import logging
from models import *
from plugin import *
import datetime
from sendmsg import *
from functools import wraps
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# Create your views here.
logger = logging.getLogger(__name__)
appid = "wx91e4c1925de9ff50"
secret = "f2f564ea79ff43f7ed3004821ac3b2b8"

def need_login(func):
    def _need_login(request):
        if not request.session.get("openid",False):
            if request.GET.get("code",False):
                w = wx_login(appid,secret,request.GET['code'])
                request.session['openid'] = w['openid']
                try:
                    u = User.objects.get(openid=request.session['openid'])
                except Exception,e:
                    u = User(openid = request.session['openid'],headimgurl=w['headimgurl'].encode("utf8"),nickname=w['nickname'].encode('utf8'),dateline=str(time.time()),total_height=0)
                    u.save()
                return func(request)
            else:
                if request.GET.get("openid",False):
                    return HttpResponseRedirect("/blow/login/?openid="+request.GET['openid'])
                return HttpResponseRedirect("/blow/login/") 
        else:
            return func(request)
    return _need_login
def login(request):
	return render(request,"login.html")
@need_login
def enter(request):
    if request.GET.get('openid',False):
        return HttpResponseRedirect("/blow/public/?openid="+request.GET['openid'])
    return HttpResponseRedirect("/blow/public/")
@need_login
def index(request):
    try:
        u = User.objects.get(openid=request.session['openid'])
        prize = 0
        if u.total_height >= 10000:
            prize = 1
        mobile = "0"
        if u.phone :
            mobile = u.mobile
        json = {
            "status":"success",
            "reason":"",
            "message":{
                "uid":u.id,
                "openid":request.session['openid'],
                "total_height":u.total_height,
                "dateline":u.dateline,
                "nickname":u.nickname,
                "headimgurl":u.headimgurl,
                "height":u.times,
                "prize":prize,
                "mobile":mobile
            }
        }
    except Exception,e:
        json = {
            "status":"fail",
            "reason":"no such user",
            "message":{},
        }
    return JsonResponse(json)
def can_play(request):
    if request.GET.get('openid',False):
        
        try:
            h = Help.objects.get(toopenid=request.GET['openid'],openid=request.session['openid'])
            if h:
                return JsonResponse({
                    "status":"success",
                    "reason":"",
                    "message":{
                        "data":"can't help"
                    }
                })
            else:
                return JsonResponse({
                    "status":"success",
                    "reason":"",
                    "message":{
                        "data":"can help"
                    }
                })
        except Exception,e:
            return JsonResponse({
                "status":"success",
                "reason":str(e),
                "message":{
                    "data":"can help"
                }
            })
    else:
        try:
            u = User.objects.get(openid=request.session['openid'])
            if u.times and u.shared:
                return JsonResponse({
                    "status":"success",
                    "reason":"",
                    "message":{
                        "data":"played"
                    }
                })
            else:
                return JsonResponse({
                    "status":"success",
                    "reason":"",
                    "message":{
                        "data":"can play"
                    }
                })
        except Exception,e:
            return JsonResponse({
                "status":"fail",
                "reason":str(e),
                "message":{
                    "data":"no such user"
                }
            })
def share_complate(request):
    u = User.objects.get(openid=request.session['openid'])
    if u.times:
        u.shared = '1'
        u.save()
    return JsonResponse({
        "status":"success",
        "reason":"",
        "message": {
            "share":"complate"    
        }
    })
def share_message(request):
    u = User.objects.all()
    me = User.objects.get(openid=request.session['openid'])
    t = 0
    now = 0
    for i in u:
        t += 1
        if i.times < me.times:
            now += 1
    over = now/t*100; 
    return JsonResponse({
        "status":"success",
        "reason":"",
        "message": {
            "over":over
        }
    })      
              
             
def add_height(request):
    try:
        u = User.objects.get(openid=request.GET['openid'])
        p = [40,20,20,10,7,3]
        n = random.randint(0,100)
        h = 1
        t5000 = 20
        t8000 = 10
        t10000 = 5
        if n < p[0]:
            h = random.randint(1,300)
        elif n < p[0] + p[1] and n >= p[0]:
            h = random.randint(301,500)
        elif n < p[0] + p[1] + p[2] and n >= p[0] + p[1]:
            h = random.randint(501,700)
        elif n < p[0] + p[1] + p[2] + p[3] and n >= p[0] + p[1] + p[2]:
            h = random.randint(701,800)
        elif n < p[0] + p[1] + p[2] + p[3] + p[4] and n >= p[0] + p[1] + p[2] + p[3]:
            h = random.randint(801,900)
        else :
            h = random.randint(901,1000)
        count_5000 = User.objects.filter(total_height__gt=10000).count()
        if count_5000 >= t5000:
            #feed
            if u.total_height >= 10000:
                #看是不是冲8000,20人
                count_8000 = User.objects.filter(total_height__gt=15000).count()
                if count_8000 >= t8000:
                    if u.total_height >= 15000:
                        count_10000 = User.objects.filter(total_height__gt=20000).count()
                        if count_10000 >= t10000:
                                
                            if u.total_height >= 20000:
                                u.total_height += h
                                u.save()
                            else:
                                diff = 19999 - u.total_height
                                h = random.randint(1,diff/40+1)
                                if u.total_height + h < 19999:
                                    u.total_height += h
                                    u.save()
                        else:
                            u.total_height += h
                            u.save()
                    else:
                        diff = 14999 - u.total_height
                        h = random.randint(1,diff/40+1)
                        if u.total_height + h < 14999:
                            u.total_height += h
                            u.save()
                else:
                    #说明不是二等奖种子选手
                    diff = 19999 - u.total_height
                    h = random.randint(1,diff/40+1)
                    if u.total_height + h < 19999:
                        u.total_height += h
                        u.save()
            else:
                #说明不是种子选手
                diff = 9999 - u.total_height
                h = random.randint(1,diff/40+1)
                #永远吹不破5000
                if u.total_height + h < 9999:
                    u.total_height += h
                    u.save()
        else:
            count_8000 = User.objects.filter(total_height__gt=15000).count()
            if count_8000 >= t8000:
                if u.total_height >= 15000:
                    count_10000 = User.objects.filter(total_height__gt=20000).count()
                    if count_10000 >= t10000:
                                
                        if u.total_height >= 20000:
                            u.total_height += h
                            u.save()
                        else:
                            diff = 19999 - u.total_height
                            h = random.randint(1,diff/40+1)
                            if u.total_height + h < 19999:
                                u.total_height += h
                                u.save()
                    else:
                        u.total_height += h
                        u.save()
                else:
                    #说明不是二等奖种子选手
                    diff = 14999 - u.total_height
                    h = random.randint(1,diff/40+1)
                    if u.total_height + h < 14999:
                        u.total_height += h
                        u.save()
            else:
                count_10000 = User.objects.filter(total_height__gt=20000).count()
                if count_10000 >= t10000:
                    if u.total_height >= 20000:
                        u.total_height += h
                        u.save()
                    else:
                        diff = 19999 - u.total_height
                        h = random.randint(1,diff/40+1)
                        if u.total_height + h < 19999:
                            u.total_height += h
                            u.save()
                else:
                    u.total_height += h
                    u.save()
        #help = Help(openid=request.session['openid'],toopenid=request.GET['openid'],dateline=time.time(),height=h)
        #help.save()
        if request.GET['openid'] == request.session['openid']:
            u = User.objects.get(openid=request.session['openid'])
            if u.times:
                u.total_height -= u.times
            u.times = h
            if not u.shared :
                u.save()
        else:
            um = User.objects.get(openid=request.session['openid'])
            help = Help(openid=request.session['openid'],toopenid=request.GET['openid'],dateline=time.time(),height=h,user_id=um.id)
            help.save()
        json = {
            "status":"success",
            "reason":"",
            "message":{
                "height":h,
                "total_height":u.total_height
            }
        }
    except Exception,e:
        json = {
            "status":"fail",
            "reason":str(e),
            "message": {}
        }
    return JsonResponse(json)
@need_login
def mobile(request):
    if request.GET.get("mobile",False):
        if len(request.GET.get("mobile")) != 11:
            
            return JsonResponse({
                "status":"fail",
                "reason":"mobile format wrong",
                "message": {}
            })
        else:
            u = User.objects.get(openid=request.session['openid'])
            u.phone = request.GET['mobile']
            u.save()
            return JsonResponse({
                "status":"success",
                "reason":"",
                "message":{}
            })
    else:
        return JsonResponse({
            "status":"fail",
            "reason":"no mobile message",
            "message":{}
        })
def rank(request):
    fetch = 10
    offset = 0
    if request.GET.get('fetch',False):
        fetch = request.GET['fetch']
    if request.GET.get('offset',False):
        offset = request.GET['offset']
    try:
        u = User.objects.order_by("-total_height")[offset:int(offset)+int(fetch)]
        res = []
        for i in u:
            a = {"id":i.id,"openid":i.openid,"nickname":i.nickname,"headimgurl":i.headimgurl,"phone":i.phone,"times":i.times,"total_height":i.total_height}
            res.append(a)
        return JsonResponse({
            "status":"success",
            "reason":"",
            "message":res
        })
    except Exception,e:
        return JsonResponse({
            "status":"fail",
            "reason":str(e),
            "message":{}
        })
        
def help_or_not(request):
    if request.session.get('openid',False) and request.GET.get('openid',False):
        if request.session['openid'] == request.GET['openid']:
            return JsonResponse({
                "status":"success",
                "reason":"",
                "message":{
                    "help":"me"
                }
            })
        else:
            return JsonResponse({
                "status":"success",
                "reason":"",
                "message":{
                    "help":"others"
                }
            })
    else:
        if request.session.get('openid',False):
            return JsonResponse({
                "status":"fail",
                "reason":"need login",
                "message":{}
            })
        else:
            return JsonReponse({
                "status":"fail",
                "reason":"can't get openid",
                "message":{}
            })
def wxconfig(request):
	url = request.POST['url']
	js_ticket = Wx.objects.get(id=1).js_ticket
	s = sign(js_ticket,url)
	json = {
		"appId":appid,
		"timestamp":s['timestamp'],
		"nonceStr":'nameLR9969',
		"signature":s['hash'],
		"jsApiList":['onMenuShareAppMessage','onMenuShareTimeline']
	}
	return JsonResponse(json)
def get_small_help_big(request):
    try:
        h = Help.objects.get(openid=request.GET['openid_small'],toopenid=request.GET['openid_big'])
        u = User.objects.get(openid=request.GET['openid_big'])
        return JsonResponse({
            "status":"success",
            "reason":"",
            "message":{
                "height":h.height,
                "total_height":u.total_height
            }
        })
    except Exception,e:
        return JsonResponse({
            "status":"fail",
            "reason":str(e),
            "message":{}
        })
def get_help_message(request):
    try:
        h = Help.objects.filter(toopenid=request.GET['openid']).order_by("-dateline")[0:20]
        help = []
        for i in h:
            a = {
                "openid" : i.openid,
                "nickname": i.user.nickname,
                "height":i.height
            }
            help.append(a)
        if help:
            return JsonResponse({
                "status":"success",
                "reason":"",
                "message":{
                    "help_message":help
                }
            })
        else:
            return JsonResponse({
                "status":"fail",
                "reason":"no one helps",
                "message":{}
            })
    except Exception,e:
        return JsonResponse({
            "status":"fail",
            "reason":str(e),
            "message":{}
        })
def get_height(request):
    try:
        u = User.objects.get(openid=request.GET['openid'])
        
        return JsonResponse({
            "status":"success",
            "reason":"",
            "message":{
                "height":u.total_height,
                "nickname":u.nickname,
                "openid":u.openid
            }
        })
    except Exception,e:
        return JsonResponse({
            "status":"fail",
            "reason":"no such user",
            "message":{}
        })
def update_access_token(request):
	get_js_ticket(get_access_token(appid,secret),appid,secret)
	return JsonResponse({
		"status":"success"
	})
def has_phone(request):
    u = User.objects.get(openid=request.session['openid'])
    if u.phone:
        return JsonResponse({
            "status":"success",
            "reason":"",
            "message":{}
        })
    else:
        return JsonResponse({
            "status":"fail",
            "reason":"no phone",
            "message":{}
        })
