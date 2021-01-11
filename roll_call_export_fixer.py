"""Script to take Roll Call GSuite Export and get it actually ready for import
into Google Admin.

Arguements:
    filename.csv - File name, in this existing folder, to read from.

Outputs:
    results.csv - File to upload to Google Admin
"""
import csv
import os
import sys

import phonenumbers
from phonenumbers import NumberParseException
from email_validator import EmailNotValidError, validate_email


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
def main(argv):
    """Main sub for the program."""
    my_file = os.path.join(THIS_FOLDER, f'{argv}')
    with open(f'{my_file}', "r", newline='') as source:
        rdr = csv.reader(source)
        line_number = 0
        error_count = 0
        with open("result.csv", "w") as result:
            wtr = csv.writer(result)
            for row in rdr:
                line_number += 1
                use_blank_phone = False
                if line_number == 1:
                    wtr.writerow((
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                        row[7], row[8], row[9], row[10], row[11], row[12],
                        row[13], row[14], row[15], row[16], row[17], row[18],
                        row[19], row[20], row[22], row[23], row[24], row[25]))
                    continue
                # All but column 21 (V - Cost Centre)
                email = row[0].split(' ', 1)[0] + \
                    row[1].split(' ', 1)[0] + \
                    '@navyleagueofcanada.org'
                try:
                    _ = validate_email(email)
                    email = _.email.lower()
                except EmailNotValidError:
                    print(f"{line_number} - Invalid email supplied - {email}"
                          ". Skipping entry...")
                    error_count += 1
                    continue
                password = '!G00gle' + row[0][0].upper() + row[1][0].upper()
                if row[5] == "/NLCC 142 Aurora":
                    orgunit = "/BCMD/NLCC Aurora"
                if row[5] == "/NLCC Captain Rankin":
                    orgunit = "/BCMD/NLCC Captain Rankin"
                if row[5] == "/NLCC 78 MJ Miller":
                    orgunit = "/BCMD/NLCC MJ Miller"
                if row[5] == "/NLCC 125 Columbia":
                    orgunit = "/BCMD/NLCC Columbia"
                if row[10] == "+1" or row[10] == "1":
                    if row[11] != "--":
                        row[10] = "+1" + row[11]
                    else:
                        use_blank_phone = True
                        print(f"Line {line_number} - Using blank telephone number")
                if use_blank_phone:
                    phonenumber = ""
                else:
                    try:
                        phonenumber = phonenumbers.format_number(
                            phonenumbers.parse(row[10], 'US'),
                            phonenumbers.PhoneNumberFormat.E164)
                    except NumberParseException:
                        phonenumber = ""
                        print(f"Line {line_number} - Using blank telephone number (exception)")
                wtr.writerow((
                    row[0], row[1], email, password, row[4], orgunit, row[6],
                    row[7], row[8], row[9], phonenumber, row[11], row[12],
                    row[13], row[14], row[15], row[16], row[17], row[18],
                    row[19], row[20], row[22], row[23], row[24], row[25]))
    print(f"Completed! {line_number} lines inputted; {error_count} error(s)")

if __name__ == '__main__':
    main(sys.argv[1])
