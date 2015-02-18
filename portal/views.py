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
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# Create your views here.
logger = logging.getLogger(__name__)
appid = "wx91e4c1925de9ff50"
secret = "f2f564ea79ff43f7ed3004821ac3b2b8"

def login(request):
	return render(request,"login.html")

def index(request):
    #if help other
    mod = "self"
    #and not myself
    try:
        request.GET['openid']
        mod = "help"
        if request.GET['openid'] == request.session['openid']:
            mod = 'self'
        print mod
    except Exception,e:
        print e
        mod = "self"
    if mod == "self":
        try:
            request.GET['code']
        except Exception,e:
            return HttpResponseRedirect("/nabob/login/")
        try:
            request.session['openid']
        except Exception,e:
            p = wx_login(appid,secret,request.GET['code'])
            request.session['openid'] = p['openid']
            request.session['headimgurl'] = p['headimgurl'].encode("utf8")
            request.session['nickname'] = p['nickname'].encode("utf8")
            request.session['code'] = request.GET['code']
            try:
                u = User.objects.get(openid=request.session['openid'])
                u.openid = request.session['openid']
                u.headimgurl = request.session['headimgurl']
                u.nickname = request.session['nickname']
                u.code = request.session['code']
                u.dateline = datetime.datetime.now().strftime("%Y-%m-%d") 
                u.save()
            except Exception,e:
                u = User(openid=request.session['openid'],headimgurl=request.session['headimgurl'],nickname=request.session['nickname'],pos=0,code=request.session['code'],times=0,dateline=datetime.datetime.now().strftime("%Y-%m-%d"))
                u.save()
    elif mod == "help":
        try:
            request.GET['code']
            p = wx_login(appid,secret,request.GET['code'])
            request.session['openid'] = p['openid']
            request.session['headimgurl'] = p['headimgurl'].encode("utf8")
            request.session['nickname'] = p['nickname'].encode("utf8")
            request.session['code'] = request.GET['code']
            try:
                request.session['openid']
            except Exception,e:
                return HttpResponseRedirect("/nabob/login/?openid="+request.GET['openid'])
        except Exception,e :
            return HttpResponseRedirect("/nabob/login/?openid="+request.GET['openid'])
    has_phone = "true"
    try:
        b = Bonus.objects.get(openid=request.session['openid'])
        if b.phone:
            has_phone = "true"
        else:
            has_phone = "false"
    except Exception,e:
        has_phone = "false"
    pos = 0
    if mod == 'self':
        u = User.objects.get(openid=request.session['openid'])
        pos = u.pos
    else:
        u = User.objects.get(openid=request.GET['openid'])
        pos = u.pos
    return render(request,"index.html",{
        "mod":mod,
        "has_phone":has_phone,
        "pos":pos
    })
def openid(request):
    return JsonResponse({
        "openid":request.session['openid']    
    })

def move(request):
    l20 = [1,3,7,9,13]
    l100 = [2,8,14]
    lapp100 = [4,11]
    l0 = [6,12]
    l200 = [5]
    ran = random.randint(0,100)
    prize = 1
    if ran < 45:
        prize = 1
        r = random.randint(0,4)
        pos = l20[r]
    elif ran >= 45 and ran < 65:
        prize = 2
        r = random.randint(0,2)
        pos = l100[r]
    elif ran >= 65 and ran < 85:
        prize = 3
        r = random.randint(0,1)
        pos = lapp100[r]
    elif ran >= 85 and ran < 95:
        prize = 4
        r = random.randint(0,1)
        pos = l0[r]
    else:
        prize = 5
        pos = 5
    openid = request.session['openid']
    try:
        openid = request.GET['openid']
    except Exception,e:
        print e
        openid = request.session['openid']
     
    u = User.objects.get(openid=openid)
    u.pos = pos
    u.save()
    return JsonResponse({
        "move":pos,
        "prize":prize
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
	print json
	return JsonResponse(json)
def update_access_token(request):
	get_js_ticket(get_access_token(appid,secret),appid,secret)
	return JsonResponse({
		"status":"success"
	})
def sendmsg(request):
    code = random.randint(100000,999999);
    try:
        c = Code.objects.filter(openid=request.session['openid']).order_by("-dateline")[0]
        if int(c.dateline) + 100 < int(time.time()):
            r = requests.get("http://www.360youtu.com/uwp/web/sms/send.jsp?tel="+request.GET['phone'].strip()+"&content="+str(code)+"。用该密码登录爱学贷官网查收压岁券，并及时修改登录密码")
            c = Code(openid=request.session['openid'],dateline=str(int(time.time())),code=str(code),phone=request.GET['phone'],used="0")
            c.save()
    except Exception,e:
        print e
        r = requests.get("http://www.360youtu.com/uwp/web/sms/send.jsp?tel="+request.GET['phone'].strip()+"&content="+str(code)+"。用该密码登录爱学贷官网查收压岁券，并及时修改登录密码")
        try:
            c = Code(openid=request.session['openid'],dateline=str(int(time.time())),code=str(code),phone=request.GET['phone'],used="0")
            c.save()
        except Exception,e:
            print e
    return JsonResponse({
        "status":"success"
    })
def getChance(request):
    try:
        u = User.objects.get(openid=request.session['openid'])
        if str(u.dateline) != str(datetime.datetime.now().strftime("%Y-%m-%d")):
            u.times = 0
            u.dateline = datetime.datetime.now().strftime("%Y-%m-%d")
        u.save()
        return JsonResponse({
            "num":3-u.times
        })
    except Exception,e:
        print e
        return JsonResponse({
            "num":3
        })
def bonus_or_not(request):
    try:
        b = Bonus.objects.get(openid=request.session['openid'])
        return JsonResponse({
            "status":"true"
        })
    except Exception,e:
        print e
        return JsonResponse({
            "status":"false"    
        })
def help_or_not(request):
    try:
        h = Help.objects.get(openid=request.session['openid'],toopenid=request.GET['openid'])
        return JsonResponse({
            "status":"true"
            })
    except Exception,e:
        print e
        return JsonResponse({
            "status":"false"
            })
def commit_prize(request):
    try:
        #可能为别人领取
        b = Bonus.objects.get(openid=request.GET['openid'])
        #检测领没领过
        #使用GET获取说明是别人
        #先更新help表
        #尝试看表里有没有，没有更新，有则无操作
        if request.session['openid'] != request.GET['openid']:
            try:
                h = Help.objects.get(openid=request.session['openid'],toopenid=request.GET['openid'])
                return JsonResponse({
                    "status":"help failed",
                })
            except Exception,e:
                h = Help(openid=request.session['openid'],toopenid=request.GET['openid'],prize=request.GET['type']+str(request.GET['num']),dateline=datetime.datetime.now().strftime("%Y-%m-%d"))
                h.save()
                b = Bonus.objects.get(openid=request.GET['openid'])
                b.help_count += 1
                b.save()
                conpontype = 'axdyasui'
                if request.GET['type'] == 'ticket':
                    coupontype = 'axdyasui'
                elif request.GET['type'] == 'apple':
                    coupontype = 'appleyasui'
                elif request.GET['type'] == 'iphone':
                    coupontype = 'iphone5md'
                money = 0
                total_money = 0
                apple_money = 0
                iphone = 0
                if request.GET['type'] == 'ticket': 
                    total_money = request.GET['num']
                elif request.GET['type'] == 'apple':
                    apple_money = request.GET['num']
                else:
                    iphone = request.GET['num']
                if total_money:
                    money = total_money
                elif apple_money:
                    money = apple_money
                r = requests.post("http://121.40.57.243:20000/sale_t/newyear/coupon",{"telphone":str(b.phone),"password":"","regip":"119.29.66.37","money":str(money),"coupontype":coupontype})
                print r.json()
                return JsonResponse({
                    "status":"help success",
                    "prize":request.GET['prize']
                })
    except Exception,e:
        print e
        total_money = 0
        apple_money = 0
        iphone = 0
        if request.GET['type'] == 'ticket': 
            total_money = request.GET['num']
        elif request.GET['type'] == 'apple':
            apple_money = request.GET['num']
        else:
            iphone = request.GET['num']
        try:
            u = User.objects.get(openid=request.session['openid'])
            b = Bonus.objects.get(openid=request.session['openid'])
            if u.times <= 3:    
                b.total_money += int(total_money)
                b.apple_money += int(apple_money)
                b.iphone = iphone
                b.dateline = datetime.datetime.now().strftime("%Y-%m-%d")
                b.save()
                conpontype = 'axdyasui'
                if request.GET['type'] == 'ticket':
                    coupontype = 'axdyasui'
                elif request.GET['type'] == 'apple':
                    coupontype = 'appleyasui'
                elif request.GET['type'] == 'iphone':
                    coupontype = 'iphone5md'
                money = 0
                if total_money:
                    money = total_money
                elif apple_money:
                    money = apple_money
                r = requests.post("http://121.40.57.243:20000 /sale_t/newyear/coupon",{"telphone":str(b.phone),"password":"","regip":"119.29.66.37","money":str(money),"coupontype":coupontype})
                print r.json()
                return JsonResponse({
                    "status":"self success",
                    "prize":request.GET['prize']
                })
            else:
                return JsonResponse({
                    "status":"self failed",
                    "prize":request.GET['prize']
                })

        except Exception,e:
            print e
            b = Bonus(openid=request.session['openid'],dateline=datetime.datetime.now().strftime("%Y-%m-%d"),total_money=total_money,apple_money=apple_money,iphone=iphone,times=1)
            b.save()
            
            conpontype = 'axdyasui'
            if request.GET['type'] == 'ticket':
                coupontype = 'axdyasui'
            elif request.GET['type'] == 'apple':
                coupontype = 'appleyasui'
            elif request.GET['type'] == 'iphone':
                coupontype = 'iphone5md'
            money = 0
            if total_money:
                money = total_money
            elif apple_money:
                money = apple_money
            r = requests.post("http://121.40.57.243:20000 /sale_t/newyear/coupon",{"telphone":str(b.phone),"password":"","regip":"119.29.66.37","money":str(money),"coupontype":coupontype})
            print r.json()
            return JsonResponse({
                "status":"self success",
                "reason":"insert new message"
            })
def checkcode(request):
    c = Code.objects.filter(openid=request.session['openid']).order_by("-id")[0]
    if c.code == request.GET['vcode']:
        c.used = 1
        c.save()
        u = User.objects.get(openid=request.session['openid'])
        u.phone = request.GET['phone']
        u.save()
        try:
            #可能为别人领取
            b = Bonus.objects.get(openid=request.GET['openid'])
            #检测领没领过
            #使用GET获取说明是别人
            #先更新help表
            #尝试看表里有没有，没有更新，有则无操作
            if request.session['openid'] != request.GET['openid']:
                try:
                    h = Help.objects.get(openid=request.session['openid'],toopenid=request.GET['openid'])
                    return JsonResponse({
                        "status":"help failed",
                    })
                except Exception,e:
                    h = Help(openid=request.session['openid'],toopenid=request.GET['openid'],prize=request.GET['type']+str(request.GET['num']),dateline=datetime.datetime.now().strftime("%Y-%m-%d"))
                    h.save()
                    return JsonResponse({
                        "status":"help success",
                        "prize":request.GET['prize']
                    })
        except Exception,e:
            print e
            total_money = 0
            apple_money = 0
            iphone = 0
            if request.GET['type'] == 'ticket': 
                total_money = request.GET['num']
            elif request.GET['type'] == 'apple':
                apple_money = request.GET['num']
            else:
                iphone = request.GET['num']
            try:
                u = Bonus.objects.get(openid=request.session['openid'])
                b = Bonus.objects.get(openid=request.session['openid'])
                if u.times <= 3:    
                    b.total_money += int(total_money)
                    b.apple_money += int(apple_money)
                    b.iphone = iphone
                    b.dateline = datetime.datetime.now().strftime("%Y-%m-%d")
                    b.phone = request.GET['phone']
                    b.save()
                    conpontype = 'axdyasui'
                    if request.GET['type'] == 'ticket':
                        coupontype = 'axdyasui'
                    elif request.GET['type'] == 'apple':
                        coupontype = 'appleyasui'
                    elif request.GET['type'] == 'iphone':
                        coupontype = 'iphone5md'
                    money = 0
                    if total_money:
                        money = total_money
                    elif apple_money:
                        money = apple_money
                    r = requests.post("http://121.40.57.243:20000/sale_t/newyear/coupon",{"telphone":str(b.phone),"password":request.GET['vcode'],"regip":"119.29.66.37","money":str(money),"coupontype":coupontype})
                    print r.json()
                    return JsonResponse({
                        "status":"self success",
                        "prize":request.GET['prize']
                    })
                else:
                    return JsonResponse({
                        "status":"self failed",
                        "prize":request.GET['prize']
                    })

            except Exception,e:
                print e
                b = Bonus(openid=request.session['openid'],phone=request.GET['phone'],dateline=datetime.datetime.now().strftime("%Y-%m-%d"),total_money=total_money,apple_money=apple_money,iphone=iphone,times=1,help_count=0,user_id=u.id)
                b.save()
                conpontype = 'axdyasui'
                if request.GET['type'] == 'ticket':
                    coupontype = 'axdyasui'
                elif request.GET['type'] == 'apple':
                    coupontype = 'appleyasui'
                elif request.GET['type'] == 'iphone':
                    coupontype = 'iphone5md'
                money = 0
                if total_money:
                    money = total_money
                elif apple_money:
                    money = apple_money
                r = requests.post("http://121.40.57.243:20000/sale_t/newyear/coupon",{"telphone":str(b.phone),"password":request.GET['vcode'],"regip":"119.29.66.37","money":str(money),"coupontype":coupontype})
                print r.json()
                return JsonResponse({
                    "status":"self success",
                    "reason":"insert new message"
                })
    else:
        return JsonResponse({
            "status":"error",
            "reason":"vcode wrong"
        })

def num_plus(request):
    try:
        u = User.objects.get(openid = request.session['openid'])
        u.times += 1
        u.save()
        print u.times
        return JsonResponse({
            "times":u.times
        })
    except Exception,e:
        return JsonResponse({
            "status":"error"
        })
def first_title(request):
    try:
        b = Bonus.objects.get(openid=request.session['openid'])
        bo = Bonus.objects.order_by("-help_count")
        cnt = 0
        rank = 0
        for i in bo:
            cnt += 1
            if i.openid == request.session['openid']:
                rank = cnt
                break
        return JsonResponse({
            "total":b.total_money,
            "help_count":b.help_count,
            "rank":rank
        })
    except Exception,e:
        print e
        return JsonResponse({
            "total":0,
            "help_count":0,
            "rank":0
        })
def rank(request):
    b = Bonus.objects.order_by("-help_count")[0:100]
    prize = []

    for i in b:
        a = {"openid":i.openid,"phone":i.phone,"power":i.help_count,"headimgurl":i.user.headimgurl,"nickname":i.user.nickname}
        prize.append(a) 
    return JsonResponse({
        "status":"success",
        "rank":prize
    })
