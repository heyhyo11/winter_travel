"""
Django settings for project_main project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https: // docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https: // docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import json
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%=6t*dk*@05k2bif5^0o$gn_2+ct78pclop49vx*htu)iuzk99'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main_page',
    'storages',
    'API',
    'detail',

    # 유저
    'user',
    # 소셜 로그인
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.github',

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project_main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'winter_project',
        'USER': 'admin',
        'PASSWORD': 'winterproject',
        'HOST': 'database-1.cudljsclqczn.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# static 기본경로 설정
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR
]

STATIC_ROOT = os.path.join(BASE_DIR, '.static_root')

# AWS

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


with open(os.path.join(BASE_DIR, 'project_main/config/aws.json')) as f:
    secrets = json.loads(f.read())

AWS_ACCESS_KEY_ID = secrets['AWS']['ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secrets['AWS']['SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = secrets['AWS']['STORAGE_BUCKET_NAME']

AWS_S3_REGION_NAME = "ap-northeast-2"
AWS_S3_SIGNATURE_VERSION = "s3v4"

AWS_DEFAULT_ACL = 'public-read'


# user 앱
AUTH_USER_MODEL = 'user.UserModel'

# 소셜 로그인
SITE_ID = 1     # 사이트 설정에 필요한 변수

AUTHENTICATION_BACKENDS = (
    # allauth와 관계없이 django-admin에서 username으로 로그인
    'django.contrib.auth.backends.ModelBackend',
    # allauth 인증 방법 (ex. email로 로그인)
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = '/'                # 로그인 성공 시 리다이렉트할 페이지
ACCOUNT_LOGOUT_REDIRECT_URL = '/account/login'  # 로그아웃 후 리다이렉트할 페이지

ACCOUNT_LOGOUT_ON_GET = True             # /account/logout 페이서 추가적으로 버튼 클릭할 것 없이 자동으로 로그아웃 시켜줌
SOCIALACCOUNT_LOGIN_ON_GET = True        # 바로 구글/카카오 계정 연결하는 페이지로 넘어감 (False로 하면 /account/kakao/login 페이지가 나옴)

ACCOUNT_EMAIL_REQUIRED = True            # 회원 가입시 email은 필수 입력
ACCOUNT_USERNAME_REQUIRED = True         # 회원 가입시 username은 필수 입력
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # 로그인 인증 방법 : 이메일
ACCOUNT_EMAIL_VERIFICATION = "none"      # 이메일 유효성 인증 사용 안함

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "104758601108-t2dvrpe1486k3tjuau81f8nt2rinjrkh.apps.googleusercontent.com",
            "secret": "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",
            "key": ""
        }
    },
    "kakao": {
        "APP": {
            "client_id": "bbadf3bef8eadc2f7e3f62e4d1014c75",
            "secret": "",
            "key": ""
        }
    },
    "github": {
        "APP": {
            "client_id": "511f439400dbbcf91596",
            "secret": "eb5a900902ce61ac203128d65d5c35696b9b9c4b",
            "key": ""
        }
    }
}

CRONJOBS = [
    ('0 */1 * * *', 'API.cron.hot_item_reset', '>> reset.log')
]


