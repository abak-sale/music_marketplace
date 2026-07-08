import os
from pathlib import Path

# Jalur dasar proyek (music_marketplace/)
BASE_DIR = Path(__file__).resolve().parent.parent

# KEAMANAN: Jangan gunakan ini di produksi rahasia!
SECRET_KEY = 'django-insecure-ganti-ini-nanti-saat-live-marketplace'

# Jalankan dalam mode debug untuk melihat error secara detail saat develop
DEBUG = True

# Host yang diizinkan mengakses website ini di lokal
ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Aplikasi yang terdaftar di proyek ini
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Aplikasi buatan kita akan dimasukkan di bawah sini nanti...
    'homepage.apps.HomepageConfig',
    'products.apps.ProductsConfig',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # BEST PRACTICE: Mengarahkan Django ke folder templates/ di root project
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database menggunakan SQLite3 (Sesuai panduan pemula)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validasi Password bawaan Django
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


# Konfigurasi Bahasa dan Zona Waktu Indonesia
LANGUAGE_CODE = 'id'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_TZ = True


# Konfigurasi File Statis (CSS, JavaScript, Gambar Tema)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Konfigurasi File Media (Gambar yang diupload penjual/user)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Pengaturan ID otomatis bawaan untuk Model database
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'