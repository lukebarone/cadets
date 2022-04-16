#!/usr/bin/env python3
"""Sends an email to the specified account
"""
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

SMTP_PORT = 587
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "bc9@bcmainland.ca"
RECEIVER_EMAIL = "lbarone+bc9@bcmainland.ca"
PASSWORD = os.environ['BC9_APP_PASSWORD']
SUBJECT = "BC9 Submission"


def send_mail(email_body: str):
    mimemsg = MIMEMultipart()
    mimemsg['From'] = SENDER_EMAIL
    mimemsg['To'] = RECEIVER_EMAIL
    mimemsg['Subject'] = SUBJECT
    mimemsg.attach(MIMEText(email_body, 'plain'))
    connection = SMTP(host=SMTP_SERVER, port=SMTP_PORT)
    connection.set_debuglevel(10)
    connection.starttls()
    connection.login(SENDER_EMAIL, PASSWORD)
    connection.send_message(mimemsg)
    connection.quit()
    connection.close()


if __name__ == "__main__":
    print("Script not made to be called directly. Import then use the send_mail function.")
