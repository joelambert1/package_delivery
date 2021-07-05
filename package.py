

class Package:
    def __init__(self, p_id, special, status, address, city, state, zipcode, deadline, mass, hub_status="", route_status="", deliv_status=""):
        self.p_id = p_id
        self.special = special
        self.status = status
        self.hub_status = hub_status
        self.route_status = route_status
        self.deliv_status = deliv_status
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.mass = mass
        self.address_index = None

    def print_package(self):
        blue = '\033[94m'
        bold = '\033[1m'
        underline = '\033[4m'
        endc = '\033[0m'
        print("\npackage:", bold + blue + str(self.p_id) + endc, "\"", self.address, self.city, self.state, self.zipcode, "\"",
              blue + "\n\t\tstatus:" + endc, self.status, "\n\t\tdeadline:",
              underline + self.deadline + endc, "mass:", self.mass, "special:", self.special)

    def get_address(self):
        return self.address

    def update_status(self, string):
        self.status = string

    def initialize_address_index(self, distance_list):
        for i in range(len(distance_list)):
            if self.address == distance_list[i].get_address():
                self.address_index = i