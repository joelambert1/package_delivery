import csvreader
import package_table
import truck


def format_adjacency_list(obj_list):
    for i in range(len(obj_list)-1):
        for j in range(i + 1, len(obj_list)):
            temp_list = obj_list[j].get_distances()[i]
            obj_list[i].add_single_distance(temp_list)


def load_truck(t, packages):
    # choose what gets loaded and return what doesn't
    package_list = []
    package_index_list = []

    for i in range(len(packages)):
        package_list.append(packages[i])
        package_list[i].update_status("on truck " + str(truck.truck_num))
        package_list[i].initialize_address_index(distance_list)
        package_index_list.append(package_list[i].address_index)
        package_index_list.sort()
    t.add_packages(package_list)


def deliver_packages(truck, distance_list):
    package_list = truck.get_packages()
    address_list = []
    package_index_list = []
    current_location = 0
    for i in range(len(package_list)):
        package_index_list.append(package_list[i].address_index)
    package_index_list.sort()
    # nearest neighbor algorithm for now
    # need to update mileage travelled, need to change package status to delivered, and deliver all packs at address
    current_location = next_stop(package_index_list, distance_list, current_location, package_list)
    del_list = []
    for i in range(len(package_list)):
        if distance_list[current_location].address == package_list[i].address:
            del_list.append(i)
    for i in del_list:
        del package_list[i]
    # for i in package_list:
    #     # print(i)
        print(package_list)


def next_stop(package_index_list, distance_list, current_location, package_list):
    smallest = 100.0
    smallest_index = 0
    for i in package_index_list:
        option = distance_list[current_location].distances[i]
        if smallest > option > 0:
            smallest = option
            smallest_index = i

    return smallest_index


if __name__ == '__main__':
    p_table = package_table.HashTable()
    csvreader.read_package_file(p_table)
    p_list = []
    for i in range(1, 41):
        if p_table.search(i):
            p_list.append(p_table.search(i))
        else:
            print("no index found in hash table: ", i)

    distance_list = []
    distance_list = csvreader.format_distances(distance_list)

    format_adjacency_list(distance_list)

    truck = truck.Truck(2, "john")
    load_truck(truck, p_list)

    deliver_packages(truck, distance_list)






