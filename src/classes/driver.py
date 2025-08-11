class Driver:
    # Initialization method: Sets driver ID.
    def __init__(self, driver_id):
        self.driver_id = driver_id
        self.truck = None

    #Gets a truck for the driver, checks if any trucks are available
    # and assigns driver to truck.
    def getTruck(self, trucks):
        for truck in trucks:
            if truck.driver is None:
                truck.driver = self
                self.truck = truck
                return True
        return False
    
    #Remove Driver from truck and vice versa.
    def dropTruck(self):
        self.truck.driver = None
        self.truck = None
