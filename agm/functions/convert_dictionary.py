"""Function(s) to convert a raw `data:dict` into a pretty-printed format"""
from __future__ import annotations
import re

DATA_KEYS_REQUIRED = ['branch_name', 'participant_name', 'participant_email',
                      'participant_phone', 'is_delegate',
                      'delegate_position', 'uuid', 'submitted_date',
                      'book_hotel', 'share_room', 'amount_payable',
                      'people_count']
luke_data = {'branch_name': 'bcmd',
             'participant_name': 'Luke Barone',
             'participant_email': 'lbarone@bcmainland.ca',
             'participant_phone': '2505527118',
             'personnel_allergy': 'Not really',
             'is_delegate': 'No',
             'delegate_position': 'bcmd_exec',
             'uuid': 'acaad283-b115-455f-89c7-a20c8b7222ca',
             'submitted_date': 'Submitted: 28/6/2023 @ 13:58:28',
             'book_hotel': 'Yes',
             'share_room': 'Yes',
             'amount_payable': 0,
             'people_count': 1}
def valid_keys(data: dict) -> bool:
    """Checks that all the required elements exist"""
    for key_names in DATA_KEYS_REQUIRED:
        if not key_names in data:
            return False
    return True


def convert_for_email(data: dict) -> tuple[str, bool]:
    """Returns the formatted message string, and false if it could not convert."""
    if not valid_keys(data):
        return "", False
    message = f"""
Branch Name: {data['branch_name']}
Participant Name: {data['participant_name']} ({data['participant_email']} / {data['participant_phone']})
Allergy/dietary restrictions: {data['participant_allergy']}
Is the participant the voting delegate? {data['is_delegate']} (Position: {data['delegate_position']})
Should BCMD book the hotel? {data['book_hotel']}
Are the participant(s) willing to share rooms with other people? {data['share_room']}
"""
    for names in data.keys():
        if names.startswith("personnel_name"):
            array_number = get_trailing_number(names)
            message += f"""Additional Personnel: {data['personnel_name_' + array_number]} / {data['personnel_type_' + array_number]} / {data['personnel_allergy_' + array_number]}"""
    message += f"""
Amount Payable (registrations only - Hotel is extra) - ${data['amount_payable']}
Total people attending: {data['people_count']}
"""
    return message, True


def get_trailing_number(string_to_check: str) -> int:
    """For the input `s`, get the trailing number, or `None` if it can't"""
    matches = re.search(r'\d+$', string_to_check)
    return int(matches.group()) if matches else None

if __name__=='__main__':
    print(valid_keys(luke_data))
    print(convert_for_email(luke_data)[0])