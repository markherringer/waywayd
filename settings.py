# -*- coding: utf-8 -*-
# Django settings for basic pinax project.

import os.path
import posixpath
import pinax

PINAX_ROOT = os.path.abspath(os.path.dirname(pinax.__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# tells Pinax to use the default theme
PINAX_THEME = "default"

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

INTERNAL_IPS = [
    "127.0.0.1",
]

ADMINS = [
    # ("Your Name", "your_email@domain.com"),
]

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "US/Eastern"

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = "en"

USE_I18N = True
ugettext = lambda s: s
LANGUAGES = (
    ('en', u'English'),
    ('it', u'Italiano'),
)
CMS_LANGUAGES = LANGUAGES

# Make English the default language
DEFAULT_LANGUAGE = 1

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'media')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/site_media/media/'

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'static')

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = '/site_media/static/'

# Additional directories which hold static files
STATICFILES_DIRS = (
    ('basic071', os.path.join(PROJECT_ROOT, 'media')),
    ('pinax', os.path.join(PINAX_ROOT, 'media', PINAX_THEME)),
)

ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# 1.2
#MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media")
#MEDIA_URL = "/site_media/media/"
OLWIDGET_MEDIA_URL = "/site_media/static/olwidget/"
#STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")
#STATIC_URL = "/site_media/static/"
#STATICFILES_DIRS = [
#    os.path.join(PROJECT_ROOT, "media"),
#    os.path.join(PINAX_ROOT, "media", PINAX_THEME),
#]
#ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Make this unique, and don"t share it with anybody.
SECRET_KEY = "wdsk$eseb7-11y_kb%r$j)%azk-0&l*v#q0$j0d2e%aqcna+l$"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.load_template_source",
    "django.template.loaders.app_directories.load_template_source",
]

MIDDLEWARE_CLASSES = [
    'django.middleware.cache.UpdateCacheMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    #"django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_openid.consumer.SessionConsumer",
    #"django.contrib.messages.middleware.MessageMiddleware",
    "middleware.LocaleMiddleware",
    "django.middleware.doc.XViewMiddleware",
    "pagination.middleware.PaginationMiddleware",
    "pinax.middleware.security.HideSensistiveFieldsMiddleware",
    'middleware.MultilingualURLMiddleware',
    'middleware.DefaultLanguageMiddleware',
    #"debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.cache.FetchFromCacheMiddleware',
    "flatpages.middleware.FlatpageFallbackMiddleware",
]

ROOT_URLCONF = "urls"

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
    os.path.join(PINAX_ROOT, "templates", PINAX_THEME),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    #"django.contrib.messages.context_processors.messages",
    
    "pinax.core.context_processors.pinax_settings",
    
    "notification.context_processors.notification",
    "announcements.context_processors.site_wide_announcements",
    "account.context_processors.openid",
    "account.context_processors.account",
    "multilingual.context_processors.multilingual",
]

INSTALLED_APPS = [
    # included
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    #"django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.gis",
    "django.contrib.sitemaps",
    "flatpages",
    "pinax.templatetags",
    
    # external
    "notification", # must be first
    "django_openid",
    "emailconfirmation",
    "mailer",
    "announcements",
    "pagination",
    "timezones",
    "ajax_validation",
    "uni_form",
    "staticfiles",
    #"debug_toolbar",
    #added to basic_project
    "django_extensions",
    "tagging",
    
    # internal (for now)
    "basic_profiles",
    "account",
    "signup_codes",
    "about",

    # non-pinax
    "rosetta",

    # ours
    "olwidget",
    "attractions",
    "django_extensions",
    "multilingual",
]

#MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/profile/%s/" % o.username,
}

MARKUP_FILTER_FALLBACK = "none"
MARKUP_CHOICES = [
    ("restructuredtext", u"reStructuredText"),
    ("textile", u"Textile"),
    ("markdown", u"Markdown"),
    ("creole", u"Creole"),
]
WIKI_MARKUP_CHOICES = MARKUP_CHOICES

AUTH_PROFILE_MODULE = "basic_profiles.Profile"
NOTIFICATION_LANGUAGE_MODULE = "account.Account"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = False

if ACCOUNT_EMAIL_AUTHENTICATION:
    AUTHENTICATION_BACKENDS = [
        "account.auth_backends.EmailModelBackend",
    ]
else:
    AUTHENTICATION_BACKENDS = [
        "django.contrib.auth.backends.ModelBackend",
    ]

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG
CONTACT_EMAIL = ""
SITE_NAME = ""
LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URLNAME = "what_next"

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}
LANGUAGE_HREF_IGNORES = ['sitemap']
# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass

FORCE_LOWERCASE_TAGS = True
#CACHE_BACKEND = "memcached://127.0.0.1:11211/"
#CACHE_MIDDLEWARE_SECONDS = 10000
#CACHE_MIDDLEWARE_KEY_PREFIX = 'cittadelcapo'
#CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

