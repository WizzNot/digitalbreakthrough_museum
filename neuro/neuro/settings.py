from pathlib import Path
from dotenv import load_dotenv
import tensorflow as tf
import pandas as pd
from tensorflow.keras.models import load_model
import os
import tensorflow_addons as tfa

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fakekey")

DEBUG = os.getenv("DJANGO_DEBUG", "false").lower() in ("true", "1")

ALLOWED_HOSTS = [i for i in os.getenv("ALLOWED_HOSTS", "127.0.0.1").split(",")]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "homepage.apps.HomepageConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "neuro.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "neuro.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = [BASE_DIR / "src"]

STATIC_SRC = BASE_DIR / "src"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Model

MODEL_PATH = os.path.join(STATIC_SRC, 'mnist-dense_second.hdf5')

MODEL_MOBILENET = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Загрузка модели
MODEL = load_model(MODEL_PATH)

# Группы

GROUPS = ['Археология', 'Оружие', 'Прочие', 'Нумизматика', 'Фото, негативы', 'Редкие книги', 'Документы', 'Печатная продукция', 'ДПИ', 'Скульптура', 'Графика', 'Техника', 'Живопись', 'Естественнонауч.коллекция', 'Минералогия']

# FEATHER DATA
DF = pd.read_feather(os.path.join(STATIC_SRC, "data.feather"))
CSV_DF = pd.read_csv(os.path.join(STATIC_SRC, "train.csv"), delimiter=";")
FEATURE_VECTORS = DF.drop("group", axis=1).drop("id", axis=1).to_numpy()

if not os.path.exists(os.path.join(STATIC_SRC, "train")):
    print("!!!Image folder doesn't exist. Please read README file.!!!")