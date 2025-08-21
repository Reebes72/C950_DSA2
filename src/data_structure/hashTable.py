from classes.package import Package

class HashTable:
    def __init__(self, capacity=40, low=0, high=1):
        self.capacity = capacity
        self.hashMap = [None] * capacity
        self.bucket_status_table = ["INITIALIZED"] * capacity
        self.resizing1 = low
        self.resizing2 = high

    # Hash Package ID w Modulus by size of hashMap to avoid collisions
    #
    def hashInsert(self, package: Package):
        i = 0
        buckets_probed = 0
        N = len(self.hashMap)
        bucket = hash(package.package_id) % N
        while buckets_probed < N:
            if self.bucket_status_table[bucket] == "INITIALIZED" or self.bucket_status_table[bucket] == "EMPTIED":
                self.hashMap[bucket] = package
                self.bucket_status_table[bucket] = "OCCUPIED"
                return True
            i = i + 1
            bucket = (hash(package.package_id) + (self.resizing1 * i) + (self.resizing2 * i ** 2)) % N
            buckets_probed = buckets_probed + 1
        self.resize()
        self.insert(package)
        return True

    def hashSearch(self, key):
        i = 0
        buckets_probed = 0
        N = len(self.hashMap)
        bucket = hash(key) % N
        while (self.bucket_status_table[bucket] != "INITIALIZED") and (buckets_probed < N):
            if (self.hashMap[bucket] is not None) and (self.hashMap[bucket].package_id == key):
                return self.hashMap[bucket]
            i = i + 1
            bucket = (hash(key) + self.resizing1 * i + self.resizing2 * i ** 2) % N
            buckets_probed = buckets_probed + 1
        return None

    def resize(self):
        resized_ht = HashTable(capacity=self.capacity * 2, resizing1=self.resizing1, resizing2=self.resizing2)
        for package in self.hashMap:
            resized_ht.insert(package)

        self.capacity = resized_ht.capacity
        self.hashMap = resized_ht.hashMap
        self.bucket_status_table = resized_ht.bucket_status_table
 
    def __str__(self):
        s = "   --------\n"
        index = 0
        for item in self.hashMap:
            value = str(item)
            if item is None: 
                value = 'E'
            s += '{:2}:|{:^6}|\n'.format(index, value)
            index += 1
        s += "   --------"
        return s