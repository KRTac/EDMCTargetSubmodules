import os
import logging

from config import appname


PLUGIN_NAME = os.path.basename(os.path.dirname(__file__))

class Log(object):

    def __init__(self):
        self.logger = logging.getLogger(f'{appname}.{PLUGIN_NAME}')
        self.logger.setLevel(logging.INFO)
        if not self.logger.hasHandlers():
            logger_channel = logging.StreamHandler()
            logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
            logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
            logger_formatter.default_msec_format = '%s.%03d'
            logger_channel.setFormatter(logger_formatter)
            self.logger.addHandler(logger_channel)

    def info(self, msg):
        self.logger.log(logging.INFO, msg)

LOG = Log()
