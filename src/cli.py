from datetime import datetime, timedelta
from data_structure.hashTable import hashTable
from classes.truck import Truck

def main_menu(table: hashTable, trucks: list):
    print("!!!!!!!!!!!!!!!!!!!!")
    print("WGU - Parcel Service")
    print(" By: Andrew Reeves")
    print("!!!!!!!!!!!!!!!!!!!!")
    print("Please select a menu option to generate a report or retrieve package information.\n")
    print("\t 1. General Report")
    print("\t 2. Package Query")
    print("\t 3. Exit")
    valid_options = [1, 2, 3]
    option = None

    while option is None:
        user_input = input("\nEnter your option selection here: ")

        if user_input.isdigit() and int(user_input) in valid_options:
            option = int(user_input)
        else:
            print("Error: Invalid option provided.")
    if option == 1: 
        general(table, trucks)
    if option == 2: 
        query(table, trucks)
    if option == 3:
        print("Closing...")
        quit()


def general(table: hashTable, trucks: list):
    report_time: datetime = prompt_time()
    print("!!!!!!!!!!!!!!!!!!!!")
    print("Generated report on packages at " + report_time.strftime("%I:%M %p"))
    print("!!!!!!!!!!!!!!!!!!!!")
    for package in range(1, len(table.hashMap) + 1):
        if package is not None:
            display_package_query(table, package, report_time)
    print_mileage(trucks, report_time)
    main_menu(table, trucks)


def print_mileage(trucks: list, report_time: datetime):
    report_timedelta = timedelta(hours=report_time.hour, minutes=report_time.minute)
    total_mileage = 0
    truck: Truck
    for truck in trucks:
        if len(truck.mileage_times) > 0:
            index = len(truck.mileage_times) - 1
            while index > 0:
                timestamp_mileage = truck.mileage_times[index][0]
                timestamp_timedelta = truck.mileage_times[index][1]
                if timestamp_timedelta <= report_timedelta:
                    total_mileage += timestamp_mileage
                    print("Truck %d's mileage: %0.2f miles" % (truck.truck_id, timestamp_mileage))
                    break
                else:
                    index = index - 1
            if index == 0:
                print("Truck %d's mileage: %0.2f miles" % (truck.truck_id, 0.00))
    print("\nThe total mileage of all trucks at " + report_time.strftime("%I:%M %p") + " is %0.2f miles" % total_mileage)


def query_package():
    pass