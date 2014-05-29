#! /usr/bin/env python
import subprocess
import sys
import os.path
from datetime import datetime

import log
from sendmail import sendmail


logger = log.setup_custom_logger('root')
CUR_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = '%s/../config/' % CUR_DIR
MOBI_DIR = '%s/../mobi/' % CUR_DIR
RECIPE_FILE = CONFIG_DIR + 'recipes.txt'
RECIPIENTS_FILE = CONFIG_DIR + 'recipients.txt'
PROCESS_SCRIPT = CUR_DIR + '/process_recipe.sh'

def get_path(recipe):
    recipe_path = CONFIG_DIR + recipe
    mobi = (os.path.splitext(os.path.basename(recipe))[0])
    mobi = '%s_%s.mobi' %(mobi, datetime.now().strftime("%Y-%m-%d"))
    mobi_path = MOBI_DIR + mobi
    return [recipe_path, mobi_path]

def process_recipe(recipe):
  """Process a single recipe
     Check if mobi exists, create one if not
     Returns the mobi file name
  """
  logger.debug('Recipe: %s' %recipe)
  [recipe, mobi] = get_path(recipe)
  logger.debug(mobi)
  if os.path.isfile(mobi):
    logger.info("mobi already exists")
  else:
    subprocess.call([PROCESS_SCRIPT, recipe, mobi])
  return mobi

if __name__ == '__main__':
  logger.debug('main')
  recipes = [line.strip() for line in open(RECIPE_FILE)]
  recipients = [line.strip() for line in open(RECIPIENTS_FILE)]
  
  logger.debug('Recipes: %s' %str(recipes))
  logger.debug('Recipients: %s' %str(recipients))
  
  for recipe in recipes:
    if recipe:
      try:
        attachment = process_recipe(recipe)
        subject = 'Daily feed push: %s' % os.path.basename(attachment)
        logger.info('Subject: %s' %subject)
        sendmail(recipients, subject, attachment)
      except:
        logger.error('Unexpected error: %s', str(sys.exc_info()))
    else:
      logger.debug("Ignore empty line")
