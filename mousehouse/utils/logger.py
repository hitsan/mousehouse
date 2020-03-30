import logging
import sys
import os
from config.config_reader import conf

def get_logger(name, console=False):
    """
    Sets the logger configuration and returns the logger.

    Args:
        name (str) : Class name
        console (bool) : whether to output to console

    Returns:
        Logger : logger
    """
    #Set logging level
    logger = logging.getLogger(name)
    level = _get_level()
    logger.setLevel(level)

    #Set format
    fmt = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
    path = os.path.abspath(__file__)
    logFlie = path[:-26] + 'logs/master.log'
    fhdlr = logging.FileHandler(logFlie)
    fhdlr.setFormatter(fmt)
    if console is True:
        shdlr = logging.StreamHandler()
        shdlr.setFormatter(fmt)
        logger.addHandler(shdlr)

    logger.addHandler(fhdlr)
    return logger

def _get_level():
    """
    Get logging level from config.

    Returns:
        int : logging level
    """
    level = {"DEBUG":logging.DEBUG, "INFO":logging.INFO, "WARNING":logging.WARNING,
    "WARN":logging.WARN, "CRITICAL":logging.CRITICAL, "ERROR":logging.ERROR}
    try:
        config = conf["logging"]["level"].upper()
    except:
        print("Logging level is not define.", file=sys.stderr)
        return logging.WARN
    return level[config]