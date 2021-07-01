

class Truck:
    def __init__(self, truck_num, driver):
        self.truck_num = truck_num
        self.driver = driver
        self.packages = []

    def add_num(self, num):
        self.truck_num = num

    def add_driver(self, driver):
        self.driver = driver

    def add_packages(self, p):
        for i in p:
            self.packages.append(i)

    def get_packages(self):
        return self.packages

    def print_packages(self):
        for i in self.packages:
            i.print_package()

