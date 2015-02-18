from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mam_beautiful.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^nabob/index/', 'portal.views.index'),
	url(r'^nabob/bonus/', 'portal.views.bonus'),
	url(r'^nabob/login/', 'portal.views.login'),
	url(r'^nabob/edit/', 'portal.views.edit'),
	url(r'^nabob/wxconfig/','portal.views.wxconfig'),
	url(r'^nabob/update_access_token/','portal.views.update_access_token'),
	url(r'^nabob/move/','portal.views.move'),
    url(r'^nabob/sendmsg/','portal.views.sendmsg'),
    url(r'^nabob/openid/','portal.views.openid'),
    url(r'^nabob/checkcode/','portal.views.checkcode'),
    url(r'^nabob/prize/','portal.views.prize'),
    url(r'^nabob/commit_prize/','portal.views.commit_prize'),
    url(r'^nabob/rank/','portal.views.rank'),
    url(r'^nabob/first_title/','portal.views.first_title'),
    url(r'^nabob/bonus_or_not/','portal.views.bonus_or_not'),
    url(r'^nabob/help_or_not/','portal.views.help_or_not'),
    url(r'^nabob/num_plus/','portal.views.num_plus'),
    url(r'^nabob/getChance/','portal.views.getChance')
)
