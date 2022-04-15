#!/usr/bin/env python3
"""Returns web page for each JSON file

To run regression tests:

python3 -m doctest Untitled-1.py"""
import json
import os

import jinja2
from models import person

def entry_point(uuid: str):
    """Function description
    
    >>> entry_point(9, 4)
    165
    
    >>> entry_point(2, 3)
    3
    """
    filename = os.path.join(os.path.relpath("bc9_outputs"),
                            uuid + ".json")
    data = {}
    with open(filename, "r", encoding='utf-8') as input_file_handle:
        data = json.load(input_file_handle)
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
    # for i in range(100):
    #     index = i.__str__()
    #     if data.getlist('extra_name_' + index).__str__() != "[]":
    #         extra_person = person.Person(data['extra_name_' + index],
    #             data['extra_address_' + index],
    #             data['extra_tel_' + index],
    #             data['extra_email_' + index],
    #             data['extra_position_' + index])
    #         people.append(extra_person)
    template_format = '''
Branch Name: {{ branch_name }}
Mailing Address: {{ branch_mailing_address }}
General Meetings held on {{ bgm_dow }} from {{ bgm_start_time }} to {{ bgm_end_time }}.

Personnel:
   President: {{ pres_name }} [{{ pres_email }}]
       Phone: {{ pres_tel }}
     Address: {{ pres_address }}
 
   1st Vice:  {{ vp1_name }}   [{{ vp1_email }}]
      Phone:  {{ vp1_tel }}
    Address:  {{ vp1_address }}
 
   2nd Vice:  {{ vp2_name }}   [{{ vp2_email }}]
      Phone:  {{ vp2_tel }}
    Address:  {{ vp2_address }}

  Treasurer:  {{ treasurer_name }}   [{{ treasurer_email }}]
      Phone:  {{ treasurer_tel }}
    Address:  {{ treasurer_address }}

  Secretary:  {{ secretary_name }}   [{{ secretary_email }}]
      Phone:  {{ secretary_tel }}
    Address:  {{ secretary_address }}

  Volunteer Screening Coordinator:  {{ vsc_name }}   [{{ vsc_email }}]
      Phone:  {{ vsc_tel }}
    Address:  {{ vsc_address }}

Compliance:
  Last AGM Date: {{ last_agm_date }}
  Financial Year-End: {{ financial_year_end }}
  Submitted financials to BCMD: {{ submitted_financials }}

{% if nlcc_corps == "yes" %}Navy League Corps: Yes
  {{ nlcc_corps_and_number }}
  Commanding Officer: {{ nlcc_co }}
  Officers registered in Roll Call: {{ nlcc_in_rollcall }}{% endif %}

{% if rcscc_corps == "yes" %}Sea Cadet Corps: Yes
  {{ rcscc_corps_and_number }}
  Commanding Officer: {{ rcscc_co }}{% endif %}

{% if additional_comments is defined and additional_comments %}Additional comments supplied:
{{ additional_comments }}{% endif %}
Information assumed accurate by the date {{ submitted_date }}
    '''
    template = jinja2.Template(template_format)
    output = template.render(data)
    print(output)
    return output


def main():
    """Main entry point"""
    uuid = input("UUID: ")
    if not os.path.exists(os.path.join(os.path.relpath("bc9_outputs"), uuid + ".json")):
        print("Path or file does not exist")
        exit(1)
    entry_point(uuid)
    
    
if __name__ == "__main__":
    main()
