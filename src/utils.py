import csv

from data_structure.HashTable import HashTable
from classes.package import Package
from classes.truck import Truck
from classes.driver import Driver

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
    for truck in range(1, minimum_trucks_or_drivers + 1, 1):
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
# O(N^3 Complexity
def load_truck(table: HashTable, truck: Truck):
    print(len(assignable_packages(table, truck)))
    while len(assignable_packages(table, truck)) > 0 and not truck.full() == True and truck.at_hub is True:
        if len(truck.packages) == 0:
            address = truck.location
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

        
        #Must be delivered together case
        for items in get_associated(table):
            if closest_package in items:
                for associated in items:
                    if associated.on_truck() is False:
                        truck.add_package(associated)
    sort_truck_packages(table, truck)


# iterates through truck's Packages, finds the nearest stop relative to current
# location, adds to sorted packages list, updates address, and removes the added package
# Replaces truck's packages list with a sorted packages list.
# O(N^2) Complexity
def sort_truck_packages(table: HashTable, truck: Truck):
    sorted_packages: list = []
    address = truck.location
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
                if  best_distance is None or dist < best_distance:
                    closest_package = package
                    best_distance = dist
    return closest_package

# Ingest hash table and trucks list. Checks if packages still need delivered.
# Marks packages as En Route, Removes packages from truck package list
# Increments distance traveled, Returns Trucks to hub, and loads them back up.
# O(N^5) Complexity
def deliver_packages(table: HashTable, trucks: list):
    while not deliveries_completed(table):
        for truck in trucks:
            truck.set_en_route(table)
            curr_add = truck.location
            curr_index = 0
            while len(truck.packages) > 0:
                package: Package = table.hashSearch(truck.packages[curr_index])
                truck.remove_package(
                                    table.hashSearch(truck.packages[curr_index]),
                                    table, 
                                    distance_between_addresses(curr_add, package.delivery_address))
            truck.return_truck(distance_between_addresses(curr_add, truck.location))
        for truck in trucks:
            load_truck(table, truck)


def unassigned_packages(table: HashTable):
    unassigned_packages = []
    for package in table.hashMap:
        if package is not None and package.truck_assigned() is False:
            unassigned_packages.append(package)

    return unassigned_packages


# Iterates through hashmap to see if any packages still need to be delivered.
# O(N) Complexity
def deliveries_completed(table: HashTable) -> bool:
    for package in table.hashMap:
        if package is not None and package.delivery_time is None:
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
    unassignable: list = []
    associated_packages: list = get_associated(table)
    for package in table.hashMap:
        if package is not None:
            if package.on_truck:
                unassignable.append(package)
            elif package.truck_id is not None and package.required_truck() is not truck.truck_id:
                unassignable.append(package)
            if len(associated_packages) > 0:
                for item in associated_packages:
                    if package in item:
                        for associated in item:
                            if associated not in unassignable:
                                unassignable.append(associated)
            elif package.delayed_arrival() is not None and package.delayed_arrival() > truck.time:
                if package not in unassignable: 
                    unassignable.append(package)
    return unassignable


def get_associated(table: HashTable):
    associated: list = []
    for curr_package in table.hashMap:
        if curr_package is not None and "Must be delivered with" in curr_package.notes:
            dir_associated = directly_associated(table, curr_package)
            combine: bool= False
            to_combine= []
            if len(associated) > 0:
                for package in dir_associated:
                    for list in associated:
                        if package.package_id == list.package_id:
                            combine = True
                            to_combine.append(list)
                            break
            if combine:
                for package in dir_associated:
                    for item in to_combine:
                        if package.package_id != item.package_id:
                            to_combine.append(package)
                            break
            else:
                for package in dir_associated:
                    associated.append(package)
    return associated


def directly_associated(table: HashTable, package: Package) -> list:
    if "Must be delivered with" in package.notes:
        associated: list = [package]
        notes = package.notes.replace(",", " ")
        notes = notes.split()
        ids = [int(id) for id in notes if id.isdigit()]
        for id in ids:
            package = table.hashSearch(id)
            associated.append(package)
            additional = directly_associated(table, package)
            if additional is not None:
                for add in additional:
                    if add not in associated:
                        associated.append(add)
        return associated