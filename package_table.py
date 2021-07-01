import package

# A custom hash table is a part of the project requirements
# going to make hash table around 1.3 times larger than the # of packages = 53
# accounts for collisions by appending to a list if required. However, collisions are minimal
# and should contain all package data and this hash works pretty well in this case


def get_hash(key):
    return key * 2654435761 % 53


class HashTable:
    def __init__(self, size=53):
        self.table = []
        for i in range(size):
            self.table.append([])

    def insert(self, p_id, special, status, address, city, state, zipcode, deadline, mass):
        p = package.Package(p_id, special, status, address, city, state, zipcode, deadline, mass)
        index = get_hash(p_id)
        self.table[index].append(p)

    def search(self, p_id):
        p_list = self.table[get_hash(p_id)]
        if len(p_list) >= 1:
            for i in p_list:
                if i.p_id == p_id:
                    return i
        else:
            return None

    def remove(self, p_id):
        key = get_hash(p_id)
        p_list = self.table[key]
        if p_list:
            obj = self.search(p_id)
            p_list.remove(obj)
            return True
        else:
            print("key not in list")
            return False

