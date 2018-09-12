# =============================================================================
# Author: falseuser
# File Name: worker_utils.py
# Created Time: 2018-09-07 17:41:41
# Last modified: 2018-09-12 11:22:38
# Description:
# =============================================================================
import logging
import os
from logging.handlers import RotatingFileHandler
from configparser import SafeConfigParser


class ConfigHandler(SafeConfigParser):

    DEFAULTS = {
    }

    def __init__(self, filename):
        super().__init__(self.DEFAULTS)
        self.read(filename)


config = ConfigHandler("config.ini")


class LogHandler(logging.Logger):

    _fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    _datefmt = "%a, %d %b %Y %H:%M:%S"
    _logpath = config.get("default", "log_path")

    def __init__(self, name=None):
        logging.Logger.__init__(self, name)
        self._prepare()
        self.log_file = "{0}/{1}.log".format(self._logpath, name)
        formatter = logging.Formatter(self._fmt, self._datefmt)
        rfhandler = RotatingFileHandler(
            self.log_file, maxBytes=1024*1024, backupCount=5,
        )
        rfhandler.setFormatter(formatter)
        self.addHandler(rfhandler)

    def _prepare(self):
        if os.path.exists(self._logpath):
            return
        else:
            os.mkdir(self._logpath)


worker_logger = LogHandler("worker")
link_logger = LogHandler("link")
