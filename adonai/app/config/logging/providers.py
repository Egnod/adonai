import logging
import typing
from abc import ABCMeta, abstractmethod

from .base import logger


class LoggingProvider(metaclass=ABCMeta):
    @abstractmethod
    def connect(self, logger: logging.Logger, *args, **kwargs) -> None:
        pass


PROVIDERS: typing.List[LoggingProvider] = []


for provider in PROVIDERS:
    provider.connect(logger)
