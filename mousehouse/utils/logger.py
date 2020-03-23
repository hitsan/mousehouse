import logging

def getLogger(name, console=False,logFlie='logs/master.log', level=logging.DEBUG):
    """
    Sets the logger configuration and returns the logger.
    """
    logger = logging.getLogger(name)
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
