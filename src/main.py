import csv
import classes.package as Package

FILEPATH: str = f"src/resources/csv/package_file.csv"

def initialize_packageFile(filename) -> list:
    packages: list = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            item = Package.Package(list(line))
            print(item)
            packages.append(item)          
    return packages


def main():
    print(initialize_packageFile(FILEPATH))


if __name__ == '__main__':
    main()
