import os


class BaseConfig:
    APP_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
