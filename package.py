

class Package:
    def __init__(self, p_id, special, status, address, city, state, zipcode, deadline, mass):
        self.p_id = p_id
        self.special = special
        self.status = status
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.mass = mass
        self.address_index = None

    def print_package(self):
        print("id:", self.p_id, "address:", self.address, "city:", self.city,
              "status:", self.status, "state:", self.state, "zip:", self.zipcode, "deadline:",
              self.deadline, "mass:", self.mass, "special:", self.special)

    def get_address(self):
        return self.address

    def update_status(self, string):
        self.status = string

    def initialize_address_index(self, distance_list):
        for i in range(len(distance_list)):
            if self.address == distance_list[i].get_address():
                self.address_index = i