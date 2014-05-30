import os.path
from datetime import datetime

# Various helper functions
CUR_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = '%s/../config/' % CUR_DIR
MOBI_DIR = '%s/../mobi/' % CUR_DIR
RECIPE_FILE = CONFIG_DIR + 'recipes.txt'
RECIPIENTS_FILE = CONFIG_DIR + 'recipients.txt'
PROCESS_SCRIPT = CUR_DIR + '/process_recipe.sh'


def get_mailconfig():
    import ConfigParser
    config = ConfigParser.ConfigParser()
    configfile = CONFIG_DIR + 'mail.conf'
    config.read(configfile)
    mailconfig = {}
    mailconfig['smtp'] = config.get('mail', 'smtp')
    mailconfig['port'] = config.get('mail', 'port')
    mailconfig['user'] = config.get('mail', 'user')
    mailconfig['password'] = config.get('mail', 'password')
    return mailconfig

def prepare_mobi_dir():
    if not os.path.exists(MOBI_DIR):
        os.mkdir(MOBI_DIR)

def get_recipe_mobi_path(recipe):
    recipe_path = CONFIG_DIR + recipe
    mobi = (os.path.splitext(os.path.basename(recipe))[0])
    mobi = '%s_%s.mobi' %(mobi, datetime.now().strftime("%Y-%m-%d"))
    mobi_path = MOBI_DIR + mobi
    return [recipe_path, mobi_path]

def get_recipes():
    return filter(bool, [line.strip() for line in open(RECIPE_FILE)])

def get_recipients():
    return filter(bool, [line.strip() for line in open(RECIPIENTS_FILE)])

def get_process_script():
    return PROCESS_SCRIPT
