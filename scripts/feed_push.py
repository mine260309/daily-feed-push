#! /usr/bin/env python
import subprocess
import sys
import os.path

import log
import utils
from sendmail import sendmail


logger = log.setup_custom_logger('root')
def process_recipe(recipe):
    """Process a single recipe
       Check if mobi exists, create one if not
       Returns the mobi file name
    """
    utils.prepare_mobi_dir()
    logger.debug('Recipe: %s' %recipe)
    [recipe, mobi] = utils.get_recipe_mobi_path(recipe)
    logger.debug(mobi)
    if os.path.isfile(mobi):
        logger.info("mobi already exists")
    else:
        ret = subprocess.call([utils.get_process_script(), recipe, mobi])
        if ret != 0:
            raise RuntimeError("process fails for recipe " + recipe)
    return mobi

if __name__ == '__main__':
    logger.debug('main')
    recipes = utils.get_recipes()
    logger.debug('Recipes: %s' %str(recipes))
    recipients = utils.get_recipients()
    logger.debug('Recipients: %s' %str(recipients))

    for recipe in recipes:
        try:
            logger.info('Processing recipe %s' % recipe)
            attachment = process_recipe(recipe)
            logger.info('%s genereated successfully' % attachment)
            subject = 'Daily feed push: %s' % os.path.basename(attachment)
            sendmail(recipients, subject, attachment)
        except:
            logger.error('Unexpected error: %s', str(sys.exc_info()))
