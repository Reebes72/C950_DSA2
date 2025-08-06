class Package:
    def __init__(self, address, deadline, city, zip, weight, status, delivery, load, id):
        self.delivery_address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip
        self.package_weight = weight
        self.package_id = id
        self.delivery_time = delivery
        self.loading_time = load

    def __str__(self):
        nl = "\n"
        return f"""Package: {self.id}{nl}
    Address: {self.address}, {self.city},
    {self.zip_code}{nl}Weight:
    {self.package_weight}{nl}
    Delivery Time: {self.delivery_time}{nl}
    Loading Time: {self.loading_time}"""

    def __repr__(self):
        nl = "\n"
        return f"""Package: {self.id}{nl}
    Address: {self.address}, {self.city},
    {self.zip_code}{nl}Weight:
    {self.package_weight}{nl}
    Delivery Time: {self.delivery_time}{nl}
    Loading Time: {self.loading_time}"""
