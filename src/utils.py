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
def distance_between_addresses(add1: str, add2: str) -> float:
    # return DISTANCES[ADDRESSES.index(add1)][ADDRESSES.index(add2)]
    distance = DISTANCES[ADDRESSES.index(add1)][ADDRESSES.index(add2)]
    if distance == '':
        distance = DISTANCES[ADDRESSES.index(add2)][ADDRESSES.index(add1)]
    return float(distance)

# Supply an address and a list of packages to iterate through. Return the distances the list of packages are from the address.
# O(N) Complexity
def get_distances(address, table):
    address_distances: list = []
    for package in table:
        address_distances.append(distance_between_addresses(address, package.delivery_address))
    return address_distances
        
        
# Look at each package's notes, and group packages by those that should be delivered together
# Manual Assignment to trucks 1,2,3 (delivered together, required truck, and delayed)
# O(N^2) Complexity
def prime_trucks(truck: Truck, table: HashTable):
    package: Package
    delivered_together: list = []
    for package in table.hashMap:
        if package.notes == "":
            pass
        # Checks for "Must be delivered with" in notes
        # Assigns to first truck
        elif "Must" in package.notes.split():
            note: str = package.notes.replace(',', '')
            delivered_together = [trk for trk in note.split() if trk.isdigit()]
            for together in delivered_together:
                if truck.truck_id == 1 and package.truck_id is None:
                    package.truck_id = truck.truck_id
                    truck.add_package(package)
                    package.truck_assigned()
        # Checks for "Can only be delivered on specific truck" in notes
        # Assigns to Truck 2
        elif "Can" in package.notes.split():
            required_truck = [trk for trk in package.notes if trk.isdigit()]
            for req in required_truck:
                if int(req) == truck.truck_id and truck.full() is False and package.truck_id is None:
                    package.truck_id = truck.truck_id
                    truck.add_package(package)
                    package.truck_assigned()
        # Delayed packages are set to truck 3
        elif "Delayed" in package.notes.split():
            if truck.truck_id == 3 and package.truck_id is None:
                package.truck_id = truck.truck_id
                truck.add_package(package)
                package.truck_assigned()
                package.delayed_arrival()
    # Adds any packages with same address to the same truck for efficiency
    for package in table.hashMap:
        for pack in truck.packages:
            if package.delivery_address == pack.delivery_address and package.package_id != pack.package_id:
                package.truck_id = truck.truck_id
                truck.add_package(package)
                package.truck_assigned()
                package.delayed_arrival()
    # Checks for possibility of a package being added multiple times
    for package in truck.packages:
        if truck.packages.count(package) > 1:
            pack = truck.packages.pop(truck.packages.index(package))

# Gets the truck's packages and looks to see which packages haven't been assigned to a truck yet, fills the truck with packages.
# NOTE: Improvements on mileage could be made here by doing a distance search on the best package of available packages
# NOTE: It would increase processing time to do so, likely from O(N) to O(N^2) Complexity
# Complexity O(N)
def fill_truck(table: HashTable, truck: Truck):
    packages_left: list = get_after_prime_packages(table)
    #Tested sort here. Worked fine
    while len(packages_left) != 0 and truck.full() is False:
        for package in packages_left:
            if package.truck_id == None:
                #Added logic in truck to add the truck_id to the package.
                # Logic in Trucks.py to prevent packages from exceeding the limit.
                truck.add_package(package)
                packages_left.remove(package)
    sort_truck_packages(truck.packages, truck)
    # Thought... Maybe you could have it add only one closest package, and send a False value if it's not full.
    # Loop until filled or packages_left is empty and return True.


# Returns the packages that haven't been assigned to a truck yet after priming.  
# Complexity O(N)
def get_after_prime_packages(table: HashTable):
    packages_left: list = []
    for package in table.hashMap:
        if package.truck_id == None:
            packages_left.append(package)
    return packages_left

# iterates through truck's Packages, finds the nearest stop relative to current
# hub_address, adds to sorted packages list, updates address, and removes the added package
# Replaces truck's packages list with a sorted packages list.
# O(N^2) Complexity
def sort_truck_packages(table, truck: Truck):
    unsorted_packages: list = truck.packages.copy()
    sorted_packages: list = []
    address = truck.hub_address
    while len(sorted_packages) != len(truck.packages):
        for package in table:
            current: Package = package
            closest: Package = find_closest(address, current, unsorted_packages)
            if closest in unsorted_packages:
                sorted_packages.append(closest)
                address = closest.delivery_address
                unsorted_packages.remove(closest)
        if len(unsorted_packages) == 0 and len(truck.packages) == len(sorted_packages):
            truck.packages = sorted_packages[:]
            return sorted_packages
        else:
            print("Failure")
            print(f"Sorted: {len(sorted_packages)}")
            print(f"Unsorted: {len(unsorted_packages)}")
            print(f"Truck: {len(truck.packages)}")


# Finds out the cloests package within a list of packages and returns it.
# Iterates through package list, checks if the package already has a closest
# package and checks if theres a better distance.
# O(N) Complexity
def find_closest(address, current_package, packages) -> Package:
    closest_package: Package = current_package
    best_distance: float = None
    for package in packages:
        if package is not None:
            if closest_package is None:
                closest_package = package
                closest_address = closest_package.delivery_address
                best_distance = distance_between_addresses(closest_address, address)
            else:
                addr = package.delivery_address
                dist = distance_between_addresses(addr, address)
                if best_distance is None or dist <= best_distance:
                    closest_package = package
                    best_distance = dist
    return closest_package

# Ingest hash table and trucks list. Checks if packages still need delivered.
# Marks packages as En Route, Removes packages from truck package list
# Increments distance traveled, Returns Trucks to hub, and loads them back up.
# O(N^5) Complexity
def deliver_packages(table: HashTable, trucks: list):
    while deliveries_completed(trucks) is False:
        for truck in trucks:
            truck.set_en_route(table)
            curr_add = truck.hub_address
            sort_truck_packages(truck.packages, truck)
            truck_packages = truck.packages.copy()
            while len(truck.packages) > 0:
                for package in truck_packages:
                    package.delivery_status = deliveryStatus.DELIVERED
                    # print(f"""!!!!!!!!!!!!!!DELIVERY INFO!!!!!!!!!!!!!!!!!
                    #           Package ID:        {package.package_id}
                    #           Delivery Location: {package.delivery_address}
                    #           Truck Location:    {curr_add}
                    #           Distance Recorded: {distance_between_addresses(curr_add, package.delivery_address)}
                    #           !!!!!!!!!!!!!!DELIVERY INFO!!!!!!!!!!!!!!!!!""")
                    truck.remove_package(
                                    package,
                                    table, 
                                    distance_between_addresses(curr_add, package.delivery_address))
                    curr_add = package.delivery_address
                    truck.current_address = curr_add
            if truck.truck_id == 1:
                truck.return_truck(distance_between_addresses(curr_add, truck.hub_address))
                # This is currently giving an incorrect output
                
                # for _ in range(10):
                #     print("!!!!!!!!!!!!!!!!!!!!RETURNING TRUCK!!!!!!!!!!!!!!!!")
                # print(curr_add, )
                # for _ in range(10):
                #     print("!!!!!!!!!!!!!!!!!!!!RETURNING TRUCK!!!!!!!!!!!!!!!!")
                # truck.return_truck(distance_between_addresses('2600 Taylorsville Blvd', truck.hub_address))                        
# Iterates through hashmap to see if any packages still need to be delivered.

# Checks to see if the list of trucks have any packages left to deliver.
# O(N) Complexity
def deliveries_completed(trucks: list) -> bool:
    for truck in trucks:
        if len(truck.packages) != 0:
            return False
    return True


