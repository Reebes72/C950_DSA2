from datetime import timedelta
from classes.package import Package
from data_structure.HashTable import HashTable
from classes.deliveryStatus import deliveryStatus


class Truck:
    # These are the constant parameters set by the assignment requirements.
    MAX_PACKAGES = 16
    AVERAGE_SPEED = 18

    # Initialization. Sets ID, list of packages, defaults for requirements
    # and other attributes. 
    def __init__(self, id, speed=AVERAGE_SPEED, package_limit=MAX_PACKAGES):
        self.truck_id: int = id
        self.packages: list = []
        self.package_limit: int = package_limit
        self.speed: int = speed
        self.distance_traveled = 0
        self.driver = None
        self.hub_address = "4001 South 700 East"
        self.current_address = self.hub_address
        self.at_hub = True
        self.mileage_times = []
        self.time = timedelta(hours=8, minutes=0, seconds=0)
        
    # Returns false if truck is full. Adds package to list.
    # O(1) Complexity
    def add_package(self, package: Package):
        if len(self.packages) < self.package_limit:
            self.packages.append(package)
            package.truck_id = self.truck_id
        else:
            return False

    # Sets all the packages' delivery status to En Route
    # Stamps a loading time.
    # O(N) Complexity
    def set_en_route(self, HashTable: HashTable):
        for id in self.packages:
                id.delivery_status = deliveryStatus.EN_ROUTE
                id.loading_time = self.time

    # Removes the package of the specified package_id from the list
    # Adds the mileage for the distance traveled to the total
    # Adds the trip duration to the Truck's total
    # O(1) Complexity
    def remove_package(self, id: Package, HashTable: HashTable, distance: float):
        package: Package = HashTable.hashSearch(id.package_id)
        self.packages.remove(package)
        self.at_hub = False
        self.add_miles(distance)
        self.time += timedelta(minutes=self.add_time(distance, self.speed))
        self.mileage_times.append([self.distance_traveled, self.time])
        package.delivery_status = deliveryStatus.DELIVERED
        package.delivery_time = self.time

    # Adds miles and time back to hub
    # Sets truck at hub
    # O(1) Complexity
    def return_truck(self, distance):
        self.add_miles(distance)
        self.time += timedelta(minutes=self.add_time(distance, self.speed))
        self.mileage_times.append([self.distance_traveled, self.time])
        self.at_hub = True
    

    # Returns list of Package objects using List Comprehension
    # O(N) Complexity
    def get_packages(self, HashTable: HashTable):
        return self.packages

    # Utility function for timedelta() objects
    # O(1) Complexity
    def add_time(self, distance, speed):
        return distance/speed * 60
    
    # Increments distance traveled by miles
    # O(1) Complexity
    def add_miles(self, miles):
        self.distance_traveled += miles
    
    # True if truck full, false otherwise
    # O(1) Complexity
    def full(self):
        if len(self.packages) == self.package_limit:
            return True
        else:
            return False