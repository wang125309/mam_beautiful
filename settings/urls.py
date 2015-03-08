from django.conf.urls import patterns, include, url
from django.contrib import admin
address = 'blow_test'
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
	url(r'^'+address+'/index/', 'portal.views.index'),
    url(r'^'+address+'/wxconfig/','portal.views.wxconfig'),
    url(r'^'+address+'/login/','portal.views.login'),
    url(r'^'+address+'/update_access_token/','portal.views.update_access_token'),
    url(r'^'+address+'/add_height/','portal.views.add_height'),
    url(r'^'+address+'/rank/','portal.views.rank'),
    url(r'^'+address+'/mobile/','portal.views.mobile'),
    url(r'^'+address+'/can_play/','portal.views.can_play'),
    url(r'^'+address+'/get_height/','portal.views.get_height'),
    url(r'^'+address+'/get_help_message/','portal.views.get_help_message'),
    url(r'^'+address+'/get_small_help_big/','portal.views.get_small_help_big'),
    url(r'^'+address+'/enter/','portal.views.enter'),
    url(r'^'+address+'/has_phone/','portal.views.has_phone'),
    url(r'^'+address+'/help_or_not/','portal.views.help_or_not'),
)
