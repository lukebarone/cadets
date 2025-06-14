"""
Router and Controller for getting the OTC Registration Forms entered.
"""
import json
import logging
import os
import csv
import re

from flask import Flask, render_template, request, send_file
# Add "bc52." in front of these imports when developing
from models.candidate import Candidate
from models.dinner_guest import Dinner_Guest
from functions import mail, convert_dictionary


ERROR_BLANK_FORM = "Blank form detected. Aborting."
# Add any error messages here for inclusion in the templates.

LOGGING_PATH = "bc52.log"
LOGGING_LEVEL = logging.DEBUG
logging.basicConfig(level=LOGGING_LEVEL, filename=LOGGING_PATH)
BRANCH_LIST = ["aldergrove", "gibsons", "vancouver", "kamloops", "kelowna",
"newwestminster", "nwvancouver", "princegeorge", "richmond", "surreywhiterock", "vernon"]
CORPS_EMAIL_LIST = {
    "aldergrove": "nlcccolumbia@bcmainland.ca",
    "gibsons": "nlcckennethgrant@bcmainland.ca",
    "vancouver": "nlcccaptainrankin@bcmainland.ca",
    "kamloops": "nlccprincerobert@bcmainland.ca",
    "kelowna": "nlccadmiralstirling@bcmainland.ca",
    "newwestminster": "nlccjfwilliams@bcmainland.ca",
    "nwvancouver": "nlcchcwallace@bcmainland.ca",
    "princegeorge": "nlccaurora@bcmainland.ca",
    "richmond": "nlccmjmiller@bcmainland.ca",
    "surreywhiterock": "nlcccormorant@bcmainland.ca",
    "vernon": "nlccokanagan@bcmainland.ca"
}
# NO_BRANCH_EMAIL_LIST = ["bcmd", "rcsu", "national"]


def create_file(data: dict) -> bool:
    """Adds the data to the database"""
    filename = os.path.join(os.path.relpath("bc52_outputs"),
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


def send_email_to_area(data: dict) -> bool:
    """Send an email to the Area Officers group with the registration info"""
    email_to = "area-officers@bcmainland.ca"
    email_subject = f"New OTC Registration from {data['corps']}"
    email_body = f"""We got a new OTC Registration!
---
{str(data)}

Sincerely,

An automated bot for your convenience.
    """
    mail.send_mail(email_body, email_to, email_subject)
    logging.info("%s - OTC email sent", data['uuid'])


def send_co_confirmation_email(data: dict) -> bool:
    """Send an email confirmation to the CO's email"""
    email_to = CORPS_EMAIL_LIST[data["corps"]]
    email_subject = f"BCMD OTC Registration from {data['corps']}"
    email_body = f"""We received your recent OTC Registration!
---
{str(data)}

Sincerely,

An automated bot for your convenience.
    """
    mail.send_mail(email_body, email_to, email_subject)
    logging.info("%s - Confirmation email sent", data['uuid'])


def send_branch_confirmation_email(data: dict) -> bool:
    """Send a confirmation email to the local branch"""
    value_found = data.get('corps')
    if not value_found in BRANCH_LIST:
        logging.warning("Not found - got %s", data['corps'])
        return False
    if convert_dictionary.convert_for_email(data)[1]:
        logging.info("Branch confirmation email should send - got %s", data['corps'])
        message = f"""
Hi {data['corps']}'s Branch President,

Someone has registered for the BC Mainland Division NLCC Officer Training Course from
your branch. Please confirm the details below, and email us if this is not an
authorized action:

{convert_dictionary.convert_for_email(data)}

If you authorized this action, then please send the cheque payable to Navy
League of Canada, BC Mainland Division for ${data['amount_payable']}
to BCMD's treasurer at:

  Pat Wingfield
  Treasurer - BC Mainland Division
  33157 Turnbridge Ave
  Mission, BC
  V2V 6X9

Payment is due by July 31.

Sincerely,

An automated bot for your convenience."""
        mail.send_mail(message,
                       f"{data['corps']}@bcmainland.ca",
                       "Branch OTC Registration Info received")
        return True

app = Flask(__name__)

@app.route('/', methods=['GET'])
def show_index():
    """Loads the static index page."""
    return send_file("index.html")


@app.route('/submit', methods=['POST'])
def submitted_form():
    """Accepts input for the registration form, passes to template"""
    data = request.form.to_dict()
    # Check the form is filled out
    if None is data:
        return render_template('error.html', error=ERROR_BLANK_FORM)
    # Get info
    candidates = []
    dinner = []
    all_keys = request.form.keys()
    logging.info("Processing candidates from %s - %s", data['corps'], " ".join(list(all_keys)))
    #try:
    keys = [key for key in all_keys if key.startswith("personnel_name_")]
    logging.info("%s - Processed keys", data['corps'])
    for key in keys:
        logging.info("%s - Entering key loop - %s", data['corps'], key)
        # Get index
        index = re.search(r'\d+$', key).group(0)
        logging.info("%s - Working on index %s of %s", data['corps'], index, key)
        candidates.append(Candidate(data.get('personnel_name_' + index),
            data.get('personnel_type_' + index),
            data.get('personnel_time_in_position_' + index),
            data.get('personnel_rank_' + index),
            data.get('personnel_allergy_' + index, "NKA"),
            data.get('personnel_years_in_otc_' + index),
            data.get('personnel_prev_co_' + index, "no"),
            data.get('personnel_prev_xo_' + index, "no"),
            data.get('personnel_prev_admino_' + index, "no"),
            data.get('personnel_prev_trgo_' + index, "no"),
            data.get('personnel_prev_instructor_' + index, "no"),
            data.get('personnel_drill_' + index),
            data.get('personnel_gender_' + index),
            data.get('personnel_medical_' + index, "N/A"),
            ))
        logging.info("%s - Added Candidate %s to array", data.get('corps'), data.get('personnel_name_' + index))

        keys = [key for key in all_keys if key.startswith("dinner_name_")]
        for key in keys:
            # Get index
            index = re.search(r'\d+$', key).group(0)
            dinner.append(Dinner_Guest(data.get('dinner_name_' + index),
                                    data.get('dinner_allergy_' + index, "NKA")))
    
    if len(candidates) < 1 and len(dinner) < 1:
        logging.info("No candidates or dinner guests found for %s", data['corps'])
        return render_template('error.html', error=ERROR_BLANK_FORM)

    logging.info("%s - Ready to process and save info", data.get('corps'))
    create_file(data)
    logging.info("%s - Creating registration file", data.get('corps'))
    add_to_csv_file(data)
    logging.info("%s - Adding to CSV file", data.get('corps'))
    send_email_to_area(data)
    logging.info("%s - Email sent to Area Staff", data.get('corps'))
    send_co_confirmation_email(data)
    logging.info("%s - Email sent to CO", data.get('corps'))
    send_branch_confirmation_email(data)
    logging.info("%s - Email sent to Branch; returning template", data.get('corps'))
    return render_template('response.html', form=request.form, candidates=candidates, dinner=dinner)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
