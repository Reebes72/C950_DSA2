from datetime import timedelta
from classes.package import Package
from data_structure.hashTable import hashTable
from classes.deliveryStatus import deliveryStatus


class Truck:
    MAX_PACKAGES = 16
    AVERAGE_SPEED = 18

    def __init__(self, id, speed=AVERAGE_SPEED, package_limit=MAX_PACKAGES):
        self.truck_id: int = id
        self.packages: list = []
        self.package_limit: int = package_limit
        self.speed: int = speed
        self.distance_traveled = 0
        self.driver = None
        self.location = "4001 South 700 East"
        self.at_hub = True
        self.mileage_times = []
        self.time = timedelta(hours=8, minutes=0, seconds=0)
        
    def add_package(self, package: Package):
        if len(self.packages) < self.package_limit:
            self.packages.append(package.package_id)
            package.truck_id = self.truck_id
        else:
            return False
    
    def set_en_route(self, hashTable: hashTable):
        for id in self.packages:
            package: Package = hashTable.hashSearch(id)
            package.delivery_status = deliveryStatus.EN_ROUTE
            package.loading_time = self.time

    def remove_package(self, id: int, hashTable: hashTable, distance: float):
        package: Package = hashTable.hashSearch(id)
        self.packages.remove(id)
        self.at_hub = False
        self.add_miles(distance)
        self.time += timedelta(minutes=self.add_time(distance, self.speed))
        self.mileage_times.append([self.distance_traveled, self.time])
        package.delivery_status = deliveryStatus.DELIVERED
        package.delivery_time = self.time
        
    def return_truck(self, distance):
        self.add_miles(distance)
        self.time += timedelta(minutes=self.add_time(distance, self.speed))
        self.mileage_times.append([self.distance_traveled, self.time])
        self.at_hub = True
    
    def add_miles(self, miles):
        self.distance_traveled = self.distance_traveled + miles

    def get_packages(self, hashTable: hashTable):
        package_list = []
        for id in self.packages:
            package_list.append(hashTable.hashSearch(id))

    def add_time(distance, speed):
        return distance/speed * 60
    
    def full(self);
        return len(self.packages) == self.package_limit