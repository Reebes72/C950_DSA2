class hashTable:

    def __init__(self, capacity: int = 10):
        self.hashMap = []
        for i in range(capacity):
            self.hashMap.append([])

    def hashInsert(self, package_id, value):
        self.values[package_id % 10] = value

    def hashSearch(self, package_id):
        key = package_id % 10
        return self.values[key]

    def __len__(self):
        return len(self.values)
            
