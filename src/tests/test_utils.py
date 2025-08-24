def fill_trucks_with_deadline(truck: Truck, table: list):
    packages_left: list = get_after_prime_packages(table)
    for package in packages_left:
        if package.deadline == "EOD":
            packages_left.remove(package)
    packages_split: int = len(packages_left)/2-1
    
    # truck_1_packages = packages_left[:int(packages_split)]
    # packages_split += 1
    # truck_2_packages = packages_left[int(packages_split):]
    # # Test function
    # test_array = []
    # for t in truck_1_packages:
    #     test_array.append(t.package_id)
    # print(test_array)
    # test_array.clear()
    # for t in truck_2_packages:
    #     test_array.append(t.package_id)
    # print(test_array)        