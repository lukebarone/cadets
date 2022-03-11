"""
Router and Controller for getting the BC(9) Forms entered.
"""
import json
import logging
import os
import re

from flask import Flask, render_template, request, send_file

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
NOT_CHECKED_ERROR_MSG = """You need to check the box acknowledging the data is
complete and verified. Click <a href="javascript:history.back(-1)">here</a> to
go back."""

LOGGING_PATH = "get_bc9.log"
LOGGING_LEVEL = logging.DEBUG
logging.basicConfig(level=LOGGING_LEVEL, filename=LOGGING_PATH)

class Person:
    """Sets up for a person with their 5 details."""
    def __init__(self, Name, Address, Telephone, Email, Position):
        self.name = Name
        self.address = Address
        self.telephone = Telephone
        if validate_email(Email):
            self.email = Email
        else:
            raise Exception()
        self.position = Position

    def has_bcmd_address(self):
        """Checks that the Person has a BCMD email address."""
        return self.email[-14:] == "@bcmainland.ca"


def validate_email(email: str) -> bool:
    """Validates that the email provided is a valid format"""
    return re.fullmatch(EMAIL_REGEX, email)


def add_to_database(data: dict) -> bool:
    """Adds the data to the database"""
    filename = os.path.join(os.path.relpath("bc9_outputs"),
                            data.get("uuid") + ".json")
    with open(filename, "w", encoding='utf-8') as output_file_handle:
        json.dump(data, output_file_handle)
    logging.info("Wrote file %s", filename)


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
        return NOT_CHECKED_ERROR_MSG, 400
    president = Person(Name=data['pres_name'],
                       Address=data['pres_address'],
                       Position="President",
                       Email=data['pres_email'],
                       Telephone=data['pres_tel'])
    vp1 = Person(Name=data['vp1_name'],
                 Address=data['vp1_address'],
                 Position="1st Vice President",
                 Email=data['vp1_email'],
                 Telephone=data['vp1_tel'])
    vp2 = Person(Name=data['vp2_name'],
                 Address=data['vp2_address'],
                 Position="2nd Vice President",
                 Email=data['vp2_email'],
                 Telephone=data['vp2_tel'])
    treasurer = Person(Name=data['treasurer_name'],
                       Address=data['treasurer_address'],
                       Position="Treasurer",
                       Email=data['treasurer_email'],
                       Telephone=data['treasurer_tel'])
    secretary = Person(Name=data['secretary_name'],
                       Address=data['secretary_address'],
                       Position="Secretary",
                       Email=data['secretary_email'],
                       Telephone=data['secretary_tel'])
    vsc = Person(Name=data['vsc_name'],
                 Address=data['vsc_address'],
                 Position="Volunteer Screening Coordinator",
                 Email=data['vsc_email'],
                 Telephone=data['vsc_tel'])
    people = [president, vp1, vp2, treasurer, secretary, vsc]
    for i in range(100):
        index = i.__str__()
        if request.form.getlist('extra_name_' + index).__str__() != "[]":
            extra_person = Person(data['extra_name_' + index],
                data['extra_address_' + index],
                data['extra_tel_' + index],
                data['extra_email_' + index],
                data['extra_position_' + index])
            people.append(extra_person)
    add_to_database(data)
    return render_template('response.html', form=request.form, people=people)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
