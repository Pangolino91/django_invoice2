from .base import *  # do the same for local

DEBUG=False
ALLOWED_HOSTS =[os.getenv("DJANGO_ALLOWED_HOSTS")]
SECRET_KEY=os.getenv("DJANGO_SECRET_KEY") # yes you will need to
print(os.getenv('DATABASE_HOST'))
# so the most important thing you'll do in produciton is set where django reads the settings from...

# for static files

STATIC_ROOT=os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, 'media')
]

EMAIL_USE_TLS=True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME'),  # Set produciton settings
        'USER': os.getenv("DATABASE_USER"),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv("DATABASE_HOST"),   # Or an IP Address that your DB is hosted on
        'PORT': os.getenv("DATABASE_PORT"), # yes/yes
        'ATOMIC_REQUESTS': True, # yes/exactly
    }
}


EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER=os.getenv("EMAIL_HOST_USER") #  Silly errors
# only applies to gmail, otherwise must be set to false EMAIL_USE_TLS=True
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
