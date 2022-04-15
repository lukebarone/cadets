import re

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

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