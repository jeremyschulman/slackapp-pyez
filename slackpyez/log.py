import sys
import logging

__all__ = ['create_logger']

_default_logfile = 'slackpyez.log'
_default_format = '%(asctime)s:%(levelname)s:%(message)s'


def create_logger(format=None, logfile=None, stdout=True):

    log = logging.getLogger(__package__)
    log.setLevel(logging.INFO)
    formatter = logging.Formatter(format or _default_format)

    fh = logging.FileHandler(logfile or _default_logfile)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    if stdout is True:
        fh = logging.StreamHandler(sys.stdout)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    return log
