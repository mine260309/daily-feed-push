# Import smtplib for the actual sending function
import smtplib
import os.path

# Import the email modules we'll need
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import log


logger = log.setup_custom_logger('sendmail')
CUR_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = '%s/../config/mail.conf' % CUR_DIR

def get_config():
  import ConfigParser
  config = ConfigParser.ConfigParser()
  config.read(CONFIG_FILE)
  mailconfig = {}
  mailconfig['smtp'] = config.get('mail', 'smtp')
  mailconfig['port'] = config.get('mail', 'port')
  mailconfig['user'] = config.get('mail', 'user')
  mailconfig['password'] = config.get('mail', 'password')
  return mailconfig

def sendmail(recipients, subject, attachment):
  mailconfig = get_config()
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
