# ANDREW REEVES - ID# 011598549
from data_structure.HashTable import HashTable
from classes.truck import Truck
from classes.package import Package

import utils
import cli


# Constants
# Lists are constants to avoid multiple loads with O(N^2) Complexity
PACKAGES_PATH: str = "src/resources/csv/packages.csv"
PACKAGES: HashTable = utils.initialize_package_file(PACKAGES_PATH)
DISTANCES_PATH: str = "src/resources/csv/distances.csv"
ADDRESSES_PATH: str = "src/resources/csv/addresses.csv"
DISTANCES: list = utils.initialize_distance_file(DISTANCES_PATH, ADDRESSES_PATH)
ADDRESSES: list = utils.initialize_address_file(ADDRESSES_PATH)

TRUCKS: int = 3
DRIVERS: int = 2


def main():
    trucks, drivers = utils.initialize_trucks_drivers(TRUCKS, DRIVERS)
    delayed_start = None
    for package in PACKAGES.hashMap:
        if package is not None and package.delayed_arrival() is not None:
            if delayed_start is None or delayed_start > package.delayed_arrival():
                delayed_start = package.delayed_arrival()
    if len(trucks) > 1:
        trucks[len(trucks) - 1].time = delayed_start
    for truck in trucks:
        utils.load_truck(PACKAGES, truck)
    utils.deliver_packages(PACKAGES, trucks)
    cli.main_menu(PACKAGES, trucks)


if __name__ == '__main__':
    main()
