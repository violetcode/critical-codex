import sys
import os
import platform
import djcelery

djcelery.setup_loader()

from django.contrib.messages import constants as messages

# ===========================
# = Directory Declaractions =
# ===========================

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

CURRENT_DIR   = os.path.dirname(__file__)
TEMPLATE_DIRS = os.path.join(CURRENT_DIR, 'templates')
UTILS_ROOT    = os.path.join(CURRENT_DIR, 'utils')
APPS_ROOT    = os.path.join(CURRENT_DIR, 'apps')
VENDOR_ROOT   = os.path.join(CURRENT_DIR, 'vendor')

if '/utils' not in ' '.join(sys.path):
    sys.path.append(UTILS_ROOT)

if '/vendor' not in ' '.join(sys.path):
    sys.path.append(VENDOR_ROOT)

if '/apps' not in ' '.join(sys.path):
    sys.path.append(APPS_ROOT)


DEBUG = True
PRODUCTION = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
	'criticalcodex.com',
    '*.criticalcodex.com',
	'criticalcodex.herokuapp.com',
]

ADMINS = (('Tyler Rilling', 'tyler@underlost.net'))
MANAGERS = ADMINS

#DB info injected by Heroku
import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}


#Cache
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    import urlparse
    redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
    CACHES = {
            'default': {
            'BACKEND': 'd20.vendor.johnny.backends.redis.RedisCache',
            'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
            'OPTIONS': {
            'PASSWORD': redis_url.password,
            'DB': 0,
            'JOHNNY_CACHE': True,
        }
      }
    }

JOHNNY_MIDDLEWARE_KEY_PREFIX='d20'
JOHNNY_MIDDLEWARE_SECONDS = 900
CACHE_MIDDLEWARE_SECONDS = 60 * 5 # 5 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'd20'

#Email
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
POSTMARK_API_KEY = os.environ.get('POSTMARK_API_KEY')
POSTMARK_SENDER = 'site@criticalcodex.com'
EMAIL_HOST = os.environ.get('POSTMARK_SMTP_SERVER')
SERVER_EMAIL = 'site@criticalcodex.com'
DEFAULT_FROM_EMAIL = "site@criticalcodex.com"

TIME_ZONE = 'US/Pacific'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
AUTH_USER_MODEL = 'core.Account'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
ALLOW_NEW_REGISTRATIONS = False
STATICFILES_DIRS = ( os.path.join(SITE_ROOT, 'static'),)
WSGI_APPLICATION = 'd20.wsgi.application'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
MIXPANEL_TOKEN = os.environ.get('MIXPANEL_TOKEN')

if DEBUG:
	STATIC_ROOT = os.path.join(CURRENT_DIR, 'static')
	STATIC_URL = 'http://criticalcodex.com/static/'
	MEDIA_URL = 'http://criticalcodex.com/static/media/'
else:
	STATIC_ROOT = 'staticfiles'
	STATIC_URL = 'http://static.criticalcodex.com/'
	MEDIA_URL = 'http://static.criticalcodex.com/media/'

#Site Settings
ALLOW_NEW_REGISTRATIONS = False
COMMENTS_APP = 'd20.apps.threadedcomments'
SITE_NAME = 'CriticalCodex'
SITE_DESC = 'A web-based application designed to enhance your tabletop RPG adventuring and storytelling.'
SITE_URL = 'http://criticalcodex.com/'

#Stripe
if DEBUG:
	STRIPE_SECRET = "WTg4xZZsbgX5oHYX8P8Ywk4jDqM3XXMP"
	STRIPE_PUBLISHABLE = "pk_YhTPLj7IIvaPzHRqDOCRMHkJfHeWj"
else:
	STRIPE_SECRET = os.environ.get('STRIPE_SECRET_KEY')
	STRIPE_PUBLISHABLE = os.environ.get('STRIPE_PUBLISHABLE_KEY')

ZEBRA_ENABLE_APP = True

#Amazon S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = 'static.criticalcodex.com'
AWS_S3_CUSTOM_DOMAIN = 'static.criticalcodex.com'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_SECURE_URLS = False
COMPRESS_URL = "http://static.criticalcodex.com/"
COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

REST_FRAMEWORK = {
    'PAGINATE_BY': 25,                 # Default to 25
    'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100             # Maximum limit allowed when using `?page_size=xxx`.
}


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = {
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'django.core.context_processors.tz',
	'django.contrib.messages.context_processors.messages',
	'django.core.context_processors.request',
	'd20.apps.core.context_processors.template_settings',
}

MIDDLEWARE_CLASSES = (
	'd20.apps.core.middleware.SubdomainMiddleware',
	'd20.apps.core.middleware.MultipleProxyMiddleware',
    'd20.apps.core.middleware.SetRemoteAddrFromForwardedFor',
	'd20.vendor.johnny.middleware.LocalStoreClearMiddleware',
	'd20.vendor.johnny.middleware.QueryCacheMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'd20.apps.core.middleware.TimingMiddleware',
	'd20.apps.core.middleware.LastSeenMiddleware',
)

ROOT_URLCONF = 'd20.urls'

SUBDOMAIN_URLCONFS = {
	None: 'd20.urls',
    'api': 'd20.apps.api.urls',
}

SESSION_COOKIE_DOMAIN = '.criticalcodex.com'

TEMPLATE_DIRS = (
	os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (

	#Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.humanize',

    #Prancing on Heroku
    'djcelery',
    'gunicorn',
    'taggit',
    'haystack',
    'compressor',
    'storages',
    'rest_framework',

    #Vendor
    'zebra',

    #Internal
    'd20.apps.core',
    'd20.apps.profile',
    'd20.apps.charactersheet',
    'd20.apps.resources',

)

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': os.environ['SEARCHBOX_URL'],
        'INDEX_NAME': 'charactersheets',
        },
    }


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}
