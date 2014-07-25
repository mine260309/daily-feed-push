#! /usr/bin/env python
import subprocess
import sys
import os.path

import log
import utils
from datetime import date
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
            if 'weekly' in recipe and date.today().weekday() == 6:
                should_process = True
            elif 'daily' in recipe:
                should_process = True
            else:
                should_process = False

            if should_process:
                logger.info('Processing recipe %s' % recipe)
                attachment = process_recipe(recipe)
                logger.info('%s genereated successfully' % attachment)
                name = os.path.basename(attachment)
                if (utils.is_mobi_sent(attachment)):
                    logger.info('%s already sent' % name)
                else:
                    subject = 'Daily feed push: %s' % name
                    sendmail(recipients, subject, attachment)
                    utils.mark_mobi_sent(attachment)
            else:
                logger.info('Skip recipe %s' %recipe)
        except:
            #logger.error('Unexpected error: %s', str(sys.exc_info()))
            import traceback
            traceback.print_exc(file=sys.stdout)
