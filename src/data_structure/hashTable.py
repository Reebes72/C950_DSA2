class hashTable:

    def __init__(self, capacity: int = 10):
        self.hashMap = []
        for i in range(capacity):
            self.hashMap.append([])

    def hashInsert(self, package_id, value):
        hash = self.hashKey(int(package_id))
        keyValue = [package_id, value]
        if self.hashMap[hash] is None:
            self.hashMap[hash] = list([keyValue])
            return True
        else:
            for item in self.hashMap[hash]:
                if item[0] == package_id:
                    item[1] = keyValue
                    return True
            self.hashMap[hash].append(keyValue)

    def hashKey(self, package_id: int) -> int:
        return int(package_id) % len(self.hashMap)
    
    def hashSearch(self, package_id):
        hash = self.hashKey(package_id)
        if self.hashMap[hash] is not None:
            for item in self.hashMap[hash]:
                if item[0] == package_id:
                    return item[1]
        return None

    def __len__(self):
        return len(self.values)
            