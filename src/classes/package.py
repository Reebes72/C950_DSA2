from classes.deliveryStatus import deliveryStatus
from datetime import datetime, timedelta


class Package:
    # Initialization of Package Object via list of parameters
    # Sets other objects to default values
    def __init__(self, params: list):
        self.package_id: int = int(params[0])
        self.delivery_address: str = params[1]
        self.city: str = params[2]
        self.state: str = params[3]
        self.zip_code: str = params[4]
        self.deadline = params[5]
        self.package_weight: int = int(params[6])
        self.notes: str = ""
        if len(params) == 8:
            self.notes = params[7]
        self.delivery_status: deliveryStatus = deliveryStatus.AT_THE_HUB
        self.delivery_time: datetime = None
        self.loading_time: datetime = None
        self.truck_id: int = None
        self.on_truck: bool = False
    # String Representation of Package
    def __str__(self):
        nl = "\n"
    #     return f"""
    # Package ID: {self.package_id}
    # Address: {self.delivery_address}, {self.city}, {self.state}, {self.zip_code}
    # Weight: {self.package_weight}
    # Truck ID: {self.truck_id}
    # Delivery Time: {self.delivery_time}
    # Loading Time: {self.loading_time}
    # Delivery Status: {self.delivery_status}"""
        return f"""
    
    Package ID: {self.package_id}
    Address: {self.delivery_address}, {self.city}, {self.state}, {self.zip_code}
    Truck ID: {self.truck_id}
    """
    # String Representation of Package
    def __repr__(self):
        nl = "\n"
        return f"""
    
    Package ID: {self.package_id}
    Address: {self.delivery_address}, {self.city}, {self.state}, {self.zip_code}
    Truck ID: {self.truck_id}
    """
    #     return f"""    Package: {self.package_id}
    # Address: {self.delivery_address}, {self.city}, {self.zip_code}
    # Weight: {self.package_weight}
    # Truck ID: {self.truck_id}
    # Delivery Time: {self.delivery_time}
    # Loading Time: {self.loading_time}
    # Delivery Status: {self.delivery_status}"""

    # True if there is a truck assigned, false if not.
    # Sets truck as true.
    # O(1) Complexity
    def truck_assigned(self) -> bool:
        if self.truck_id is None:
            return False
        else:
            self.on_truck = True
            return True
    def assign_truck(self, truck):
        self.on_truck = True
        self.truck_id = truck.truck_id
    # Gets the required truck for the package, or returns none.
    # Complexity O(N)
    def required_truck(self):
        if "Can only be on truck" in self.notes:
            id = [int(index) for index in self.notes.split() if index.isdigit()][0]
            return id
        return None
    # Checks notes for wrong address or delayed.
    # splits string to get time, converts to timedelta and returns
    # O(1) Complextity
    def delayed_arrival(self):
        if "Delayed on flight---will not arrive to depot until" in self.notes:
            time: str = self.notes.split("until ")[1]
            try:
                stamp = datetime.strptime(time, "%H:%M")
                return timedelta(hours=stamp.hour, minutes=stamp.minute)
            except:
                pass
        if "Wrong address listed" in self.notes:
            delta = timedelta(hours=10, minutes=20)
            return delta
        return None
    # Checks for deadline, gets timestampe and returns timedelta
    # Complexity O(1)
    def get_deadline(self):
        if self.deadline != "EOD":
            try:
                stamp = datetime.strptime(self.deadline.split()[0], "%H:%M")
                return timedelta(hours=stamp.hour, minutes=stamp.minute)
            except:
                pass
            