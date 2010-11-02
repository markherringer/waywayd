from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list

urlpatterns = patterns('attractions.views',
    url(r'^$', view='area_list', name="area_list"),
    url(r'^tag/(?P<tag>[-\w]+)/area/(?P<featured_area>[-\w]+)/$', view='attractions_for', name='attractions_for'),
    url(r'^tag/(?P<tag>[-\w]+)/$', view='attractions_for', name='attractions_for'),
    url(r'^tag/lang/(?P<lang>[\w]+)/area/(?P<featured_area>[-\w]+)/$', view='tag_search', name='tag_search'),
    url(r'^tag/lang/(?P<lang>[\w]+)/$', view='tag_search', name='tag_search'),
    url(r'^detail/(?P<slug>[-\w]+)/$', view='attr_detail', name='attr_detail'),
    url(r'^hotel/(?P<slug>[-\w]+)/$', view='hotel_detail', name='hotel_detail'),
    url(r'^regions/$', view='area_list', name='area_list'),
    url(r'^regions/(?P<slug>[-\w]+)/$', view='area_detail', name='area_detail'),
    url(r'^attraction/(?P<slug>[-\w]+)/vcard/$', 'vcard', {'model_name': 'Attraction',}, name='attr_vcard'),
    url(r'^hotel/(?P<slug>[-\w]+)/vcard/$', 'vcard', {'model_name': 'Hotel',}, name='hotel_vcard'),
    url(r'^ajax/tag_search/(?P<lang>[\w]+)/$', view='ajax_tag', name='ajax_tag'),
    url(r'^ajax/tag_search/(?P<lang>[\w]+)/(?P<slug>[-\w]+)/$', view='ajax_tag', name='ajax_tag'),
)
