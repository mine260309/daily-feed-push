# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import log
import utils


logger = log.setup_custom_logger('sendmail')

def sendmail(recipients, subject, attachment):
    mailconfig = utils.get_mailconfig()
    mail_from = mailconfig['user'];

    # Create a message with multipart
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = ", ".join(recipients)
    outer['From'] = mail_from

    ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)

    fp = open(attachment, 'rb')
    msg = MIMEBase(maintype, subtype)
    msg.set_payload(fp.read())
    fp.close()

    # Encode the payload using Base64
    encoders.encode_base64(msg)
    msg.add_header('Content-Disposition', 'attachment', filename=attachment)
    outer.attach(msg)
    composed = outer.as_string()

    logger.debug('Sending mail to %s ...' % str(recipients))
    try:
        if mailconfig['port']:
            logger.debug('SMTP server: %s:%s', mailconfig['smtp'], mailconfig['port'])
            server = smtplib.SMTP(mailconfig['smtp'], int(mailconfig['port']))
        else:
            logger.debug('SMTP server: %s', mailconfig['smtp'])
            server = smtplib.SMTP(mailconfig['smtp'])
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(mail_from, mailconfig['password'])
        server.sendmail(mail_from, recipients, composed)
    except:
        logger.error('Failed to send mail')
        raise
    logger.info('Sent successfully')
    server.quit()
