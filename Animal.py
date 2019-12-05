from Date import Date
from Restrict import check_attribute


@check_attribute
class Animal():
    san_id = str
    animal_type = str
    vacc = str
    reason = str
    date_arr = Date
    date_dep = Date
    dest = str
    dest_address = str

    def __init__(self, san_id: str, animal_type: str, vacc: str, reason: str,
                 date_arr: Date, date_dep: Date, dest="", dest_address=""):
        self.san_id = san_id
        self.animal_type = animal_type
        self.vacc = vacc
        self.reason = reason
        self.date_arr = date_arr
        self.date_dep = date_dep
        self.dest = dest
        self.dest_address = dest_address
        # self.status = status

    def __str__(self):
        return "{:<20}: {}\n{:<20}: {}\n{:<20}: {}\n{:<20}: {}\n{:<20}: {}\n{:<20}: {}\n{:<20}: {}\n{:<20}: {}\n" \
            .format("Sanctuary ID", self.san_id, "Type", self.animal_type, "Vaccinated", self.vacc,
                    "Reason for Entry", self.reason, "Date of Arrival", str(self.date_arr),
                    "Date of Departure", str(self.date_dep), "Destination", self.dest,
                    "Destination Address", self.dest_address)


@check_attribute
class Pet(Animal):
    breed = str
    neut = str
    microchip = str

    def __init__(self, san_id, animal_type, vacc, reason, date_arr, date_dep, dest, dest_address, breed, neut,
                 microchip):
        super(Pet, self).__init__(san_id, animal_type, vacc, reason, date_arr, date_dep, dest, dest_address)
        self.breed = breed
        self.neut = neut
        self.microchip = microchip

    def __str__(self):
        return "{:<20}: {}\n{:<20}: {}\n{:<20}: {}\n{:<20}: {}\n{:<20}: {}\n{:<20}: {}\n{:<20}: {}\n{:<20}: {}\n" \
               "{:<20}: {}\n{:<20}: {}\n{:<20}: {}\n" \
            .format("Sanctuary ID", self.san_id, "Type", self.animal_type, "Breed", self.breed, "Vaccinated", self.vacc,
                    "Neutered", self.neut, "Microchip", self.microchip, "Reason for Entry", self.reason,
                    "Date of Arrival", str(self.date_arr), "Date of Departure", str(self.date_dep),
                    "Destination", self.dest, "Destination Address", self.dest_address)



@check_attribute
class WildAnimal(Animal):
    # no need for __init__ because WildAnimal have no other Attributes
    pass

@check_attribute
class Treatment:
    san_id = str
    surgery = str
    sur_date = Date
    med = str
    med_start = Date
    med_fin = Date
    abuse = str
    abandon = str

    def __init__(self, san_id, surgery, sur_date, med, med_start, med_fin, abuse, abandon):
        self.san_id = san_id
        self.surgery = surgery
        self.sur_date = sur_date
        self.med = med
        self.med_start = med_start
        self.med_fin = med_fin
        self.abuse = abuse
        self.abandon = abandon

    def __str__(self):
        return "{:<30}: {}\n{:<30}: {}\n{:<30}: {}\n{:<30}: {}\n{:<30}: {}\n{:<30}: {}\n{:<30}: {}\n{:<30}: {}\n"\
            .format("Sanctuary ID", self.san_id, "Surgery", self.surgery, "Surgery Date", str(self.sur_date),
                    "Medication", self.med, "Medication Start", str(self.med_start),
                    "Medication Finish", str(self.med_fin), "Responsible for Abuse", self.abuse,
                    "Responsible for Abandoning", self.abandon)
