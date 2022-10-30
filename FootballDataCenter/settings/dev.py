from settings.base import *


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'footballdata',
        'USER': 'onak97',
        'PASSWORD': 'admin1234',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
