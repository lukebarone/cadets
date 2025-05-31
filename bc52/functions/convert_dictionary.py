"""Function(s) to convert a raw `data:dict` into a pretty-printed format"""
from __future__ import annotations
import re

DATA_KEYS_REQUIRED = ['corps', 'co_name',
                      'co_phone', 'uuid', 'submitted_date',
                      'amount_payable', 'people_count']

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
Branch Name: {data['corps']}
CO Name: {data['co_name']} ({data['co_phone']})
"""
    for names in data.keys():
        if names.startswith("personnel_name"):
            array_number = get_trailing_number(names)
            message += f"""Candidates: {data['personnel_rank_' + array_number]} {data['personnel_name_' + array_number]} / {data['personnel_type_' + array_number]} / {data['personnel_allergy_' + array_number]}"""
    message += f"""
Amount Payable - ${data['amount_payable']}
Total people attending: {data['people_count']}
"""
    return message, True


def get_trailing_number(string_to_check: str) -> int:
    """For the input `s`, get the trailing number, or `None` if it can't"""
    matches = re.search(r'\d+$', string_to_check)
    return int(matches.group()) if matches else None

#if __name__=='__main__':
#    print(valid_keys(luke_data))
#    print(convert_for_email(luke_data)[0])