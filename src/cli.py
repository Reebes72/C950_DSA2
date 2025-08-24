from datetime import datetime, timedelta
from data_structure.hashTable import HashTable
from classes.package import Package

def main_menu(table: HashTable, trucks: list):
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


def general(table: HashTable, trucks: list):
    report_time: datetime = prompt_time()
    print("!!!!!!!!!!!!!!!!!!!!")
    print("Generated report on packages at " + report_time.strftime("%I:%M %p"))
    print("!!!!!!!!!!!!!!!!!!!!")
    for package in range(1, len(table.hashMap) + 1):
        if package is not None:
            display_query(table, package, report_time)
    print_mileage(trucks, report_time)
    main_menu(table, trucks)


def print_mileage(trucks: list, report_time: datetime):
    report_timedelta = timedelta(hours=report_time.hour, minutes=report_time.minute)
    total_mileage = 0
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


def query(table: HashTable, trucks: list):
    report_time: datetime = prompt_time()
    id = prompt_package_id(table)
    print("!!!!!!!!!!!!!!!!!!!!")
    print("Querying: " + report_time.strftime("%I:%M %p"))
    print("!!!!!!!!!!!!!!!!!!!!")
    display_query(table, id, report_time)
    main_menu(table, trucks)


def display_query(table: HashTable, package_id: int, report_time: datetime):
    package: Package = table.hashSearch(package_id)
    report_delta: timedelta = timedelta(hours=report_time.hour, minutes=report_time.minute)
    package_info: str = f"[Package ID = {package.package_id}]"
    if package.loading_time > report_delta:
        package_info += "\n\tStatus: At Hub"
    elif package.delivery_time > report_delta:
        del_time: datetime = datetime.strptime(str(package.delivery_time), "%H:%M:%S")
        package_info += "\n\t Status: En Route, ETA at " + del_time.strftime("%I:%M %p")
    else:
        del_time: datetime = datetime.strptime(str(package.delivery_time), "%H:%M:%S")
        package_info += "\n\t Status: Delivery time at " + del_time.strftime("%I:%M %p")
    package_info += "\n\tCity: " + package.city
    package_info += "\n\tAddress: " + package.delivery_address
    package_info += "\n\tZIP Code: " + package.zip_code
    package_info += "\n\tPackage Weight: " + str(package.package_weight) + " kilograms"
    package_info += "\n\tDelivery Deadline: " + package.deadline
    print(package_info)


def prompt_time():
    report_time: timedelta = None
    while report_time is None:
        try:
            report_time = datetime.strptime(
                input("Enter a time for the report (format [HOUR:MINUTE AM/PM]): "), "%I:%M %p")
        except:
            print("\tError: Invalid entry. Try again.\n")

    return report_time


def prompt_package_id(table: HashTable):
    package_id = None
    while package_id is None:
        user_input = input("Please enter the ID of the package you would like to view: ")

        if user_input.isdigit():
            if table.hashSearch(int(user_input)) is not None:
                package_id = int(user_input)
            else:
                print("\tNo package found with the provided ID.\n")
        else:
            print("\tError: Invalid input. Please try again.\n")
    return package_id