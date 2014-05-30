import logging
import os
import os.path

LOGDIR = '%s/../logs/' % os.path.dirname(os.path.realpath(__file__))
LOGFILE = LOGDIR + 'feed_push.logs'

def prepare_log_dir():
  if not os.path.exists(LOGDIR):
    os.mkdir(LOGDIR)

def setup_custom_logger(name):
  prepare_log_dir()
  logger = logging.getLogger(name)
  hdlr = logging.FileHandler(LOGFILE)
  formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')
  hdlr.setFormatter(formatter)
  logger.addHandler(hdlr)
  logger.addHandler(logging.StreamHandler())
  logger.setLevel(logging.DEBUG)
  return logger
