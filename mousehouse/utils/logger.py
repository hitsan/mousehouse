import logging
from .configReader import conf

def getLogger(name, console=False,logFlie='logs/master.log'):
    """
    Sets the logger configuration and returns the logger.
    """
    logger = logging.getLogger(name)
    level = _getLevel(conf)
    logger.setLevel(level)

    fmt = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")

    fhdlr = logging.FileHandler(logFlie)
    fhdlr.setFormatter(fmt)
    if console is True:
        shdlr = logging.StreamHandler()
        shdlr.setFormatter(fmt)
        logger.addHandler(shdlr)

    logger.addHandler(fhdlr)
    return logger

def _getLevel(conf):
    try:
        level = {"DEBUG":logging.DEBUG, "INFO":logging.INFO, "WARNING":logging.WARNING,\
         "WARN":logging.WARN, "CRITICAL":logging.CRITICAL, "ERROR":logging.ERROR}
    except:
        print("Logging level is not define.", file=sys.stderr)
        return logging.INFO
    config = conf["logging"]["level"].upper()
    return level[config]