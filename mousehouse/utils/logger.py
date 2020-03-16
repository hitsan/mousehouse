import logging

def getLogger(name, logFlie, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    fmt = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")

    fhdlr = logging.FileHandler(logFlie)
    fhdlr.setFormatter(fmt)

    logger.addHandler(fhdlr)
    return logger
