from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mam_beautiful.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^index/', 'portal.views.index'),
	url(r'^bonus/', 'portal.views.bonus'),
	url(r'^login/', 'portal.views.login'),
	url(r'^edit/', 'portal.views.edit'),
	url(r'^wxconfig/','portal.views.wxconfig'),
	url(r'^update_access_token/','portal.views.update_access_token'),
	url(r'^click/','portal.views.click'),
)
