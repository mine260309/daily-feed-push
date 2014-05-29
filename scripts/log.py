import logging
import os.path

LOGFILE = '%s/../logs/feed_push.log' % os.path.dirname(os.path.realpath(__file__))
def setup_custom_logger(name):
  logger = logging.getLogger(name)
  hdlr = logging.FileHandler(LOGFILE)
  formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')
  hdlr.setFormatter(formatter)
  logger.addHandler(hdlr)
  logger.addHandler(logging.StreamHandler())
  logger.setLevel(logging.DEBUG)
  return logger
