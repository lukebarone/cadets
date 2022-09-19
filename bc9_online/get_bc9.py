"""
Router and Controller for getting the BC(9) Forms entered.
"""
import json
import logging
import os

from flask import Flask, render_template, request, send_file

import read_responses
from mail import send_mail
from models import person

NOT_CHECKED_ERROR_MSG = """You need to check the box acknowledging the data is
complete and verified."""
NO_CORPS_SUPPORTED_ERROR_MSG = """You need to specify whether your branch
supports a Navy League Cadet Corps, a Royal Canadian Sea Cadet Corps, or both.
"""

LOGGING_PATH = "get_bc9.log"
LOGGING_LEVEL = logging.DEBUG
logging.basicConfig(level=LOGGING_LEVEL, filename=LOGGING_PATH)


def add_to_database(data: dict) -> bool:
    """Adds the data to the database"""
    filename = os.path.join(os.path.relpath("bc9_outputs"),
                            data.get("uuid") + ".json")
    with open(filename, "w", encoding='utf-8') as output_file_handle:
        json.dump(data, output_file_handle)
    logging.info("Wrote file %s", filename)
    email_to_send = read_responses.entry_point(data['uuid'])
    send_mail(email_to_send)


app = Flask(__name__)

@app.route('/', methods=['GET'])
def show_index():
    """Loads the static form page."""
    return send_file("index.html")


@app.route('/submit', methods=['POST'])
def submitted_form():
    """Accepts input for the BC(9) form, passes to template"""
    data = request.form.to_dict()
    verified = data.get("verified")
    if not verified:
        print("Error! Was not verified")
        return render_template('error.html', error=NOT_CHECKED_ERROR_MSG)
    if not data['rcscc_corps'] == "yes" and not data['nlcc_corps'] == "yes":
        print("Error! Not supporting any corps")
        return render_template('error.html', error=NO_CORPS_SUPPORTED_ERROR_MSG)
    president = person.Person(Name=data['pres_name'],
                       Address=data['pres_address'],
                       Position="President",
                       Email=data['pres_email'],
                       Telephone=data['pres_tel'])
    vp1 = person.Person(Name=data['vp1_name'],
                 Address=data['vp1_address'],
                 Position="1st Vice President",
                 Email=data['vp1_email'],
                 Telephone=data['vp1_tel'])
    vp2 = person.Person(Name=data['vp2_name'],
                 Address=data['vp2_address'],
                 Position="2nd Vice President",
                 Email=data['vp2_email'],
                 Telephone=data['vp2_tel'])
    treasurer = person.Person(Name=data['treasurer_name'],
                       Address=data['treasurer_address'],
                       Position="Treasurer",
                       Email=data['treasurer_email'],
                       Telephone=data['treasurer_tel'])
    secretary = person.Person(Name=data['secretary_name'],
                       Address=data['secretary_address'],
                       Position="Secretary",
                       Email=data['secretary_email'],
                       Telephone=data['secretary_tel'])
    vsc = person.Person(Name=data['vsc_name'],
                 Address=data['vsc_address'],
                 Position="Volunteer Screening Coordinator",
                 Email=data['vsc_email'],
                 Telephone=data['vsc_tel'])
    people = [president, vp1, vp2, treasurer, secretary, vsc]
    for i in range(100):
        index = i.__str__()
        if request.form.getlist('extra_name_' + index).__str__() != "[]":
            extra_person = person.Person(data['extra_name_' + index],
                data['extra_address_' + index],
                data['extra_tel_' + index],
                data['extra_email_' + index],
                data['extra_position_' + index])
            people.append(extra_person)
    add_to_database(data)
    return render_template('response.html', form=request.form, people=people)

@app.route('/images/BCMD_Crest.png', methods=['GET'])
def load_crest():
    """Returns the crest for an image file"""
    return send_file("images/BCMD_Crest.png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
