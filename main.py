import csvreader
import package_table
import truck
import math

def format_adjacency_list(obj_list):
    for i in range(len(obj_list)-1):
        for j in range(i + 1, len(obj_list)):
            temp_list = obj_list[j].get_distances()[i]
            obj_list[i].add_single_distance(temp_list)

def load_truck(truck, packages, time):
    # choose what gets loaded and return what doesn't
    package_list = []
    package_index_list = []
    for i in range(len(packages)):
        # print(packages[i].special)
        package_list.append(packages[i])
        if "Delayed" not in packages[i].special:
            package_list[i].status = "At hub until " + format_time(time)
        package_list[i].initialize_address_index(distance_list)
        package_index_list.append(package_list[i].address_index)
        package_index_list.sort()
    truck.add_packages(package_list)

def format_time(time):
    if time[0] < 10:
        formatted = "0" + str(time[0]) + ":"
    else:
        formatted = str(time[0]) + ":"
    if time[1] < 10:
        formatted += "0" + str(time[1])
    else:
        formatted += str(time[1])
    return formatted

def unformat_time(time):
    u_time = [int(time[0] + time[1]), int(time[3] + time[4])]
    return u_time

def deliver_packages(truck, distance_list, time, stop_time):
    package_list = truck.get_packages()
    # print("packages#", len(package_list))
    package_index_list = []
    del_list = []
    current_location = 0
    for i in range(len(package_list)):
        if truck.truck_num == 1 or stop_time[0] > 9 or stop_time[0] == 9 and stop_time[1] > 4:
            package_list[i].status = "En route at " + format_time(time) + " on truck " + str(truck.truck_num)
        package_index_list.append(package_list[i].address_index)
    package_index_list.sort()

    # nearest neighbor algorithm for now
    # need to update mileage travelled, need to change package status to delivered, and deliver all packs at address
    for x in range(len(package_list)):
        prev_location = current_location
        current_location = next_stop(package_index_list, distance_list, current_location)
        add_mileage = distance_list[prev_location].get_distances()[current_location]
        truck.daily_mileage += add_mileage
        time[1] += add_mileage/.3
        round_time = time[1] - math.floor(time[1])
        if round_time < .5:
            time[1] = math.floor(time[1])
        else:
            time[1] = math.ceil(time[1])
        # print("mileage travelled: ", add_mileage, "time added:", time[1])

        while time[1] >= 60:
            time[0] += 1
            time[1] -= 60
        display_time = format_time(time)
        # print("time is now:" + str(time), "stop_time:", str(stop_time))
        if time[0] > stop_time[0]:
            if truck.truck_num == 1:
                print("truck == 1, running truck 2 packages?")
                return
            else:
                user_choices(p_table, distance_list)
        elif time[0] == stop_time[0] and time[1] >= stop_time[1]:
            if truck.truck_num == 1:
                print("truck == 1, running truck 2 packages?")
                return
            else:
                user_choices(p_table, distance_list)

        # remove package/s from package_list (loaded in truck), update status to delivered
        del_list.clear()
        for i in range(len(package_list)):
            del_list.append(package_list[i])
        package_list.clear()
        for i in range(len(del_list)):
            if distance_list[current_location].address == del_list[i].address:
                # print("dropping off all packages at:", del_list[i].p_id, del_list[i].address)
                del_list[i].status = " delivered at " + display_time + " By truck " + str(truck.truck_num)
            else:
                package_list.append(del_list[i])

        # print("truck mileage now:", truck.daily_mileage)
        if len(package_list) == 0:
            # return to hub
            truck.daily_mileage += distance_list[current_location].get_distances()[0]
            # print("truck mileage now:", truck.daily_mileage)
            return time


def next_stop(package_index_list, distance_list, current_location):
    smallest = 100.0
    smallest_index = 0
    temp_index_list = []
    for i in package_index_list:
        temp_index_list.append(i)
        option = distance_list[current_location].distances[i]
        if smallest > option > 0:
            smallest = option
            smallest_index = i
    package_index_list.clear()
    for i in temp_index_list:
        if i != smallest_index:
            package_index_list.append(i)
    # print("next stop is:", smallest, "miles")
    return smallest_index

def user_display(table, distance_list):
    # Get initial stop time from user
    while True:
        try:
            stop_time = ""
            stop_time += input("Enter a valid time (military/24h) in the format HH:MM ")
            if len(stop_time) == 5 and stop_time[2] == ":":
                u = stop_time
                if int(u[0]) < 3 and int(u[1]) < 10 and int(u[3]) < 6 and int(u[4]) < 10:
                    break
        except ValueError:
            print("Error, please enter numbers only and make sure to include \":\"")
    stop_time = unformat_time(stop_time)
    # print("unformatted stop time:", stop_time)

    morning_shift(table, distance_list, stop_time)

# could be an issue (location of this)
def user_choices(p_table, distance_list):
    while True:
        try:
            user_choice = input("\n1 to print all packages,\n2 to search for a key," +
                                 "\n3 to enter a new time,\n4 to print package range" +
                                "\n5 to exit: ")
            user_choice = int(user_choice)
            if 6 > user_choice > 0:
                if user_choice == 1:
                    for i in range(0, p_table.size):
                        if p_table.search(i):
                            p_table.search(i).print_package()
                elif user_choice == 2:
                    key = int(input("Enter key: "))
                    if p_table.search(key):
                        p_table.search(key).print_package()
                    else:
                        print("package not found")
                elif user_choice == 3:
                    p_table.clear()
                    csvreader.read_package_file(p_table)
                    user_display(p_table, distance_list)
                elif user_choice == 4:
                    print_package_range(p_table)
                else:
                    exit(0)
        except ValueError:
            print("Error, please enter numbers only and make sure to include \":\"")

def print_package_range(p_table):
    user_range = input("Enter a range within 1-40 & in the format #-# ")
    user_range = user_range.split("-")
    low_range = int(user_range[0])
    hi_range = int(user_range[1])
    # print(type(low_range), low_range, "through", hi_range)
    if low_range < 1:
        low_range = 1
    if hi_range > 40:
        hi_range = 40
    if low_range > 40 or hi_range < low_range:
        return
    # print("type:", type(low_range), low_range, type(hi_range), hi_range)
    for i in range(low_range, hi_range + 1):
        if p_table.search(i):
            p_table.search(i).print_package()

def fix_wrong_address(p_table):
    for i in range(0, p_table.size):
        if p_table.search(i):
            if "Wrong address" in p_table.search(i).special:
                p_table.search(i).address = "410 S State St"

def morning_shift(p_table, distance_list, stop_time):

    # assign packages to each truck
    p_truck1 = []
    p_truck2 = []
    p_truck3 = []

    for i in range(0, p_table.size):
        if p_table.search(i):
            package = p_table.search(i)
            special = package.special
            deadline = package.deadline
            if deadline[0] == '1' and "Delayed" not in special and len(p_truck1) < 16 or "delivered w" in special and len(p_truck1) < 16:
                p_truck1.append(package)
            elif deadline[0] == 'E' and len(p_truck3) < 15 and "truck 2" not in special or "Wrong add" in special and len(p_truck3) < 16:
                p_truck3.append(package)
            else:
                p_truck2.append(package)
    print("\npackages in each truck:", len(p_truck1), ",", len(p_truck2), ",", len(p_truck3))

    # Assign drivers to each truck
    truck1 = truck.Truck(1, "john")
    truck2 = truck.Truck(2, "johnny")
    truck3 = truck.Truck(3, "john")

    # load trucks at 8am
    time = [8, 0]
    time_truck1 = [8, 0]
    time_truck2 = [9, 5]

    load_truck(truck1, p_truck1, time_truck1)
    load_truck(truck2, p_truck2, time_truck2)
    deliver_packages(truck1, distance_list, time_truck1, stop_time)
    deliver_packages(truck2, distance_list, time_truck2, stop_time)

    # Find out which truck arrived latest and set time
    if time_truck1[0] > time_truck2[0]:
        time = time_truck1
    elif time_truck1[0] < time_truck2[0]:
        time = time_truck2
    elif time_truck1[1] > time_truck2[1]:
        time = time_truck1
    else:
        time = time_truck2

    # fix wrong address
    fix_wrong_address(p_table)

    # load final truck
    load_truck(truck3, p_truck3, time)
    deliver_packages(truck3, distance_list, time, stop_time)

    print("All packages delivered by:", format_time(time))
    print("total miles travelled between all trucks:", math.ceil(truck1.daily_mileage + truck2.daily_mileage + truck3.daily_mileage))
    user_choices(p_table, distance_list)

if __name__ == '__main__':
    # initialize hash table object
    p_table = package_table.HashTable()

    # insert csv info into hash table
    csvreader.read_package_file(p_table)

    # initialize adjacency list of distances
    distance_list = []
    distance_list = csvreader.format_distances(distance_list)
    format_adjacency_list(distance_list)

    user_display(p_table, distance_list)








