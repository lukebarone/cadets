"""Sends an email to the specified account"""
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

SMTP_PORT = 465
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "agm@bcmainland.ca"
RECEIVER_EMAIL = "lbarone@bcmainland.ca"
load_dotenv("/var/cadets/.env")
PASSWORD = os.environ['NOREPLY_APP_PASSWORD']
NOREPLY_EMAIL = "no-reply@bcmainland.ca"
SUBJECT = "New AGM Registration"


def send_mail(email_body: str, to_address: str = RECEIVER_EMAIL,
              subject: str = SUBJECT):
    """Send an email to the specified accounts."""
    msg = MIMEText(email_body)
    #mimemsg = MIMEMultipart()
    #mimemsg['From'] = NOREPLY_EMAIL
    #mimemsg['Reply-To'] = SENDER_EMAIL
    #mimemsg['To'] = to_address
    #mimemsg['Subject'] = subject
    #mimemsg.attach(MIMEText(email_body, 'plain'))
    msg['Subject'] = subject
    msg['From'] = NOREPLY_EMAIL
    msg['Reply-To'] = SENDER_EMAIL
    msg['To'] = to_address
    with smtplib.SMTL_SSL(SMTP_SERVER, SMTP_PORT) as smtp_server:
        smtp_server.login(NOREPLY_EMAIL, PASSWORD)
        smtp_server.sendmail(NOREPLY_EMAIL, to_address, msg.as_string())
    # connection = SMTP(host=SMTP_SERVER, port=SMTP_PORT)
    # connection.set_debuglevel(10)
    # connection.starttls()
    # connection.login(NOREPLY_EMAIL, PASSWORD)
    # connection.send_message(mimemsg)
    # connection.quit()
    # connection.close()


if __name__ == "__main__":
    print("Script not made to be called directly. Import then use the send_mail function.")
