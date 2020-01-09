import os

from ..config import conf
from .base import BaseConfig


class DataBaseConfig:
    DB_USER = conf.get_credential("db_user", "charybdis")
    DB_PORT = conf.get_credential("db_port", "5432")
    DB_NAME = conf.get_credential("db_user", "charybdis")
    DB_PASSWORD = conf.get_credential("db_password", "charybdis_secrets")
    DB_HOST = conf.get_credential("db_host", "localhost")

    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MIGRATIONS_DIR = os.path.join(BaseConfig.APP_DIR, "migrations/")
