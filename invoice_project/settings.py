from .base import *

ALLOWED_HOSTS = ['*']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&s4$ykxeo21#7t5_kx*ukhf6c-qco@0+wy^3(w$baqtyv+b8d4'
# I'll just copy this one for now
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_invoice',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
    }
}


EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
