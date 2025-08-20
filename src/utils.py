import csv

from data_structure.HashTable import HashTable
from classes.package import Package
from classes.truck import Truck
from classes.driver import Driver
from classes.deliveryStatus import deliveryStatus
from datetime import timedelta

DISTANCES_PATH: str = "src/resources/csv/distances.csv"
ADDRESSES_PATH: str = "src/resources/csv/addresses.csv"
DELIVERED_TRACKER: list = []


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
        container: list = [[0 for x in range(addresses)] for y in range(addresses)]
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
def distance_between_addresses(add1: str, add2: str) -> float:
    return DISTANCES[ADDRESSES.index(add1)][ADDRESSES.index(add2)]

# Look at each package's notes, and group packages by those that should be delivered together
def prime_trucks(truck: Truck, table: HashTable):
    package: Package
    delivered_together: list = []
    for package in table.hashMap:
        if package.notes == "":
            continue
        if package.package_id == 9:
            package.delivery_address = "410 S State St"
            package.city = "Salt Lake City"
            package.state = "UT"
            package.zip_code = "84111"
        # Checks for "Must be delivered with" in notes
        # Assigns to first truck
        elif "Must" in package.notes.split():
            note: str = package.notes.replace(',', '')
            delivered_together = [trk for trk in note.split() if trk.isdigit()]
            for together in delivered_together:
                if truck.truck_id == 1 and package.truck_id is None and package not in truck.packages:
                    truck.add_package(package)
                    if package not in DELIVERED_TRACKER:
                        DELIVERED_TRACKER.append(package)
                    package.assign_truck(truck)
        # Checks for "Can only be delivered on specific truck" in notes
        # Assigns to Truck 2
        elif "Can" in package.notes.split():
            required_truck = [trk for trk in package.notes if trk.isdigit()]
            for req in required_truck:
                if int(req) == truck.truck_id and truck.full() is False and package.truck_id is None and package not in truck.packages:
                    truck.add_package(package)
                    if package not in DELIVERED_TRACKER:
                        DELIVERED_TRACKER.append(package)
                    package.assign_truck(truck)
        elif "Delayed" in package.notes.split():
            delayed_until: list = [trk for trk in package.notes if trk.isdigit()]
            if len(delayed_until) == 4:
                time: timedelta = timedelta(hours=int(delayed_until[0] + delayed_until[1]), minutes=int(delayed_until[2] + delayed_until[3]))
            else:
                time: timedelta = timedelta(hours=int(delayed_until[0]), minutes=int(delayed_until[1] + delayed_until[2]))
            if truck.truck_id == 3 and package.truck_id is None and package not in truck.packages:
                truck.add_package(package)
                if package not in DELIVERED_TRACKER:
                    DELIVERED_TRACKER.append(package)                
                package.assign_truck(truck)
                package.delayed_arrival()
    # Adds any packages with same address that is not the same package, to the same truck
    for package in table.hashMap:
        for pack in truck.packages:
            if package.delivery_address == pack.delivery_address and package not in truck.packages:
                package.truck_id = truck.truck_id
                truck.add_package(package)
                if package not in DELIVERED_TRACKER:
                    DELIVERED_TRACKER.append(package)
                package.assign_truck(truck)
                package.delayed_arrival()


def fill_truck(table: HashTable, truck: Truck):
    #sort_truck_packages(table, truck)
    all_on = True
    # count = 0
    while len(truck.packages) < truck.package_limit:
        for package in table.hashMap:
            if package.truck_id is None and len(truck.packages) < 16:
                print(package.truck_id)
                truck.add_package(package)
            elif len(truck.packages) == 16:
                break

            
            # else:
            #     for packages in table.hashMap:
            #         if packages.truck_id == None and len(truck.packages) < 16:
            #             truck.add_package(packages)
        # if len(truck.packages) > 0:
        #     current_package = truck.packages[len(truck.packages)-1]
        #     closest: Package = find_closest_load(current_package.delivery_address, truck.packages[len(truck.packages)-1], table.hashMap, truck)
        # else: 
        #     closest: Package = find_closest_load(truck.hub_address, None, table.hashMap, truck)
        # if closest not in truck.packages and closest is not None:
        #     truck.add_package(closest)
        #     if closest not in DELIVERED_TRACKER:
        #         DELIVERED_TRACKER.append(closest)
        # if closest is not None:
        #     closest.assign_truck(truck)
        #     closest.delayed_arrival()
        #     continue
        for package in table.hashMap:
            if package.on_truck == False and package in DELIVERED_TRACKER:
                all_on = False
        if all_on == True:
            break
            
    array = []
    for p in truck.packages:
        array.append(p.package_id)
    print(array)
    array = []
    sort_truck_packages(table, truck)
    for p in truck.packages:
        array.append(p.package_id)
    print(array)    

# iterates through truck's Packages, finds the nearest stop relative to current
# hub_address, adds to sorted packages list, updates address, and removes the added package
# Replaces truck's packages list with a sorted packages list.
# O(N^2) Complexity
def sort_truck_packages(table: HashTable, truck: Truck):
    sorted_packages = []
    address = truck.hub_address
    truck_packages_left = truck.get_packages()
    current_package: Package = None
    #Gives 14
    closest_to_hub: Package = find_closest_filled(address, truck_packages_left)
    sorted_packages.append(truck_packages_left.pop(truck_packages_left.index(closest_to_hub)))
    current_package = closest_to_hub

    for package in truck_packages_left:
        closest: Package = find_closest_filled(current_package.delivery_address, truck_packages_left)

        if closest not in sorted_packages:
            sorted_packages.append(truck_packages_left.pop(truck_packages_left.index(closest)))
        current_package = closest

    truck.replace_with_sorted_package(sorted_packages)


# Finds out the cloests package within a list of packages and returns it.
# Iterates through package list, checks if the package already has a closest
# package and checks if theres a better distance.
# O(N) Complexity

def find_closest_load(current_address, current_package, packages, truck) -> Package:
    closest_package: Package = None
    best_distance: float = None
    for package in packages:
        if package in truck.packages:
            continue
        if package.truck_id == None and package != current_package:
            addr = package.delivery_address
            dist = distance_between_addresses(addr, current_address)
            if addr == current_address:
                closest_package = package
                return closest_package
            if best_distance is None or dist <= best_distance:
                closest_package = package
                best_distance = dist
    return closest_package


#find the closest package to the truck's location and return it. 
def find_closest_filled(truck_location, packages) -> Package:
    closest_package: Package = None
    best_distance: float = None
    for package in packages:
        # Evaluates the distance of each package against the truck location
        # Value is measured against the current best_distance
        dist = distance_between_addresses(package.delivery_address, truck_location)
        # Prime the closest package with the first in the list, then begin evaluation
        if closest_package == None:
            closest_package = package
            best_distance = distance_between_addresses(truck_location, closest_package.delivery_address)

        # If Duplicate address and a different package, return the package
        if closest_package.delivery_address == truck_location and closest_package is not package:
            return package

        if best_distance is None or dist < best_distance:
            closest_package = package
            best_distance = dist

    return closest_package

# Ingest hash table and trucks list. Checks if packages still need delivered.
# Marks packages as En Route, Removes packages from truck package list
# Increments distance traveled, Returns Trucks to hub, and loads them back up.
# O(N^5) Complexity
def deliver_packages(table: HashTable, trucks: list):
    # curr_add = truck.hub_address
    for truck in trucks:
        truck.set_en_route(table)
        curr_add = truck.hub_address
        for package in truck.packages:
            package.delivery_status = deliveryStatus.DELIVERED
            curr_add = package.delivery_address
            truck.remove_package(
                                package,
                                table, 
                                distance_between_addresses(curr_add, package.delivery_address))
            truck.current_address = curr_add


    for item in table.hashMap:
        if item.delivery_status == deliveryStatus.DELIVERED:
            retry_deliver_packages(table, trucks)
def retry_deliver_packages(table: HashTable, trucks: list):
    # curr_add = truck.hub_address
    
    for truck in trucks:
        fill_truck(table, truck)
        curr_add = truck.current_address
        for package in truck.packages:
            package.delivery_status = deliveryStatus.DELIVERED
            truck.remove_package(
                                package,
                                table, 
                                distance_between_addresses(curr_add, package.delivery_address))
            curr_add = package.delivery_address
            truck.current_address = curr_add
    for item in table.hashMap:
        if item.delivery_status != deliveryStatus.DELIVERED:
            print(item)
            retry_deliver_packages(table, trucks)
                            
# Iterates through hashmap to see if any packages still need to be delivered.
# O(N) Complexity
def deliveries_completed(table: HashTable) -> bool:
    package: Package
    for package in table.hashMap:
        if package is not None and package.delivery_status != deliveryStatus.DELIVERED:
            print("WHY AM I HERE?")
            return False
    return True
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