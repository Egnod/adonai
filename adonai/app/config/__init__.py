from sitri import Sitri
from sitri.contrib.system import SystemConfigProvider, SystemCredentialProvider

conf = Sitri(
    config_provider=SystemConfigProvider(prefix="adonai"),
    credential_provider=SystemCredentialProvider(prefix="adonai"),
)


from .base import BaseConfig  # isort:skip
from .database import DataBaseConfig  # isort:skip
from .logging import LoggingConfig  # isort:skip
from .secrets import SecretsConfig  # isort:skip


class Config(BaseConfig, LoggingConfig, DataBaseConfig, SecretsConfig):
    pass
