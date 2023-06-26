class Person:
    """Sets up for a person with their details."""
    def __init__(self, name, position, participant_type, allergies=None):
        self.name = name
        self.position = position
        self.type = participant_type
        self.allergies = allergies
