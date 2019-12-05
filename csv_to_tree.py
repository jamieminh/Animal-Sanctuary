import csv
from AVL_tree import AVLTree
from Date import date_format
from Animal import Pet, WildAnimal, Treatment

pet_tree = AVLTree()
wild_animals_tree = AVLTree()
treatment_tree = AVLTree()

with open("csv_files\\PETS.csv") as file:
    reader = csv.reader(file)
    next(reader)  # index is the list of headers in the first line of the csv file

    for row in reader:
        san_id, animal_type, breed, vacc, neut, microchip, entry_reason, arr_date, dep_date, dest, dest_address = row

        arr_date = date_format(arr_date)
        dep_date = date_format(dep_date)

        pet = Pet(san_id, animal_type, vacc, entry_reason, arr_date, dep_date, dest, dest_address, breed, neut,
                  microchip)
        pet_tree.insert(pet)

with open("csv_files\\WILD ANIMALS.csv") as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        san_id, animal_type, vacc, entry_reason, arr_date, dep_date, dest, dest_address = row

        arr_date = date_format(arr_date)
        dep_date = date_format(dep_date)

        wild_an = WildAnimal(san_id, animal_type, vacc, entry_reason, arr_date, dep_date, dest, dest_address)
        wild_animals_tree.insert(wild_an)

with open("csv_files\\TREATMENTS.csv") as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        san_id, surgery, sur_date, med, med_start, med_fin, abuse, abandon = row

        sur_date = date_format(sur_date)
        med_start = date_format(med_start)
        med_fin = date_format(med_fin)

        treat = Treatment(san_id, surgery, sur_date, med, med_start, med_fin, abuse, abandon)
        treatment_tree.insert(treat)

