## ANDREW REEVES - ID# 011598549
import csv
from datetime import datetime, timedelta
from data_structure.hashTable import hashTable
import utils

from classes.package import Package
# Constants
# Lists are constants to avoid multiple loads with O(N^2) Complexity
PACKAGES_PATH: str = "src/resources/csv/packages.csv"
PACKAGES: list = utils.initialize_package_file(PACKAGES_PATH)
DISTANCES_PATH: str = "src/resources/csv/distances.csv"
DISTANCES: list = utils.initialize_distance_file(DISTANCES_PATH)
ADDRESSES_PATH: str = "src/resources/csv/addresses.csv"
ADDRESSES: list = utils.initialize_address_file(ADDRESSES_PATH)

TRUCKS: int = 3
DRIVERS: int = 2


def main():
    pass


if __name__ == '__main__':
    main()
