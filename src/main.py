import csv
from data_structure.hashTable import hashTable
from classes.package import Package
FILEPATH: str = "src/resources/csv/package_file.csv"


def initialize_packageFile(filename: str, container: hashTable):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            container.hashInsert(line[0], line)


def main():
    stopsHashTable: hashTable = hashTable()
    initialize_packageFile(FILEPATH, stopsHashTable)
    


if __name__ == '__main__':
    main()
