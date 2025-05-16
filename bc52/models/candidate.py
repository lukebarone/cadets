"""Candidate object for OTC registration purposes."""
class Candidate:
    """Sets up for a person with their details."""
    def __init__(self, name, type, time_in, rank, allergy, years_in_otc, drill,
                 gender,
                 prev_co=False, prev_xo=False, prev_admino=False, prev_trgo=False,
                  prev_instructor=False, medical=None):
        self.name = name
        self.type = type
        self.time_in = time_in
        self.rank = rank
        self.allergy = allergy
        self.years_in_otc = years_in_otc
        self.drill = drill
        self.gender = gender
        self.prev_co = prev_co
        self.prev_xo = prev_xo
        self.prev_admino = prev_admino
        self.prev_trgo = prev_trgo
        self.prev_instructor = prev_instructor
        self.medical = medical
        
