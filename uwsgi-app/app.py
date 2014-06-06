# app.py
# Tested with 'uwsgi --socket /tmp/daily-feed-push.sock --wsgi-file uwsgi-app/app.py --chmod-socket=666'

from paste import request
from validate_email import validate_email
from scripts import utils, log

import re
hide_email_regex = re.compile(r'(^.*?)(.{1,4})(@.*)')

logger = log.setup_custom_logger('webapp')
def application(env, start_response):
    #print env
    if (env['REQUEST_URI'] == '/api/1/subscriptions' and env['REQUEST_METHOD'] == 'GET'):
        try:
            subscriptions = [hide_email(email) for email in get_subscriptions()]
            logger.debug('Get subscriptions: %s' % str(subscriptions))
            send_response(start_response, 200)
            return [str(subscriptions)]
        except Exception as e:
            logger.error('Failed to get subscriptions: %s' % str(e))
            send_response(start_response, 200)
            return [str(e)]
    elif (env['REQUEST_URI'] == '/api/1/subscribe' and env['REQUEST_METHOD'] == 'POST'):
        fields = request.parse_formvars(env)
        email = None
        if fields.has_key('mail'):
            email = fields.get('mail')
        if (email and len(fields) == 1 and validate_email(email)):
            try:
                logger.debug('Try to add email: %s' % email)
                subscribe(email)
                logger.debug('Added successfully')
                send_response(start_response, 200)
                return ["%s subscribed!" % email]
            except Exception as e:
                logger.error('Failed: %s' % str(e))
                send_response(start_response, 200)
                return ["Unable to subscribe %s: %s" % (email, str(e))]
        else:
            logger.warning('Bad post: %s' % str(fields))
            send_response(start_response, 400)
            return ['Invalid parameters.']
    else:
        logger.warning('Bad request: %s' % str(env))
        send_response(start_response, 400)
        return ['Invalid request.']

def send_response(response_func, code):
    if (code == 200):
        response_func('200 OK', [('Content-Type','text/html')])
    elif (code == 400):
        response_func('400 Bad Request', [('Content-Type','text/html')])
    else:
        logger.error('Invalid response code %s' % str(code))

def hide_email(email):
    '''
    Hide some characters in email address
    '''
    return hide_email_regex.sub(r'\1****\3', email)

def subscribe(email):
    # use this if you want to include modules from a subforder
    #import os, sys, inspect
    #cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe() ))[0],"scripts")))
    #if cmd_subfolder not in sys.path:
    #    print 'Add %s to sys path' % cmd_subfolder
    #    sys.path.insert(0, cmd_subfolder)
    utils.add_recipient(email)

def get_subscriptions():
    return utils.get_recipients()
