"""
Router and Controller for getting the AGM Registration Forms entered.
"""
import json
import logging
import os
import csv

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, render_template, request, send_file
from models.person import Person
from functions.mail import send_mail


ERROR_BLANK_FORM = "Blank form detected. Aborting."
# Add any error messages here for inclusion in the templates.

LOGGING_PATH = "agm.log"
LOGGING_LEVEL = logging.DEBUG
logging.basicConfig(level=LOGGING_LEVEL, filename=LOGGING_PATH)
SLACK_API_KEY = os.environ.get('SLACK_API_KEY')


def create_file(data: dict) -> bool:
    """Adds the data to the database"""
    filename = os.path.join(os.path.relpath("agm_outputs"),
                            data.get("uuid") + ".json")
    try:
        with open(filename, "w", encoding='utf-8') as output_file_handle:
            json.dump(data, output_file_handle)
        logging.info("%s - Wrote file %s", data['uuid'], filename)
    except IOError:
        logging.warning("%s - Failed to write individual file", data['uuid'])
        return False
    return True


def add_to_csv_file(data: dict) -> bool:
    """Add the data to the spreadsheet"""
    # fieldnames = ['branch_name', 'participant_email', 'participant_phone',
    #               'uuid', 'submitted_date', 'additional_comments',
    #               'book_hotel', 'share_room', 'people_count', 'amount_payable']
    file_exists = os.path.exists('registrations.csv')
    file_write_mode = 'w' if not file_exists else 'a'
    try:
        with open('registrations.csv', file_write_mode, encoding='UTF8', newline='') as _:
            writer = csv.DictWriter(_, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
            logging.info("%s - Added to CSV file", data['uuid'])
    except IOError:
        logging.warning("%s - error adding to CSV file", data['uuid'])
        return False
    return True


def send_email_to_agm_group(data: dict) -> bool:
    """Send an email to the AGM group with the registration info"""
    email_to = "agm@bcmainland.ca"
    email_subject = f"New AGM Registration from {data['branch_name']}"
    email_body = f"""We got a new AGM Registration!
---
{str(data)}

Sincerely,

An automated bot for your convenience.
    """
    send_mail(email_body, email_to, email_subject)
    logging.info("%s - AGM email sent", data['uuid'])


def send_slack_notification(data: dict) -> bool:
    """Send a Slack notification to #agm-planning"""
    client = WebClient(SLACK_API_KEY)
    message_text = f"""New AGM Registration: {data['participant_name']} from
        {data['branch_name']}"""
    try:
        filepath = os.path.join(os.path.relpath("agm_registrations"),
                                data.get("uuid") + ".json")
        response = client.files_upload(channels="#bcmd-agm-planning",
                                       file=filepath)
        assert response["file"]
        client.chat_postMessage(channel="#bcmd-agm-planning",
                                text=message_text)
    except SlackApiError as error:
        assert error.response["ok"] is False
        assert error.response["error"]
        logging.warning("%s - Slack notification failed", data['uuid'])
        return False
    logging.info("%s - Slack notification sent", data['uuid'])
    return True


def send_confirmation_email(data: dict) -> bool:
    """Send an email confirmation to the primary name's email"""
    email_to = data['participant_email']
    email_subject = f"BCMD AGM Registration from {data['branch_name']}"
    email_body = f"""We received your recent AGM Registration!
---
{str(data)}

Note: If you asked us to book your hotel room, we will attempt to complete it within 72 hours. If you do not hear from us by then, please reply to this email (it should reply to agm@bcmainland.ca).

Sincerely,

An automated bot for your convenience.
    """
    send_mail(email_body, email_to, email_subject)
    logging.info("%s - Confirmation email sent", data['uuid'])


app = Flask(__name__)

@app.route('/', methods=['GET'])
def show_index():
    """Loads the static index page."""
    return send_file("index.html")


@app.route('/registration.html', methods=['GET'])
def show_registration():
    """Loads the static registration page"""
    return send_file("registration.html")


@app.route('/submit', methods=['POST'])
def submitted_form():
    """Accepts input for the registration form, passes to template"""
    data = request.form.to_dict()
    # Check the form is filled out
    if None is data:
        return render_template('error.html', error=ERROR_BLANK_FORM)
    # Get branch info
    primary_name = Person(data['participant_name'],
                          data['delegate_position'],
                          data['is_delegate'],
                          data['personnel_allergy'])
    people = [primary_name]
    for i in range(100):
        index = str(i)
        if str(request.form.getlist('additional_personnel[' + index + ']')) != "[]":
            extra_person = Person(data['personnel_name_' + index],
                                  data['personnel_position_' + index],
                                  "No",
                                  data['personnel_allergy_' + index])
            people.append(extra_person)
    create_file(data)
    add_to_csv_file(data)
    send_slack_notification(data)
    send_email_to_agm_group(data)
    send_confirmation_email(data)
    return render_template('response.html', form=request.form, people=people)

@app.route('/images/BCMD_Crest.png', methods=['GET'])
def load_crest():
    """Returns the crest for an image file"""
    return send_file("images/BCMD_Crest.png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
