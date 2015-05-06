# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = (

    os.path.join(BASE_DIR,'plantillas'),

)


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1m8g5&hjlsfi@obef1d4a6&bu)x1+o-0s__h4ct*dp#mm+8^*1'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = (
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'django.contrib.sites',
'django.contrib.admindocs',
'south',
'polymorphic', # We need polymorphic installed for the shop
'shop', # The django SHOP application
'shop_simplevariations',
'shop.addressmodel',
'deportmania',
'paypal.standard.ipn',
'shop_paypal',

)




#Email definition

EMAIL_USER_TLS= True
EMAIL_HOST= 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER= 'alemaki92@gmail.com'
EMAIL_HOST_PASSWORD = 'alejandro21992'

PAYPAL_RECEIVER_EMAIL = "deportmania@point-sport.com"
PAYPAL_CURRENCY_CODE ="EUR"
SHOP_SHIPPING_FLAT_RATE = '0'
SHOP_SHIPPING_BACKENDS = [
'deportmania.shipping.FlatRateShipping',
]
SHOP_PAYMENT_BACKENDS = [
'shop_paypal.offsite_paypal.OffsitePaypalBackend'
]
SHOP_CART_MODIFIERS = ['deportmania.modifiers.Fixed7PercentTaxRate','shop_simplevariations.cart_modifier.ProductOptionsModifier',
'shop_simplevariations.cart_modifier.ProductOptionsModifier',
'deportmania.modifiers.FixedShippingCosts',
]
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
MIDDLEWARE_CLASSES = (
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.locale.LocaleMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
PASSWORD_HASHERS = (
'django.contrib.auth.hashers.PBKDF2PasswordHasher',
'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
'django.contrib.auth.hashers.BCryptPasswordHasher',
'django.contrib.auth.hashers.SHA1PasswordHasher',
'django.contrib.auth.hashers.MD5PasswordHasher',
'django.contrib.auth.hashers.CryptPasswordHasher',
)
ROOT_URLCONF = 'deportmania.urls'
WSGI_APPLICATION = 'deportmania.wsgi.application'
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

SOUTH_DATABASE_ADAPTERS = {

    'default':'south.db.mysql'
    }


DATABASES = {
'default': {
'ENGINE': 'django.db.backends.mysql',
'NAME': 'deportmania', # Or path to database file if using sqlite3.
'USER': 'root', # Not used with sqlite3.
'PASSWORD': '', # Not used with sqlite3.
'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
'PORT': '', # Set to empty string for default. Not used with sqlite3.
}
}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),
)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = False
USE_TZ = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
SITE_ID = 1
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8000/media/'
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''
# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'
# Additional locations of static files
STATICFILES_DIRS = (
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
os.path.join(BASE_DIR, "static"),
)
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
'django.template.loaders.filesystem.Loader',
'django.template.loaders.app_directories.Loader',
# 'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
'django.core.context_processors.request',
'django.contrib.auth.context_processors.auth',
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.contrib.messages.context_processors.messages",
)
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
'version': 1,
'disable_existing_loggers': False,
'handlers': {
'mail_admins': {
'level': 'ERROR',
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