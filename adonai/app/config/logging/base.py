import logging

from charybdis.app.config import conf


class LoggingConfig:
    LOGGING_FORMAT = conf.get_config("logging_fomat", "%(asctime)-15s %(clientip)s %(user)-8s %(message)s")
    LOGGING_LEVEL = conf.get_config("logging_level", "info")


log_levels = {
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.INFO,
    "debug": logging.DEBUG,
}

logger = logging.getLogger()

if LoggingConfig.LOGGING_LEVEL in log_levels:
    level = log_levels[LoggingConfig.LOGGING_LEVEL]

else:
    logger.warning(f"{LoggingConfig.LOGGING_LEVEL} is invalid log level. Set to default: info.")
    level = log_levels["info"]

logger.setLevel(level)
