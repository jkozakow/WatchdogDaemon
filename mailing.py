import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MAIL_SENDER = os.environ.get('MAIL_SENDER', "notifications@example.com")
MAIL_RECEIVER = os.environ.get('MAIL_RECEIVER', "admin@mydomain.com")


def send_email(text):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Notification from watchdog_deamon"
    msg['From'] = MAIL_SENDER
    msg['To'] = MAIL_RECEIVER

    mail_text = MIMEText(text, 'plain')
    msg.attach(mail_text)
    s = smtplib.SMTP('localhost')
    s.sendmail(MAIL_SENDER, [MAIL_RECEIVER], msg.as_string())
    s.quit()
