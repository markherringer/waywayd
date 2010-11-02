from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from account.openid_consumer import PinaxConsumer

#handler500 = "pinax.views.server_error"

if settings.ACCOUNT_OPEN_SIGNUP:
    signup_view = "account.views.signup"
else:
    signup_view = "signup_codes.views.signup"

from django.contrib.sitemaps import Sitemap
from attractions.models import Area, Attraction
from tagging.models import Tag


class AreaSitemap(Sitemap):
    #changefreq = "never"
    #priority = 0.5

    def items(self):
        return Area.objects.filter(featured=True)

class TagMap(Sitemap):

    def items(self):
        return Tag.objects.all()

    def location(self, obj):
        return '/attractions/tag/%s/' % obj.name

class TagAndAreaMap(Sitemap):

    def items(self):
        strings = [ t.name for t in Tag.objects.all() ]
        together = []
        for t in strings:
            for a in Area.objects.filter(featured=True):
                together.append('%s|%s' % (t, a.slug))

        return together

    def location(self, obj):
        return '/attractions/tag/%s/area/%s/' % (obj.split('|')[0], obj.split('|')[1])

sitemaps = {'areas': AreaSitemap, 'tags': TagMap, 'tags_and_areas': TagAndAreaMap}

urlpatterns = patterns("",
    url(r"^$", "attractions.views.area_list", name="home"),
    
    url(r"^admin/invite_user/$", "signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^account/signup/$", signup_view, name="acct_signup"),
    
    (r"^attractions/", include("attractions.urls")),
    (r"^(?P<lang>[-\w].*)/attractions/", include("attractions.urls")),
    (r"^about/", include("about.urls")),
    (r"^account/", include("account.urls")),
    (r"^openid/(.*)", PinaxConsumer()),
    (r"^profiles/", include("basic_profiles.urls")),
    (r"^notices/", include("notification.urls")),
    (r"^announcements/", include("announcements.urls")),
    (r'^i18n/setlang/', 'views.setlang'),
    #(r'^i18n/', include('django.conf.urls.i18n')),
    (r"^admin/", include(admin.site.urls)),
    #(r'^en/sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    #(r'^it/sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^feedback-form/$', view='views.feedback_form'),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
            (r'^site_media/', include('staticfiles.urls')),
    )
