from .base import *  # do the same for local

ALLOWED_HOSTS =os.getenv("DJANGO_ALLOWED_HOSTS")
SECRET_KEY=os.get_env("DJANGO_SECRET_KEY") # yes you will need to

# so the most important thing you'll do in produciton is set where django reads the settings from...

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME'),  # Set produciton settings
        'USER': os.getenv("DATABSE_USER"),
        'PASSWORD': os.getenv('DATABSE_PASSWORD'),
        'HOST': os.getenv("DATABASE_HOST"),   # Or an IP Address that your DB is hosted on
        'PORT': os.getenv("DATABASE_PORT"), # yes/yes
        'ATOMIC_REQUESTS': True, # yes/exactly
    }
}


EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_USER=os.getenv("EMAIL_USER")