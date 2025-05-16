"""Dinner Guest object for OTC registration purposes."""
class Dinner_Guest:
    """Sets up for a person with their details."""
    def __init__(self, name, allergy=None):
        self.name = name
        self.allergy = allergy
