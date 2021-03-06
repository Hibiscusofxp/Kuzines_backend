import sys
import imp
from os.path import abspath, dirname, join, isfile


sys.path.insert(0, '../..')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_PATH = abspath(dirname(__file__))

ADMINS = (
    # ('Ben_Xu', 'hibiscusofxp@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # 'NAME': 'new_fb_login_v2',                      # Or path to database file if using sqlite3.
        'NAME': 'kuzines_db_v2',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',                      # Set to empty string for default.
     }
}

TIME_ZONE = 'America/Montevideo'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = '/Users/Ben/Documents/umich/kuzines/testimages'
MEDIA_URL = ''

STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '#$5btppqih8=%ae^#&amp;7en#kyi!vh%he9rg=ed#hm6fnw9^=umc'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'api.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'api.wsgi.application'

TEMPLATE_DIRS = (
    join(ROOT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    # 'social.apps.django_app.default',
    'api.app',
    'api.apiv1',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
)

AUTHENTICATION_BACKENDS = (
    # 'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.google.GooglePlusAuth',
    # 'social.backends.twitter.TwitterOAuth',
    # 'social.backends.yahoo.YahooOpenId',
    # 'social.backends.stripe.StripeOAuth2',
    # 'social.backends.persona.PersonaAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.facebook.FacebookAppOAuth2',
    # 'social.backends.yahoo.YahooOAuth',
    # 'social.backends.angel.AngelOAuth2',
    # 'social.backends.behance.BehanceOAuth2',
    # 'social.backends.bitbucket.BitbucketOAuth',
    # 'social.backends.box.BoxOAuth2',
    # 'social.backends.linkedin.LinkedinOAuth',
    # 'social.backends.linkedin.LinkedinOAuth2',
    # 'social.backends.github.GithubOAuth2',
    # 'social.backends.foursquare.FoursquareOAuth2',
    # 'social.backends.instagram.InstagramOAuth2',
    # 'social.backends.live.LiveOAuth2',
    # 'social.backends.vk.VKOAuth2',
    # 'social.backends.dailymotion.DailymotionOAuth2',
    # 'social.backends.disqus.DisqusOAuth2',
    # 'social.backends.dropbox.DropboxOAuth',
    # 'social.backends.evernote.EvernoteSandboxOAuth',
    # 'social.backends.fitbit.FitbitOAuth',
    # 'social.backends.flickr.FlickrOAuth',
    # 'social.backends.livejournal.LiveJournalOpenId',
    # 'social.backends.soundcloud.SoundcloudOAuth2',
    # 'social.backends.thisismyjam.ThisIsMyJamOAuth1',
    # 'social.backends.stocktwits.StocktwitsOAuth2',
    # 'social.backends.tripit.TripItOAuth',
    # 'social.backends.twilio.TwilioAuth',
    # 'social.backends.xing.XingOAuth',
    # 'social.backends.yandex.YandexOAuth2',
    # 'social.backends.douban.DoubanOAuth2',
    # 'social.backends.mixcloud.MixcloudOAuth2',
    # 'social.backends.rdio.RdioOAuth1',
    # 'social.backends.rdio.RdioOAuth2',
    # 'social.backends.yammer.YammerOAuth2',
    # 'social.backends.stackoverflow.StackoverflowOAuth2',
    # 'social.backends.readability.ReadabilityOAuth',
    # 'social.backends.skyrock.SkyrockOAuth',
    # 'social.backends.tumblr.TumblrOAuth',
    # 'social.backends.reddit.RedditOAuth2',
    # 'social.backends.steam.SteamOpenId',
    # 'social.backends.podio.PodioOAuth2',
    # 'social.backends.amazon.AmazonOAuth2',
    # 'social.backends.runkeeper.RunKeeperOAuth2',
    'social.backends.email.EmailAuth',
    'social.backends.username.UsernameAuth',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/app/done/'
# LOGIN_REDIRECT_URL = '/mylogin/'

URL_PATH = ''
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/userinfo.profile'
]
# SOCIAL_AUTH_EMAIL_FORM_URL = '/signup-email'
SOCIAL_AUTH_EMAIL_FORM_HTML = 'email_signup.html'
SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'api.app.mail.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/email-sent/'
# SOCIAL_AUTH_USERNAME_FORM_URL = '/signup-username'
SOCIAL_AUTH_USERNAME_FORM_HTML = 'username_signup.html'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'api.app.pipeline.require_email',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

try:
    from api.local_settings import *
except ImportError:
    pass
    
SOCIAL_AUTH_FACEBOOK_KEY ='587784734610029'
SOCIAL_AUTH_FACEBOOK_SECRET ='f1b4c38284384384657cc65c95b82d74'
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

if isfile(join(ROOT_PATH, "settings_production.py")):
    PRODUCTION_SETTINGS = imp.load_source("settings_production", join(ROOT_PATH, "settings_production.py"))
    DATABASES = PRODUCTION_SETTINGS.DATABASES
    MEDIA_ROOT = PRODUCTION_SETTINGS.MEDIA_ROOT

MY_GOOGLE_API_KEY = 'AIzaSyB68eUZvmlXHPJ4zHBtCnqhAV87_z3CT30'

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    '173.255.234.214:8000',
    '173.255.234.214',
    '127.0.0.1:8000',
    'localhost:8000',
    'localhost',
    '127.0.0.1',
    'localhost:9000',
    '127.0.0.1:9000',
)