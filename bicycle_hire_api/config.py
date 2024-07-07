from environs import Env
from dataclasses import dataclass


@dataclass
class Database:
    prod_name: str
    test_name: str
    host: str
    port: int
    user: str
    password: str


@dataclass
class Django:
    secret_key: str
    debug: bool
    django_settings_module: str


@dataclass
class SMTP:
    host: str
    host_user: str
    password: str
    port: str


@dataclass
class Celery:
    celery_broker_url: str
    celery_result_backend: str


@dataclass
class Config:
    database: Database
    django: Django
    smtp: SMTP
    celery: Celery


def get_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        database=Database(
            prod_name=env('DB_PROD_NAME'),
            test_name=env('DB_TEST_NAME'),
            host=env('DB_HOST'),
            port=env.int('DB_PORT'),
            user=env('DB_USER'),
            password=env('DB_PASSWORD'),
        ),
        django=Django(
            secret_key=env('DJANGO_SECRET_KEY'),
            django_settings_module=env('DJANGO_SETTINGS_MODULE'),
            debug=env.bool('DEBUG_MODE', default=False),
        ),
        smtp=SMTP(
            host=env('EMAIL_HOST'),
            host_user=env('EMAIL_HOST_USER'),
            password=env('EMAIL_HOST_PASSWORD'),
            port=env('EMAIL_PORT'),
        ),
        celery=Celery(
            celery_broker_url=env('CELERY_BROKER_URL'),
            celery_result_backend=env('CELERY_RESULT_BACKEND'),
        ),
    )
