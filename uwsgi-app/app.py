# app.py
# Tested with 'uwsgi --socket /tmp/daily-feed-push.sock --wsgi-file uwsgi-app/app.py --chmod-socket=666'

from paste import request
from validate_email import validate_email
from scripts import utils, log
import simplejson as json

import re
hide_email_regex = re.compile(r'(^.*?)(.{1,4})(@.*)')

logger = log.setup_custom_logger('webapp')
encoder = json.JSONEncoder()

def api_subscriptions(env, start_response):
    """
    A simple RESTful API: /subscriptions
    GET: return list of subscriptions
    POST: add a email into subscriptions
    DELETE: delete a email from subscriptions, not supported yet

    Returns json result:
      {
         "meta":{
            "code":<code value>
            "msg":<msg string, optional>
         },
         "data":{
            "subscriptions":[<list of email, optional>]
         }
      }
    """
    code = 400
    result = {}
    if (env['REQUEST_METHOD'] == 'GET'):
        try:
            subscriptions = [hide_email(email) for email in get_subscriptions()]
            logger.debug('Get subscriptions: %s' % str(subscriptions))
            code = 200
            result = construct_response(code, None, subscriptions)
        except Exception as e:
            logger.error('Failed to get subscriptions: %s' % str(e))
            code = 500
            result = construct_response(
                code,
                'Resource Temporarily Unavailable: %s' % str(e),
                None)
    elif (env['REQUEST_METHOD'] == 'POST'):
        fields = request.parse_formvars(env)
        email = None
        if fields.has_key('mail'):
            email = fields.get('mail')
        if (email and len(fields) == 1 and validate_email(email)):
            try:
                logger.debug('Try to add email: %s' % email)
                ret = subscribe(email)
                logger.debug('Added successfully')
                code = 200
                subscriptions = [hide_email(email)
                        for email in get_subscriptions()]
                if ret:
                    msg = 'Subscribed'
                else:
                    msg = 'Already subscribed'
                result = construct_response(code, msg, subscriptions)
            except Exception as e:
                logger.error('Failed: %s' % str(e))
                code = 409
                result = construct_response(
                        code,
                        'Unable to subscribe %s: %s' % (email, str(e)),
                        None)
        else:
            logger.warning('Bad post: %s' % str(fields))
            code = 400
            result = construct_response(code, 'Invalid parameters', None)
    #elif (env['REQUEST_METHOD'] == 'DELETE'):
        #TODO
    else:
        logger.warning('Bad request: %s' % str(env))
        send_response(start_response, 400)
        code = 400
        result = construct_response(code, 'Invalid method', None)
    send_response(start_response, code)
    response = encoder.encode(result)
    logger.debug('Encoded json: %s' % response)
    return [response]

apis = dict()
apis['subscriptions'] = api_subscriptions

def application(env, start_response):
    request_uri = env['REQUEST_URI']
    try:
        api = request_uri[request_uri.rindex('/') + 1:]
        if api in apis:
            return apis[api](env, start_response)
        else:
            logger.warning('Bad request: %s' % str(env))
            code = 400
            result = construct_response(code, 'Invalid request', None)
            send_response(start_response, code)
            response = encoder.encode(result)
            logger.debug('Encoded json: %s' % response)
            return [response]
    except Exception:
        import traceback
        traceback.print_exc()

def construct_response(code, msg, subscriptions):
    result = {'meta': {}, 'data':{}}
    result['meta']['code'] = code
    if msg:
        result['meta']['msg'] = msg
    if subscriptions:
        result['data']['subscriptions'] = subscriptions
    return result

def send_response(response_func, code):
    if (code == 200):
        response_func('200 OK', [('Content-Type', 'application/json')])
    elif (code == 400):
        response_func('400 Bad Request', [('Content-Type', 'application/json')])
    elif (code == 409):
        response_func('409 Conflict', [('Content-Type', 'application/json')])
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
    return utils.add_recipient(email)

def get_subscriptions():
    return utils.get_recipients()
