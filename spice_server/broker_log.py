# coding=utf-8
from datetime import datetime
import logging
author__ = 'aleksandrvadimovic'

def log(error):
    logging.basicConfig(filename='broker.log',level=logging.DEBUG)
    logging.warning(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S") + ": " + error + "\n")


