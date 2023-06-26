"""
Router and Controller for getting the AGM Registration Forms entered.
"""
import json
import logging
import os

from flask import Flask, render_template, request, send_file
from models import person

# import read_responses
# from mail import send_mail

# Add any error messages here for inclusion in the templates.
# TODO: Above

LOGGING_PATH = "agm.log"
LOGGING_LEVEL = logging.DEBUG
logging.basicConfig(level=LOGGING_LEVEL, filename=LOGGING_PATH)


def add_to_database(data: dict) -> bool:
    """Adds the data to the database"""
    filename = os.path.join(os.path.relpath("agm_registrations"),
                            data.get("uuid") + ".json")
    with open(filename, "w", encoding='utf-8') as output_file_handle:
        json.dump(data, output_file_handle)
    logging.info("Wrote file %s", filename)
#    email_to_send = read_responses.entry_point(data['uuid'])
#    send_mail(email_to_send)


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
    # TODO: Above

    # Get branch info
    branch_name = data['branch_name']
    primary_name = person.Person(data['participant_name'],
                                 data['delegate_position'],
                                 data['is_delegate'],
                                 data['personnel_allergy'])
    primary_email = data['participant_email']
    primary_phone = data['participant_phone']
    uuid = data['uuid']
    submission_date = data['submitted_date']
    additional_comments = data['additional_comments']

    should_book = data['book_hotel']
    share_room = data['share_room']
    total_people = data['people_count']
    total_cost = data['amount_payable']
    people = [primary_name]
    for i in range(100):
        index = i.__str__()
        if request.form.getlist('additional_personnel[' + index + ']').__str__() != "[]":
            extra_person = person.Person(data['personnel_name_' + index],
                data['personnel_position_' + index],
                "No",
                data['personnel_allergy_' + index])
            people.append(extra_person)
    add_to_database(data)
    return render_template('response.html', form=request.form, people=people)

@app.route('/images/BCMD_Crest.png', methods=['GET'])
def load_crest():
    """Returns the crest for an image file"""
    return send_file("images/BCMD_Crest.png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
