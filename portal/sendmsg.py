#coding:utf8
import random
import json
import requests
from models import *
import logging
import time
import hashlib
import urllib
logger = logging.getLogger(__name__)
def sendMsg(phone):
    ran = random.randint(100000,999999)
    msg = u"http://service.winic.org:8009/sys_port/gateway/vipsms.asp?id=360youtu&pwd=zxbt20111212&to="+phone+"&content="+str(ran)+"&time="+str(int(time.time()))
    return ran
