## ANDREW REEVES - ID# 011598549
from data_structure.hashTable import hashTable
from classes.truck import Truck
from classes.package import Package

import utils
import cli


# Constants
# Lists are constants to avoid multiple loads with O(N^2) Complexity
PACKAGES_PATH: str = "src/resources/csv/packages.csv"
PACKAGES: hashTable = utils.initialize_package_file(PACKAGES_PATH)
DISTANCES_PATH: str = "src/resources/csv/distances.csv"
ADDRESSES_PATH: str = "src/resources/csv/addresses.csv"
DISTANCES: list = utils.initialize_distance_file(DISTANCES_PATH, ADDRESSES_PATH)
ADDRESSES: list = utils.initialize_address_file(ADDRESSES_PATH)

TRUCKS: int = 3
DRIVERS: int = 2


def main():
    trucks, drivers = utils.initialize_trucks_drivers(TRUCKS, DRIVERS)
    delayed_start = None
    for p in PACKAGES.hashMap:
        for package in p:
            if package[1] is not None and package[1].delayed_arrival() is not None:
                if delayed_start is None or delayed_start > package[1].delayed_arrival():
                    delayed_start = package[1].delayed_arrival()
    if len(trucks) > 1:
        trucks[len(trucks) - 1].time = delayed_start
    for truck in trucks:
        utils.load_truck(PACKAGES.hashMap, truck)
    utils.deliver_packages(PACKAGES.hashMap, trucks)
    cli.main_menu(PACKAGES.hashMap, trucks)
if __name__ == '__main__':
    main()
