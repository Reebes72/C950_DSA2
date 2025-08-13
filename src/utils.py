import csv

from data_structure.hashTable import hashTable
from classes.package import Package


# Opens csv, iterates through each line, inserts a Package Object into hashMap
# O(N) Complexity
def initialize_package_file(filename: str) -> list:
    container: hashTable = hashTable()
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            container.hashInsert(int(line[0]), Package(line))
    return container


# Opens csv, gets number of addresses, populates container(2D Array) with 0s
# Iterates through entries in CSV, and sets distances
# O(N^2) Complexity
def initialize_distance_file(filename: str) -> list:
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        addresses: int = number_of_addresses()
        container: list = [[0 for _ in range(addresses)] for _ in range(addresses)]
        source_address: int = 0
        for address in reader:
            for index in range(addresses):
                if address[index] != "":
                    container[address][index] = float(address[index])
                    container[index][address] = float(address[index])
            source_address += 1
        return container


# Opens csv, splits address and strips address and inserts street address 
# to the container, returns container.
# O(N) Complexity
def initialize_address_file(filename: str) -> list:
    container: list = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=",")
        for line in reader:
            full_address = line[0].split("\n")
            street = full_address[1].strip()
            container.append(street)
    return container


# Returns sum of rows in file
# O(N) Complexity
def number_of_addresses(filename: str) -> int:
    with open(filename, 'r') as file:
        return sum(1 for row in file)