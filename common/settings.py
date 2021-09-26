import os

DATABASES = {
    'local_games': {
        'SQLALCHEMY_ENGINE': 'postgresql+psycopg2',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'NAME': 'games',
        'USER': 'postgres',
        'PASSWORD': 'akshat@123',
    }
}

DATABASES['default'] = DATABASES['local_games']