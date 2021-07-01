

class Distance:
    def __init__(self, location=None, address=None, distances=None, zipcode=None):
        self.location = location
        self.address = address
        self.distances = distances
        self.zipcode = zipcode

    def add_location(self, location):
        location = location.lstrip().rstrip()
        self.location = location.lstrip()

    def add_address(self, address):
        zipcode = int(address.split('(')[1].replace(')', ''))
        self.address = address.split('(')[0]

    def get_address(self):
        return self.address

    def add_distances(self, distances):
        self.distances = distances

    def add_single_distance(self, distance):
        self.distances.append(distance)

    def get_distances(self):
        return self.distances

    def print_all(self):
        print("location:", self.location, ",", self.address, ",", self.distances)

    def print_distances(self):
        print(self.distances)




