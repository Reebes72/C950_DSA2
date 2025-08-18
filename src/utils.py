import csv

from data_structure.HashTable import HashTable
from classes.package import Package
from classes.truck import Truck
from classes.driver import Driver
from classes.deliveryStatus import deliveryStatus
from datetime import timedelta

DISTANCES_PATH: str = "src/resources/csv/distances.csv"
ADDRESSES_PATH: str = "src/resources/csv/addresses.csv"


# Opens csv, iterates through each line, inserts a Package Object into hashMap
# O(N) Complexity
def initialize_package_file(filename: str) -> list:
    container: HashTable = HashTable()
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            container.hashInsert(Package(line))
    return container


# Returns sum of rows in file
# O(N) Complexity
def number_of_addresses(filename: str) -> int:
    with open(filename, 'r') as file:
        return sum(1 for row in file)


# Opens csv, gets number of addresses, populates container(2D Array) with 0s
# Iterates through entries in CSV, and sets distances
# O(N^2) Complexity
def initialize_distance_file(distancePath: str = DISTANCES_PATH, addressesPath: str = ADDRESSES_PATH) -> list:
    with open(distancePath, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        addresses: int = int(number_of_addresses(addressesPath))
        container: list = [[0 for _ in range(addresses)] for _ in range(addresses)]
        source_address: int = 0
        for address in reader:
            for index in range(addresses):
                if address[index] != "":
                    container[source_address][index] = float(address[index])
                    container[index][source_address] = float(address[index])
            source_address += 1
        return container


# Opens csv, splits address and strips address and inserts street address 
# to the container, returns container.
# O(N) Complexity
def initialize_address_file(filename: str) -> list:
    container: list = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=",")
        for line in reader:
            # full_address = line[0].split(",")
            street = line[1].strip()
            container.append(street)
    return container


DISTANCES: list = initialize_distance_file(DISTANCES_PATH, ADDRESSES_PATH)
ADDRESSES: list = initialize_address_file(ADDRESSES_PATH)

# Gets Constants from main to assign drivers and trucks
# Returns list of driver objects and truck objects
# O(N) Complexity
def initialize_trucks_drivers(trucks: int, drivers: int):
    truck_list: list = []
    driver_list: list = []
    minimum_trucks_or_drivers = min(trucks, drivers)
    for truck in range(1, trucks + 1):
        truck_list.append(Truck(truck))
    for driver in range(1, minimum_trucks_or_drivers + 1, 1):
        driver = Driver(driver)
        driver.getTruck(truck_list)
        driver_list.append(driver)
    return truck_list, driver_list


# Takes 2 addresses, distance and addresses files, returns distance between the two addresses
# O(1) Complexity
def distance_between_addresses(add1: int, add2: int) -> float:
    return DISTANCES[ADDRESSES.index(add1)][ADDRESSES.index(add2)]

# Adds packages to truck and sorts after checking for remaining packages, truck has space and is at hub.
# Handles cases with notes that require address change or must be delivered together
# Sorts the packages in truck for efficient delivery
# O(N^3 Complexity)
def load_truck(table: HashTable, truck: Truck):
    
    print(len(assignable_packages(table, truck)))
    while len(assignable_packages(table, truck)) > 0 and not truck.full() == True and truck.at_hub is True:
        if len(truck.packages) == 0:
            address = truck.hub_address
        else:
            last_package: Package = table.hashSearch(truck.packages[len(truck.packages) - 1])
            address: str = last_package.delivery_address
        closest_package: Package = find_closest(address, assignable_packages(table, truck))
        truck.add_package(closest_package)
        
        #Wrong Address case
        if closest_package.package_id == 9:
            closest_package.delivery_address = "410 S State St"
            closest_package.city = "Salt Lake City"
            closest_package.state = "UT"
            closest_package.zip_code = "84111"
            sort_truck_packages(table, truck)

        
        #Must be delivered together case
        for items in get_associated(table):
            for item in items:
                if str(closest_package.package_id) in str(item.package_id):
                    for associated in items:
                        if associated.on_truck() is False:
                            truck.add_package(associated)
    sort_truck_packages(table, truck)

def fill_truck(table: HashTable, truck: Truck):
    #Sort into lists for trucks
    # together_list: []
    # required_truck_list: []
    # deadline_list: []
    package: Package
    for package in table.hashMap:
        if package.delivery_status is not deliveryStatus.DELIVERED:
            if package.package_id == 9:
                package.delivery_address = "410 S State St"
                package.city = "Salt Lake City"
                package.state = "UT"
                package.zip_code = "84111"
                # sort_truck_packages(table, truck)

            if package.on_truck is False and truck.full() is False:
                #Delivered on specific truck
                if "Can" in package.notes.split():
                    required_truck = [trk for trk in package.notes if trk.isdigit()]
                    for req in required_truck:
                        if int(req) == truck.truck_id:
                            package.truck_id = truck.truck_id
                            truck.add_package(package)
                #Delivered with specific packages
                #Checks for space on the truck
                elif "Must" in package.notes.split():
                    delivered_together = [trk for trk in package.notes if trk.isdigit()]
                    if truck.package_limit - len(truck.packages) >= len(delivered_together):
                        for together in delivered_together:
                            package.truck_id = truck.truck_id
                            truck.add_package(package)
                #Delayed packages
                elif "Delayed" in package.notes.split():
                    delayed_until: list = [trk for trk in package.notes if trk.isdigit()]
                    if len(delayed_until) == 4:
                        time: timedelta = timedelta(hours=int(delayed_until[0] + delayed_until[1]), minutes=int(delayed_until[2] + delayed_until[3]))
                    else:
                        time: timedelta = timedelta(hours=int(delayed_until[0]), minutes=int(delayed_until[1] + delayed_until[2]))
                    if truck.truck_id == 3:
                        package.truck_id = truck.truck_id
                        truck.add_package(package)
                else:
                    package.truck_id = truck.truck_id
                    truck.add_package(package)
    # while len(truck.packages) < truck.package_limit:
    #     #TODO: Case for non-filled truck.


# iterates through truck's Packages, finds the nearest stop relative to current
# hub_address, adds to sorted packages list, updates address, and removes the added package
# Replaces truck's packages list with a sorted packages list.
# O(N^2) Complexity
def sort_truck_packages(table: HashTable, truck: Truck):
    sorted_packages: list = []
    address = truck.hub_address
    packages = truck.get_packages(table)
    while len(packages) != 0:
        closest: Package = find_closest(address, packages)
        sorted_packages.append(closest.package_id)
        address = closest.delivery_address
        packages.remove(closest)
    truck.packages = sorted_packages


# Finds out the cloests package within a list of packages and returns it.
# Iterates through package list, checks if the package already has a closest
# package and checks if theres a better distance.
# O(N) Complexity
def find_closest(address, packages) -> Package:
    closest_package: Package = None
    best_distance: float = None
    for package in packages:
        if package is not None:
            if closest_package is not None:
                closest_package = package
                closest_address = closest_package.delivery_address
                best_distance = distance_between_addresses(closest_address, address)
            else:
                addr = package.delivery_address
                dist = distance_between_addresses(addr, address)
                if best_distance is None or dist < best_distance:
                    closest_package = package
                    best_distance = dist
    return closest_package

# Ingest hash table and trucks list. Checks if packages still need delivered.
# Marks packages as En Route, Removes packages from truck package list
# Increments distance traveled, Returns Trucks to hub, and loads them back up.
# O(N^5) Complexity
def deliver_packages(table: HashTable, trucks: list):
    while deliveries_completed(table) is False:
        for truck in trucks:
            truck.set_en_route(table)
            curr_add = truck.hub_address
            while len(truck.packages) > 0:
                for package in truck.packages:
                    package.delivery_status = deliveryStatus.DELIVERED
                    truck.remove_package(
                                    package,
                                    table, 
                                    distance_between_addresses(curr_add, package.delivery_address))
                    curr_add = package.delivery_address
                    truck.current_address = curr_add
            truck.return_truck(distance_between_addresses(curr_add, truck.hub_address))
        for truck in trucks:
            fill_truck(table, truck)


def unassigned_packages(table: HashTable):
    unassigned_packages = []
    for package in table.hashMap:
        if package is not None and package.truck_assigned() is False:
            unassigned_packages.append(package)

    return unassigned_packages


# Iterates through hashmap to see if any packages still need to be delivered.
# O(N) Complexity
def deliveries_completed(table: HashTable) -> bool:
    package: Package
    for package in table.hashMap:
        if package is not None and package.delivery_status != deliveryStatus.DELIVERED:
            print(package)
            return False
    return True


def assignable_packages(table: HashTable, truck: Truck) -> list:
    unassignable: list = unassignable_packages(table, truck)
    assignable: list = []
    for package in table.hashMap:
        if package is not None and package not in unassignable:
            assignable.append(package)
    return assignable


def unassignable_packages(table: HashTable, truck: Truck) -> list:
    unassignable_packages = []
    associated_package_lists = get_associated(table)
    package: Package
    # Iterate through the Package list
    for package in table.hashMap:
        if package is not None:
            # If a Package is already assigned to a Truck, append it to the list
            if package.on_truck:
                unassignable_packages.append(package)

            # If a Package is required to be on a Truck different from the one passed, add the Package to the
            # unassignable Packages list
            elif package.required_truck() is not None and package.required_truck() is not truck.truck_id:
                unassignable_packages.append(package)

                # If the current unassignable Package ends up in one of the lists of associated Packages, ensure
                # all associated Packages are added to the unassignable Packages list
                if len(associated_package_lists) > 0:
                    for list in associated_package_lists:
                        if str(package.package_id) in str(list[0].package_id):
                            for associated_package in list:
                                if associated_package not in unassignable_packages:
                                    unassignable_packages.append(associated_package)

            # If the Package is delayed and has not arrived at the depot yet, it cannot be assigned to the Truck yet
            elif package.delayed_arrival() is not None and package.delayed_arrival() > truck.time:
                if package not in unassignable_packages:
                    unassignable_packages.append(package)

    return unassignable_packages


def get_associated(table: HashTable):
    associated_package_list = []
    for current_package in table.hashMap:
        if current_package is not None and "Must be delivered with" in current_package.notes:
            # Create a new list of associated Packages that must be delivered with the current Package
            associated_packages = directly_associated(table, current_package)

            # Variables to check if we need to combine lists of associated Packages that must be delivered together
            combine_lists = False
            list_to_combine = None

            # Space-Time Complexity: O(N^2)
            # Check if a Package in the current list already exists in a list that we've appended to the master list
            if len(associated_package_list) > 0:
                for package in associated_packages:
                    for list in associated_package_list:
                        if package in list:
                            combine_lists = True
                            list_to_combine = list
                            break

            # Space-Time Complexity: O(N)
            # If any Packages in the current associated_packages exist in a list that was appended to the master
            # list, do not add a new list but instead add directly to the already created list
            if combine_lists:
                for package in associated_packages:
                    if package not in list_to_combine:
                        list_to_combine.append(package)
            # If none of the Packages in the current associated_packages exist in a list that was appended to the
            # master list, add this as a new list
            else:
                associated_package_list.append(associated_packages)
    return associated_package_list


def directly_associated(table: HashTable, package: Package) -> list:
    if "Must be delivered with" in package.notes:
        associated: list = []
        associated.append(package)
        notes = package.notes.replace(",", " ")
        notes = notes.split()
        ids = [int(id) for id in notes if id.isdigit()]
        for id in ids:
            assoc_package = table.hashSearch(id)
            associated.append(assoc_package)
            #Recursion
            additional = directly_associated(table, assoc_package)
            if additional is not None:
                for add in additional:
                    if add not in associated:
                        associated.append(add)
        return associated