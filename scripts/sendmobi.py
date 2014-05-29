#! /usr/bin/env python
from sendmail import sendmail

def send_command(recipients, subject, attachment):
    """Send email to recipients with subject and an attachment"""
    print 'Attachment: %s' %attachment
    print 'Recipients:'
    tos = recipients.split()
    for to in tos:
        print to
    sendmail(tos, subject, attachment)

if __name__ == '__main__':
    import scriptine
    scriptine.run()

