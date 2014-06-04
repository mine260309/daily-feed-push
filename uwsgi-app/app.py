# app.py
# Tested with 'uwsgi --socket /tmp/mysite.sock --wsgi-file uwsgi-app/app.py --chmod-socket=666'

from paste import request


def application(env, start_response):
    if (env['REQUEST_METHOD'] == 'GET'):
        fields = request.parse_formvars(env)
        email = None
        if 'mail' in fields:
            email = fields['mail']
        if (email and len(fields) == 1):
            try:
                subscribe(email)
                start_response('200 OK', [('Content-Type','text/html')])
                return ["%s subscribed!" % email]
            except Exception as e:
                start_response('200 OK', [('Content-Type','text/html')])
                return ["Unable to subscribe %s: %s" % (email, str(e))]
        else:
            start_response('400 Bad Request', [('Content-Type','text/html')])
            return ['Invalid request.']
    else:
        start_response('400 Bad Request', [('Content-Type','text/html')])
        return ['Invalid request.']

def subscribe(email):
    # use this if you want to include modules from a subforder
    #import os, sys, inspect
    #cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe() ))[0],"scripts")))
    #if cmd_subfolder not in sys.path:
    #    print 'Add %s to sys path' % cmd_subfolder
    #    sys.path.insert(0, cmd_subfolder)
    from scripts import utils
    utils.add_recipient(email)
