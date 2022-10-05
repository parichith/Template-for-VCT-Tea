# The django settings for the tea shop project with recommender system
# https://docs.djangoproject.com/en/3.1/topics/settings/

import os
from pathlib import Path

# This details of url path patterns for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Localhost deployment area

# This is the secret key for the project
# SECRET_KEY = 'df+7#=dd@p$k@koe(ce%am5jj#9ts(kl_5iy9kxuu60f9p0&7k'

# Debug is currently turned on for development use.
# DEBUG = True

# End Localhost deployment area


# MAIN DEPLOYMENT AREA

# Deployment follows instructions from:
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment
# [Accessed 23/10/2020]
# Django deployment location from:
# https://www.heroku.com/pricing
# [Accessed 23/10/2020]
# Deployment details:
# https://devcenter.heroku.com/articles/how-heroku-works
# [Accessed 23/10/2020]
# Redis on Heroku deployment from:
# https://devcenter.heroku.com/articles/heroku-redis
# [Accessed 28/10/2020]]

# This is the secret key for the project
SECRET_KEY = 'df+7#=dd@p$k@koe(ce%am5jj#9ts(kl_5iy9kxuu60f9p0&7k'

# Debug is currently turned on for development use.
# DEBUG = True
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'
# This was set on the CLI with in directory myshop, containing manage.py:
# export DJANGO_DEBUG=False

# The following warnings are in progress:
# python3 manage.py check --deploy
# # WARNINGS:
# ?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting. If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
# ?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
# ?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
# ?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.
# ?: (security.W020) ALLOWED_HOSTS must not be empty in deployment.

# From Heroku Redis:
CACHES = {
    "default": {
         "BACKEND": "redis_cache.RedisCache",
         "LOCATION": os.environ.get('REDIS_URL'),
    }
}



# END MAIN DEPLOYMENT AREA


# There are no allowed hosts at present
# UPDATED
ALLOWED_HOSTS = ['nameless-sierra-12731.herokuapp.com', 'warm-stream-88728.herokuapp.com', '127.0.0.1', '.herokuapp.com',]

# Applications used in the project
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop.apps.ShopConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'payment.apps.PaymentConfig',
    'coupons.apps.CouponsConfig',

]

#  The list of middleware used in this project
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myshop.urls'

# Details of the templates used in the project
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'myshop.wsgi.application'


# This project uses the default django backend database to run the shop
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# This section is the validators for passwords
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# The current setting of the language code is set to US English, as this appears to be stable.
# The setting will be adjusted to 'en-gb' when other factors have been stabilised
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

CART_SESSION_ID = 'cart'

# ^^^ Django sessions create a virtual JSON structiure that is ended when the session closes.
# It is used in the creation of a shopping cart in the project.
# The cart object is associated with the session in order to allow the purchasing process to take place.
# The process checks if a cart already exists, if not it creates one.
# It continually performs this check for each user amendment, sustaining product objects in the cart
# The 'cart' ID is the key that stores the cart in the session.
# In the cart class, a session is "reqeusted" and this triggers a new session, or an unpdate to an existing one.

# The automated django email backend is used for the django admin system
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# TESTING AREA FOR RECOMMENDER MIDDLEWARE

# This is the port used by the redis server, the redis database is set to default, localhost is its attachment
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# This is the celery setttings, used for asynchronous activities such as billing emails. Free software:
# https://docs.celeryproject.org/en/stable/getting-started/brokers/redis.html
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# Braintree settings for billing validation.  The codes are generated from a free braintree account:
# https://www.braintreepayments.com/
BRAINTREE_MERCHANT_ID = 'ssy9znzx2w2r6bvc'  # Merchant ID
BRAINTREE_PUBLIC_KEY = '3fkrphkkcvcshcdq'   # Public Key
BRAINTREE_PRIVATE_KEY = '8e415b2976c33e42143a650541f4589b'  # Private key

import braintree

BRAINTREE_CONF = braintree.Configuration(
    braintree.Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)

# HEROKU SETTINGS

import django_heroku
django_heroku.settings(locals())
