# -*- coding: utf-8 -*-
# Django settings for lfs development buildout.

import os, sys
DIRNAME = os.path.dirname(__file__)

at_project_root = lambda name: os.path.join(DIRNAME, name)
sys.path.insert(0, DIRNAME)
for app_lookup_path in ('contrib', 'apps'):
    sys.path.insert(0, at_project_root(app_lookup_path))

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DIRNAME+'',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Yekaterinburg'
DATE_FORMAT = 'j.m.Y'
TIME_FORMAT = 'G:i'
FIRST_DAY_OF_WEEK = 1


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(DIRNAME, 'apps', 'student', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/assets/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+0zsw5n@v7*rhl6r6ufqhoc6jlqq0f-u8c+gh(hjb+_jmg@rh6'

# List of callables that know how to import templates from various sources.
#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.load_template_source',
#    'django.template.loaders.app_directories.load_template_source',
#)
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(DIRNAME, 'apps', "student", "templates"),
)

INSTALLED_APPS = (

    # admin tools
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    # contrib
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'django.contrib.redirects',

    # main
    'technics4me',

)

FORCE_SCRIPT_NAME = ""
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/personal/contacts/"

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.contrib.auth.context_processors.auth',
)

AUTHENTICATION_BACKENDS = (
    #'lfs.customer.auth.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# For sql_queries
INTERNAL_IPS = (
    "127.0.0.1",
)

TINYMCE_DEFAULT_CONFIG = {
  'mode': 'none',
  'theme': 'advanced',
  'language': 'ru',
  'convert_urls' : False,
  'theme_advanced_toolbar_location': 'top',
  'theme_advanced_toolbar_align' : 'center',
  'plugins': 'fullscreen, images, paste, advlist, searchreplace, table',
  'theme_advanced_buttons2_add' : 'separator, images',
  'theme_advanced_buttons3_add' : 'separator, fullscreen, separator, pastetext, pasteword, separator, search,replace',
  'theme_advanced_buttons4' : 'tablecontrols',
}


CACHE_BACKEND = 'dummy:///'
#CACHE_BACKEND = 'locmem:///'

SESSION_COOKIE_AGE = 86400 * 30 # 30 days


EMAIL_HOST = ""
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""


AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'tech4me@mail.ru'

EMAIL_BACKEND = 'mailer.backend.DbBackend'

STATIC_URL = MEDIA_URL

try:
    from settings_local import *
except ImportError:
    pass
