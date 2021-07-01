import csv
import distance


distance_file = 'input_data/Distance csv.csv'
package_file = 'input_data/Package File.csv'


def read_package_file(packages):
    p_status = "At Hub"
    p_ids = []
    p_special = []
    p_addresses = []
    p_cities = []
    p_state = []
    p_zip = []
    p_deadline = []
    p_mass = []
    with open(package_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            p_ids.append(row[0])
            if len(row[7]) == 0:
                p_special.append("none")
            else:
                p_special.append(row[7])
            p_addresses.append(row[1])
            p_cities.append(row[2])
            p_state.append(row[3])
            p_zip.append(row[4])
            p_deadline.append(row[5])
            p_mass.append(row[6])
        for i in range(len(p_ids)):
            packages.insert(int(p_ids[i]), p_special[i], p_status, p_addresses[i], p_cities[i], p_state[i],
                            p_zip[i], p_deadline[i], p_mass[i])


def format_distances(distance_list):
    distance_csv_list = read_distance_file(distance_file)
    address = get_addresses(distance_csv_list)
    name_list = get_names(distance_csv_list)
    distance_list = get_distances(distance_csv_list, address, name_list, distance_list)
    return distance_list


def read_distance_file(file):
    distance_csv_list = []
    with open(file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            distance_csv_list.append(str(row))
    return distance_csv_list


def get_distances(distance_csv_list, address, name_list, distance_list):
    distance_entry = []
    temp_distance_list = []
    for entry in distance_csv_list:
        # Next: remove everything except the distances
        entry = entry.split("\', ", 1)[1].split(", \'\'", )[0].split("\', \'", 1)[1]
        distance_entry.append(entry.replace('\'', '').replace(']', ''))
        # now we have comma separated distances but they are still in string format
    temp_list = []
    for i in distance_entry:
        temp_distance_list.append(i.split(','))
        temp_list.append([])
    for i in range(len(temp_distance_list)):
        for j in temp_distance_list[i]:
            temp_list[i].append(float(j))
        distance_obj = distance.Distance()
        distance_obj.add_address(address[i])
        distance_obj.add_distances(temp_list[i])
        distance_obj.add_location(name_list[i])
        distance_list.append(distance_obj)
    return distance_list


def get_addresses(distance_csv_list):
    address = []
    for entry in distance_csv_list:
        address.append(entry.split('\', \' ')[1].split('\', \'')[0].replace('\\n', ''))
    return address


def get_names(distance_csv_list):
    name_list = []
    for entry in distance_csv_list:
        name_list.append(entry.split('[\'')[1].split('\\n')[0])
    return name_list





