#! /usr/bin/env python
import sys
import os.path

import utils
from sendmail import sendmail


def send_notify():
    if len(sys.argv) != 2:
        print 'Usage:\n\t{0} <file>\nSend a notification to all users.'.format(sys.argv[0])
        return 1
    file = sys.argv[1]
    fullpath = os.path.abspath(file)
    filename = os.path.basename(fullpath)
    print 'To send {0} to all users...'.format(file)
#    print 'Full path: {0}, filename: {1}'.format(fullpath, filename)
    recipients = utils.get_recipients()
    sendmail(recipients, filename, fullpath)
    print 'Done'

if __name__ == '__main__':
    send_notify()
