"""Function(s) to convert a raw `data:dict` into a pretty-printed format"""
from __future__ import annotations
import logging
import re

DATA_KEYS_REQUIRED = ['corps', 'co_name',
                      'co_phone', 'uuid', 'submitted_date',
                      'amount_payable', 'people_count']

def valid_keys(data: dict) -> bool:
    """Checks that all the required elements exist"""
    logging.info("%s - Checking for valid keys", data.get('corps'))
    for key_names in DATA_KEYS_REQUIRED:
        if not key_names in data:
            return False
    logging.info("%s - Returning TRUE for valid_keys", data.get('corps'))
    return True


def convert_for_email(data: dict) -> tuple[str, bool]:
    """Returns the formatted message string, and false if it could not convert."""
    logging.info("%s - Converting data for email; checking if valid keys...", data.get('corps'))
    if not valid_keys(data):
        return "", False
    logging.info("%s - Generating email message...", data.get('corps'))
    message = f"""
Branch Name: {data['corps']}
CO Name: {data['co_name']} ({data['co_phone']})
"""
    logging.info("%s - Created message (%s)", data.get('corps'), message)
    all_keys = data.keys()
    keys = [key for key in all_keys if key.startswith("personnel_name_")]
    for key in keys:
        index = re.search(r'\d+$', key).group(0)
        message += f"""Candidates: {data['personnel_rank_' + index]} {data['personnel_name_' + index]} / {data['personnel_type_' + index]} / {data['personnel_allergy_' + index]}"""
    logging.info("%s - Created message (%s)", data.get('corps'), message)
    keys = [key for key in all_keys if key.startswith("dinner_name_")]
    for key in keys:
        index = re.search(r'\d+$', key).group(0)
        message += f"""Dinner only guests: {data['dinner_name_' + index]} / {data['dinner_allergy_' + index]}"""
    logging.info("%s - Created message (%s)", data.get('corps'), message)

    message += f"""
Amount Payable - ${data.get('amount_payable')}
Total people attending: {data.get('people_count')}
"""
    logging.info("%s - CREATED MESSAGE (%s)", data.get('corps'), message)
    return message, True


def get_trailing_number(string_to_check: str) -> int:
    """For the input `s`, get the trailing number, or `None` if it can't"""
    matches = re.search(r'\d+$', string_to_check)
    return int(matches.group()) if matches else None

#if __name__=='__main__':
#    print(valid_keys(luke_data))
#    print(convert_for_email(luke_data)[0])