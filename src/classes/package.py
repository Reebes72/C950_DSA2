from classes.deliveryStatus import deliveryStatus
class Package:

    def __init__(self, params: list):
        self.package_id = params[0]
        self.delivery_address = params[1]
        self.city = params[2]
        self.state = params[3]
        self.zip_code = params[4]
        self.deadline = params[5]
        self.package_weight = params[6]
        self.delivery_status = deliveryStatus.AT_THE_HUB
        self.delivery_time = None
        self.loading_time = None

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

    def setStatus(self, status):
        if status == 1:
            self.delivery_status = deliveryStatus.EN_ROUTE
        elif status == 2:
            self.delivery_status = deliveryStatus.DELIVERED
        else:
            self.delivery_status = deliveryStatus.AT_THE_HUB
