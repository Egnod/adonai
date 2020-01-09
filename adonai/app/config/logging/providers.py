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

# EXAMPLE WITH fluentd
"""
from fluent import handler

class FluentdProvider(LoggingProvider):
    FLUENTD_TAG = get_config("fluentd_tag")
    FLUENTD_HOST = get_config("fluentd_host")
    FLUENTD_PORT = get_config("fluentd_port")

    def connect(self, logger: logging.Logger) -> None:
        custom_format = {
        'host': '%(hostname)s',
        'where': '%(module)s.%(funcName)s',
        'type': '%(levelname)s',
        'stack_trace': '%(exc_text)s'
        }
        handle_fluentd = handler.FluentHandler(self.FLUENTD_TAG, host=self.FLUENTD_HOST, port=self.FLUENTD_PORT)
        formatter = handler.FluentRecordFormatter(custom_format)
        handle_fluentd.setFormatter(formatter)
        logger.addHandler(handle_fluentd)

PROVIDERS: typing.List[LoggingProvider] = [FluentdProvider]

"""
