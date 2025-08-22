
def fill_truck(table: HashTable, truck: Truck):
    for package in table.hashMap:
        if package.delivery_status is not deliveryStatus.DELIVERED:
            if package.package_id == 9:
                package.delivery_address = "410 S State St"
                package.city = "Salt Lake City"
                package.state = "UT"
                package.zip_code = "84111"
                # sort_truck_packages(table, truck)

            if package.truck_assigned() is False and truck.full() is False:
                #Delivered on specific truck
                if "Can" in package.notes.split():
                    required_truck = [trk for trk in package.notes if trk.isdigit()]
                    for req in required_truck:
                        if int(req) == truck.truck_id and truck.full() is False:
                            package.truck_id = truck.truck_id
                            truck.add_package(package)
                            package.truck_assigned()
                        if truck.full() is True and package.truck_assigned() is False:
                            for pack in truck.packages:
                                if pack.notes == "":
                                    pack.package_id = None
                                    truck.packages.pop(truck.pack.index(pack))
                                    pack.on_truck = False
                                    package.truck_id = truck.truck_id
                                    truck.add_package(package)
                                    package.truck_assigned()
                                    break
                                    
                    
                    # truck.packages = sort_truck_packages(table, truck)
                #Delivered with specific packages
                #Checks for space on the truck
                elif "Must" in package.notes.split():
                    note: str = package.notes.replace(',', '')
                    delivered_together = [trk for trk in note.split() if trk.isdigit()]
                    if truck.package_limit - len(truck.packages) >= len(delivered_together) + 1:
                        if truck.truck_id == 2:
                            package.truck_id = truck.truck_id
                            truck.add_package(package)
                            package.truck_assigned()
                            for together in delivered_together:
                                linked_package = table.hashSearch(int(together))
                                linked_package.truck_id = truck.truck_id
                                truck.add_package(table.hashSearch(int(together)))
                                linked_package.truck_assigned()
                        
                    # truck.packages = sort_truck_packages(table, truck)
                #Delayed packages
                elif "Delayed" in package.notes.split():
                    delayed_until: list = [trk for trk in package.notes if trk.isdigit()]
                    if len(delayed_until) == 4:
                        time: timedelta = timedelta(hours=int(delayed_until[0] + delayed_until[1]), minutes=int(delayed_until[2] + delayed_until[3]))
                    else:
                        time: timedelta = timedelta(hours=int(delayed_until[0]), minutes=int(delayed_until[1] + delayed_until[2]))
                    if truck.truck_id == 3:
                        package.truck_id = truck.truck_id
                        truck.add_package(package)
                        package.truck_assigned()
                else:
                    package.truck_id = truck.truck_id
                    truck.add_package(package)
                    package.truck_assigned()


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
    
#TODO Idea to grab the three closest packages the hub and add 1 of them to each truck
#TODO 
def triple_sort(trucks: list, table: HashTable):
    packages_left: list = []
    for package in table.hashMap:
        if package.truck_id == None:
            packages_left. append(package)
    truck_1: Truck = trucks[0]
    truck_2: list = []
    truck_3: list = []
    for package in packages_left:
        find_closest()