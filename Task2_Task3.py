from Animal import Pet, WildAnimal, Treatment
from csv_to_tree import pet_tree, wild_animals_tree, treatment_tree
from Date import *
from AVL_tree import AVLTree, NodePerson
import csv


# ***************   Task2   *********************
# A. Create new entry
def new_entry(category):
    san_id = input("Sanctuary ID: ").lower().upper()

    # If user want to create new entry on Pets or Wild Animal
    if category != 'treatment':
        animal_type = input("Type: ").lower().capitalize()
        vacc = input("Vaccinated (Yes or leave blank): ").lower().capitalize()
        reason_entry = input("Reason for entry: ").lower().title()
        date_arr = date_format(input("Date of Arrival (DD/MM/YY): "))
        date_dep = date_format(input("Date of Departure (DD/MM/YY) or leave blank: "))

        dest, dest_address = "", ""
        # if date of departure is specified, ask for destination and destination address
        if str(date_dep) != "":
            print(date_dep)
            dest = input("Destination:")
            dest_address = input("Destination Address: ")

        # if user want to create new entry on PETS
        if category == 'pet':
            breed = input("Breed of Pet: ").lower().capitalize()
            neut = input("Neutered ('Yes' or leave blank): ").lower().capitalize()
            microchip = input("Microchip (Leave blank if pet have not been microchipped): ").capitalize()

            pet = Pet(san_id, animal_type, vacc, reason_entry, date_arr, date_dep, dest, dest_address, breed, neut, microchip)
            pet_tree.insert(pet)
            # Append the new entry to csv file
            with open("csv_files\\PETS.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(file_attributes('pet', pet))

        # if user want to create new entry on WILD ANIMALS
        elif category == 'wild animal':
            wild_animal = WildAnimal(san_id, animal_type, vacc, reason_entry, date_arr, date_dep, dest, dest_address)
            wild_animals_tree.insert(wild_animal)
            # Append the new entry to csv file
            with open("csv_files\\WILD ANIMALS.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(file_attributes('wild animal', wild_animal))

    # If user want to create new entry on TREATMENT
    else:
        sur = input("Enter Surgery details: ").lower().title()
        sur_date = date_format(input("Enter Surgery Date(DD-MM-YY): "))
        med = input("Enter Medication: ").lower().title()
        med_start = date_format(input("Enter Medication Start Date (DD/MM/YY): "))
        med_fin = date_format(input("Enter Medication Finish Date (DD/MM/YY): "))
        abuse = input("Enter Name of Person Responsible for Abuse: ").lower().title()
        abandon = input("Enter Name of Person Responsible for Abandon: ").lower().title()

        treatment = Treatment(san_id, sur, sur_date, med, med_start, med_fin, abuse, abandon)
        treatment_tree.insert(treatment)
        with open("csv_files\\TREATMENTS.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(file_attributes('treatment', treatment))

    print("Insertion with animal ID " + san_id + " successful.")

# B. Find full data for an animal using sanctuary ID
def find_animal(file_type, id):
    if file_type == 'pet':
        return pet_tree.search(id.upper())
    elif file_type == 'wild animal':
        return wild_animals_tree.search(id.upper())
    else:
        return treatment_tree.search(id.upper())

# C/D: List of people that have abused/abandoned their animals in alphabetical order
def abused_abandoned_list(crime):
    people_crime = AVLTree()

    # function to recursively look for abusers or abandoners and add them to the list
    def in_order_recur(node):
        if node is None:
            return

        in_order_recur(node.left)
        if crime == 'abuse':
            person = node.animal.abuse
        else:
            person = node.animal.abandon

        if person != "" and ("not exist" in people_crime.search(person, "person")):
            people_crime.insert(person, "person")

        in_order_recur(node.right)

    in_order_recur(treatment_tree.root)
    return people_crime

# E/F. List of Cats/Dogs ready for adoption
def pets_adoption(pet_type):
    adopt_ready = AVLTree()

    # function to recursively look for cats or dogs and add them to the tree
    def in_order_recur(node):
        if node is None:
            return
        in_order_recur(node.left)
        if node.animal.animal_type == pet_type \
                and node.animal.vacc \
                and node.animal.neut\
                and node.animal.microchip:
            adopt_ready.insert(node.animal)
        in_order_recur(node.right)

    in_order_recur(pet_tree.root)
    return adopt_ready

# G. List of Pets, Wild Animals ready to be returned to owners in ascending order of sanctuary id, pets first
def return_to_owner():
    return_ready = AVLTree()

    def check_ready(curr_root):
        if curr_root is None:
            return 0
        check_ready(curr_root.left)
        an = curr_root.animal

        if an.vacc and str(an.dest) == "":
            treat = treatment_tree.search(an.san_id)
            # if animal is NOT in treatment, or in treatment but med_fin is specified, it can go
            if type(treat) == str or (type(treat) != str and str(treat.med_fin) != ""):
                if (type(an) == Pet and an.reason not in ["Abused", "Abandoned", "Stray"])\
                        or (type(an) == WildAnimal and an.reason == 'Lost'):
                    return_ready.insert(an)

        check_ready(curr_root.right)

    check_ready(pet_tree.root)
    check_ready(wild_animals_tree.root)

    return return_ready


# ******************* TASK 3 ***********************
# A. Enter details of surgery
def enter_surgery(id):
    id = id.upper()
    # search for animal
    animal = treatment_tree.search(id)
    # if animal does not exist
    if type(animal) == str:
        print(animal)
        return

    if animal.surgery:
        print("Animal with ID " + id + " has already had surgery details. You cannot change it.")
        return
    else:
        while True:
            # if user input blank string, try again
            surgery = input("Enter details of surgery: ")
            sur_date = date_format(input("Enter date of surgery (DD-MM-YY): "))

            if surgery and sur_date:
                break
        animal.surgery = surgery
        animal.sur_date = sur_date

        write_to_file("treatment")

# B. Enter details of neutering
def enter_neutering(id):
    id = id.upper()
    animal = pet_tree.search(id)
    if type(animal) == str:
        print(animal)
        return

    if animal.neut == 'Yes':
        print("Animal with ID " + id + " has already been neutered. You cannot change it.")
    else:
        animal.neut = 'Yes'
        write_to_file('pet')
        print("Neutering details of Pet with ID " + id + " has been changed to: Yes ")

# C. Enter Pet microchip number
def enter_microchip(id):
    id = id.upper()
    animal = pet_tree.search(id)
    if type(animal) == str:
        print(animal)
        return

    if animal.microchip:
        print("Pet with ID " + id + " has already had a microchip. You cannot change it.")
    else:
        detail = input("Enter Microchip Number (D + 6 digits): ").upper()
        while len(detail) != 7 and detail[0] != 'D':
            detail = input("Please Enter correct format of Microchip number (D + 6 digits):")
        animal.microchip = detail
        write_to_file('pet')

        print("Microchip Number of Pet with ID " + id + " is now: " + animal.microchip)

# D. Edit Date of Departure from Sanctuary
def edit_depart_date(id):
    id = id.upper()
    animal = check_ID(id)
    if type(animal) == str:
        print(animal)
        return

    print("The current Date of Departure of animal with ID " + id + " is: " +
          (str(animal.date_dep) if str(animal.date_dep) else "blank"))

    date = date_format(input("Enter new Date (DD-MM-YY) or leave blank: "))
    animal.date_dep = date

    # if departure date is not specified, destination and destination address will also be blank
    if str(date) == "":
        animal.dest = ""
        animal.dest_address = ""
    # if departure date is specified, destination and its address must also be specified
    else:
        # if destination and its address have not previously been specified
        if not animal.dest and not animal.dest_address:
            while True:
                dest = input("Specify the Destination: ")
                dest_address = input("Specify Destination Address: ")
                if dest and dest_address:
                    break
            animal.dest = dest
            animal.dest_address = dest_address

    if type(animal) == Pet:
        write_to_file('pet')
    else:
        write_to_file('wild animal')

    print("Date of Departure of Animal with ID " + id + " is now: " +
          (str(animal.date_dep) if str(animal.date_dep) != "" else "blank"))
    print("Destination and Destination Address upon departure is currently: " +
          (animal.dest if animal.dest != "" else "blank") + " and " +
          (animal.dest_address if animal.dest_address != "" else "blank"))

# E. Edit Destination of the animal upon departure
def edit_dest(id):
    id = id.upper()
    animal = check_ID(id)
    if type(animal) == str:
        print(animal)
        return

    if str(animal.date_dep) == "":
        print("Date of departure of animal must be specified first.\n")
        edit_depart_date(id)
        return

    print("The current Destination and Destination Address of animal with ID " + id + " is: " +
          (animal.dest if animal.dest else "blank") + " and " +
          (animal.dest_address if animal.dest_address else "blank"))

    dest = input("Enter new Destination or Leave blank: ")
    animal.dest = dest

    # if dest is specified, ask for address
    if dest:
        # loop until user has specified the address
        while True:
            dest_address = input("Enter Destination address")
            if dest_address:
                break
        animal.dest_address = dest_address
    # if dest is not specified, address will be blank
    else:
        animal.date_dep = Date()
        animal.dest_address = ""

    if id[0] == 'P':
        write_to_file('pet')
    else:
        write_to_file('wild animal')

    print("The current Destination and Destination Address  of animal with ID " + id + " is now: " +
          (animal.dest if animal.dest else "blank") + " and " +
          (animal.dest_address if animal.dest_address else "blank"))


# ***************** Other Functions *******************
# Function to check user input ID:
def check_ID(id):
    if id[0] == 'P':
        return pet_tree.search(id)
    elif id[0] == 'W':
        return wild_animals_tree.search(id)
    else:
        return False

# function to return a list of attributes of each file
def file_attributes(file_type, an):
    if file_type == 'pet':
        return [an.san_id, an.animal_type, an.breed, an.vacc, an.neut, an.microchip,
                an.reason, an.date_arr, an.date_dep, an.dest, an.dest_address]
    elif file_type == 'wild animal':
        return [an.san_id, an.animal_type, an.vacc, an.reason,
                an.date_arr, an.date_dep, an.dest, an.dest_address]
    else:
        return [an.san_id, an.surgery, an.sur_date, an.med,
                an.med_start, an.med_fin, an.abuse, an.abandon]

# function to write a whole AVL tree to a specific file
def write_to_file(file_type):
    # method to write in data in-order (ascending order of animal id)
    def in_order_recur(node):
        if node is None:
            return 0
        in_order_recur(node.left)
        an = node.animal
        writer.writerow(file_attributes(file_type, an))
        in_order_recur(node.right)

    if file_type == 'pet':
        file = "csv_files\\PETS.csv"
    elif file_type == 'wild animal':
        file = "csv_files\\WILD ANIMALS.csv"
    else:
        file = "csv_files\\TREATMENTS.csv"

    with open(file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        if file_type == 'pet':
            writer.writerow(["Sanctuary Identification", "Type", "Breed", "Vaccinated",
                             "Neutered", "Microchip", "Reason for Entry", "Date of Arrival",
                             "Date of Departure", "Destination", "Destination Address"])
            in_order_recur(pet_tree.root)
        elif file_type == 'wild animal':
            writer.writerow(["Sanctuary Identification", "Type", "Vaccinated", "Reason for Entry",
                             "Date of Arrival", "Date of Departure", "Destination", "Destination Address"])
            in_order_recur(wild_animals_tree.root)
        else:
            writer.writerow(["Sanctuary Identification", "Surgery", "Surgery Date", "Medication", "Medication Start",
                             "Medication Finish", "Responsible for Abuse", "Responsible for Abandoning"])
            in_order_recur(treatment_tree.root)

# function to print all data of a file
def print_full(file_type):
    if file_type == "pet":
        print("-" * 200 + "\nINFORMATION ON PETS")
        return pet_tree.in_order()
    elif file_type == 'wild animal':
        print("-" * 200 + "\nINFORMATION ON WILD ANIMALS")
        return wild_animals_tree.in_order()
    else:
        print("-" * 200 + "\nINFORMATION ON TREATMENTS")
        return treatment_tree.in_order()


# Menu:
if __name__ == "__main__":
    def menu():
        print("-"*100 + "\n---Good day! What do you want to do?---")
        print("     Enter anything else to Exit Application.\n"
              "     1. See full data on Pets\n"
              "     2. See full data on Wild Animals\n"
              "     3. See full data on Treatments\n"
              "     4. Create a new entry (Pets, Wild Animal, Treatments).\n"
              "     5. Get full information of an animal.\n"
              "     6. See list of identified people that have abused animals.\n"
              "     7. See list of identified people that have abandoned animals.\n"
              "     8. See list of Cats that are ready for adoption.\n"
              "     9. See list of Dogs that are ready for adoption.\n"
              "     10. See list of Animals ready to be returned to owners.\n"
              "     11. Edit details of surgery.\n"
              "     12. Edit details of neutering.\n"
              "     13. Edit microchip number.\n"
              "     14. Edit Date of Departure from the sanctuary.\n"
              "     15. Edit Destination of the animal upon departure.\n"
              )

        cmd = int(input())
        if cmd == 1:
            print_full('pet')
        elif cmd == 2:
            print_full('wild animal')
        elif cmd == 3:
            print_full('treatment')
        elif cmd == 4:
            category = int(input("Which type of entry do you want to add?"
                                 "\n    1. Pet.\n    2. Wild Animal.\n    3. Treatment.\n"
                                 "--- Enter anything else to go return to Main Menu. ---\n"))
            if category == 1:
                new_entry('pet')
            elif category == 2:
                new_entry('wild animal')
            elif category == 3:
                new_entry('treatment')
            else:
                menu()
                return
        elif cmd == 5:
            print("What do you want to find, choose your number: ")
            file_type = int(input("    1. Pets\n    2. Wild Animals\n    3. Treatments\n"
                                  "--- Enter anything else to go return to Main Menu. ---\n"))
            if file_type == 1:
                file_type = 'pet'
            elif file_type == 2:
                file_type = 'wild animal'
            elif file_type == 3:
                file_type = 'treatment'
            else:
                menu()
                return

            san_id = input("Enter animal Sanctuary ID: ")
            print(find_animal(file_type, san_id))

        elif cmd == 6:
            print("List of people that have abused animal: ")
            abused_abandoned_list('abuse').in_order("person")
        elif cmd == 7:
            print("List of people that have abandoned animal: ")
            abused_abandoned_list('abandon').in_order("person")
        elif cmd == 8:
            print("List of Cats ready for adoption: ")
            pets_adoption('Cat').in_order()
        elif cmd == 9:
            print("List of Dogs ready for adoption: ")
            pets_adoption('Dog').in_order()
        elif cmd == 10:
            return_to_owner().in_order()
        elif cmd == 11:
            san_id = input("Enter Animal ID: ")
            enter_surgery(san_id)
        elif cmd == 12:
            san_id = input("Enter Pet ID: ")
            enter_neutering(san_id)
        elif cmd == 13:
            san_id = input("Enter Pet ID: ")
            enter_microchip(san_id)
        elif cmd == 14:
            san_id = input("Enter Animal ID: ")
            edit_depart_date(san_id)
        elif cmd == 15:
            san_id = input("Enter Animal ID: ")
            edit_dest(san_id)
        else:
            return

        again = input("\nDo you want to work on something else? (Yes/No): ")
        if again.lower() == 'yes':
            menu()
    menu()
