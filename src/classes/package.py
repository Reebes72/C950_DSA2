from classes.deliveryStatus import deliveryStatus
from datetime import datetime, timedelta


class Package:

    def __init__(self, params: list):
        self.package_id: int = params[0]
        self.delivery_address: str = params[1]
        self.city: str = params[2]
        self.state: str = params[3]
        self.zip_code: str = params[4]
        self.deadline = params[5]
        self.package_weight: int = params[6]
        self.notes: str = params[7]
        self.delivery_status: deliveryStatus = deliveryStatus.AT_THE_HUB
        self.delivery_time = None
        self.loading_time = None
        self.truck_id: int = None
        self.on_truck: bool = False

    def __str__(self):
        nl = "\n"
        return f"""
    Package: {self.package_id}{nl}
    Address: {self.delivery_address}, {self.city}, {self.state}, {self.zip_code}{nl}
    Weight: {self.package_weight}{nl}
    Delivery Time: {self.delivery_time}{nl}
    Loading Time: {self.loading_time}{nl}"""

    def __repr__(self):
        nl = "\n"
        return f"""
    Package: {self.package_id}{nl}
    Address: {self.delivery_address}, {self.city}, {self.zip_code}{nl}
    Weight: {self.package_weight}{nl}
    Delivery Time: {self.delivery_time}{nl}
    Loading Time: {self.loading_time}{nl}"""

    def set_status(self, status):
        if status == 1:
            self.delivery_status = deliveryStatus.EN_ROUTE
        elif status == 2:
            self.delivery_status = deliveryStatus.DELIVERED
        else:
            self.delivery_status = deliveryStatus.AT_THE_HUB

    def truck_assigned(self) -> bool:
        return True if self.truck_assigned is not None else False

    def required_truck(self):
        if "Can only be on truck" in self.notes:
            id = [int(index) for index in self.notes.split() if index.isdigit()][0]
            return id
        return None

    def delayed_arrival(self):
        if "Delayed on flight---will not arrive to depot until" in self.notes:
            time:str = self.notes.split("until ")[1]
            try:
                stamp = datetime.strptime(time, "%H:%M")
                delta = timedelta(hours=stamp.hour, minutes=stamp.minute)
                return delta
            except:
                pass
        if "Wrong address listed" in self.notes:
            delta = timedelta(hours=10, minutes=20)
            return delta
        return None

    def get_deadline(self):
        if self.deadline != "EOD":
            try:
                stamp = datetime.strptime(self.deadline.split()[0], "%H:%M")
                return timedelta(hours=stamp.hour, minutes=stamp.minute)
            except:
                pass
            