#!/usr/bin/env python3
"""Returns web page for each JSON file

To run regression tests:

python3 -m doctest Untitled-1.py"""
import json
import os
import sys

import jinja2

def send_email(email_body: str) -> bool:
    pass

def entry_point(uuid: str) -> str:
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
    #print(output)
    return output


def main(argument:str = None):
    """Main entry point"""
    if argument is None:
        uuid = input("UUID: ")
    else:
        uuid = argument
    if not os.path.exists(os.path.join(os.path.relpath("bc9_outputs"), uuid + ".json")):
        print("Path or file does not exist")
        exit(1)
    send_email(entry_point(uuid))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        main()
    else:
        main(sys.argv[1])
