"""Adds the registration data to an SQLite3 database"""

import json
import pathlib
import sqlite3

connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()
# Create the database
cursor.execute('''
CREATE TABLE IF NOT EXISTS AGMRegistrations (
    uuid Text,
    branch_name Text,
    participant_name Text,
    participant_email Text,
    participant_phone Text,
    personnel_allergy Text,
    is_delegate Text,
    delegate_position Text,
    submitted_date Text,
    book_hotel Text,
    share_room Text
);'''
)

outputs = [f for f in pathlib.Path().glob("*.json")]
columns = ['branch_name', 'participant_name', 'participant_email',
           'participant_phone', 'personnel_allergy', 'is_delegate',
           'delegate_position', 'uuid',
           'submitted_date', 'book_hotel', 'share_room']
for filename in outputs:
    with open(filename, 'r', encoding='utf-8') as file_handle:
        row = json.load(file_handle)
#        print(f"{raw_file=}")
#        for row in raw_file:
        cursor.execute('''
insert into AGMRegistrations (
    uuid,
    branch_name,
    participant_name,
    participant_email,
    participant_phone,
    personnel_allergy,
    is_delegate,
    delegate_position,
    submitted_date,
    book_hotel,
    share_room) 
values(?,?,?,?,?,?,?,?,?,?,?)''',(
row["uuid"],
row["branch_name"],
row["participant_name"],
row["participant_email"],
row["participant_phone"],
row["personnel_allergy"],
row["is_delegate"],
row["delegate_position"],
row["submitted_date"],
row["book_hotel"],
row["share_room"])
        )
        print(f'{row} data inserted successfully')
connection.commit()
connection.close()
