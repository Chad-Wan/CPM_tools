
import re


def read_file(file_path: str):
    f = open(file_path, 'r')
    lines = f.readlines()
    f.close()
    return lines


def extract_location_ports(file_path: str):
    tmp = read_file(file_path)
    location_x = []
    location_y = []
    for line in tmp:
        location_x.append(float(line.split('(')[1].split(')')[0].split()[0]))
        location_y.append(float(line.split('(')[1].split(')')[0].split()[1]))
    return location_x, location_y


def extract_location_pkg(file_path: str):
    tmp = read_file(file_path)
    location_x = []
    location_y = []
    for line in tmp:
        tmp = line.split(':')
        a = tmp[1].replace('(', '').replace(')', '').split()
        location_x.append(0.0 - float(a[0]))
        location_y.append(float(a[1]))
    return location_x, location_y


def extract_location_ploc(file_path: str):
    tmp = read_file(file_path)
    location_x = []
    location_y = []
    for line in tmp:
        tmp = line.split()
        location_x.append(float(tmp[1]))
        location_y.append(float(tmp[2]))
    return location_x, location_y


def port_dict_gen(file_path: str):
    # 这个函数用于生成sub_cpm ports的字典，字典的名字就是port的名称
    # 字典的内容就是该port的坐标值
    # 如果发现有两个port的名字一样，就会报告ERROR

    # 输入为redhawk生成的Powermodel.sp文件
    # 输出为从文件中提取出的的pin名字和pin的位置，格式为
    # [
    # [<pin_name_1>, <x_location>, <y_location>]
    # [<pin_name_2>, <x_location>, <y_location>]
    # ... ... ... ... ...
    # [<pin_name_m>, <x_location>, <y_location>]
    # ]

    tmp = {}
    pin_info_pattern = re.compile(r'^\*\s.*:\s.*:\s.*[a-zA-Z0-9]+')
    line = ""
    f = open(file_path, 'r')
    while "End Chip Package Protocol" not in line:
        line = f.readline()
        if re.match(pin_info_pattern, line):
            location = line.split('(')[1].split(')')[0].split()
            location_x = float(location[0])
            location_y = float(location[1])
            name = line.split()[1]
            if name not in tmp.keys():
                tmp[name] = [location_x, location_y]
            else:
                print("ERROR, there are two nodes have a same name.")
                print("ERROR node name is:", name, "location is:", location)
                return tmp
    f.close()
    return tmp


def pkg_dict_gen(file_path: str):
    # 这个函数用于生成package ports的字典，字典的名字就是port的名称格式为：结点名-U1_XXX
    # 输入为XtractIM生成的package netlist文件
    # 字典的内容就是该port的坐标值
    # 如果发现有两个port的名字一样，就会报告ERROR
    tmp = {}
    pin_info_pattern = re.compile(r'^\*\sU1-[0-9]+:\([-]{0,1}[0-9]*[\.]{0,1}.*\s*[-]{0,1}[0-9]*')
    line = ""
    f = open(file_path, 'r')
    while "End Chip Package Protocol" not in line:
        line = f.readline()
        if re.match(pin_info_pattern, line):
            a = line.split()[1].split(':')[0].replace('-', '_')
            b = line.split('=')[0].split(':')[-1]
            name = b + '-' + a
            location = line.split('(')[1].split(')')[0].split()
            location_x = float(location[0])
            location_y = float(location[1])
            if name not in tmp.keys():
                tmp[name] = [location_x, location_y]
            else:
                print("ERROR, there are two nodes have a same name.")
                print("ERROR node name is:", name, "location is:", location)
                return tmp
        # else:
        #     print(line, end='')
    f.close()
    return tmp


def merge_port_dicts(dict_1: dict, dict_2: dict):
    # 将输入的两个字典合并，并返回合并后的字典。
    # 如果两个字典所有元素中有任意两个键值对同键不同值，或者是同值不同键，将会打印错误信息
    error_tolerance = 2
    tmp = {}
    # 将字典1中的元素添加到tmp字典中
    for key in dict_1.keys():
        if key not in tmp.keys():
            tmp[key] = dict_1[key]

    # 将字典2中的元素添加到字典tmp中，
    # 如果该元素的key已经存在，则比较元素的value是否一样，如果不一样则报错
    for key in dict_2.keys():
        if key not in tmp.keys():
            tmp[key] = dict_2[key]
        elif (abs(tmp[key][0] - dict_2[key][0]) > error_tolerance) or (abs(tmp[key][1] - dict_2[key][1]) > error_tolerance):
            print("ERROR when merging sub_CPM ports,",
                  "there is one node but has two different locations in these two sub_CPM:")
            print("node_name:", key)
            print("node location_1 is:", tmp[key])
            print("node location_2 is:", dict_2[key])
            return tmp

    # 合并完成后，检查字典内部是否有相同的value值
    for key_1 in tmp.keys():
        for key_2 in tmp.keys():
            if key_1 != key_2 and ((abs(tmp[key_1][0] - tmp[key_2][0]) < error_tolerance) and (abs(tmp[key_1][1] - tmp[key_2][1]) < error_tolerance)):
                print("ERROR when checking merged CPM ports,",
                      "there is two nodes but has a same locations in merged CPM:")
                print("node_name_1:", key_1)
                print("node location_1 is:", tmp[key_1])
                print("node_name_2:", key_2)
                print("node location_2 is:", tmp[key_2])
                return tmp

    # 返回生成的最终字典
    return tmp


def cpm_pin_merge(pin_list_1: list, pin_list_2: list):
    # 输入文件是两个pin的名称列表
    # 返回值是一个列表，列表里面包含去重之后的所有pin的名称
    pin_list_1.extend(pin_list_2)
    tmp = []
    for pin in pin_list_1:
        if pin not in tmp:
            tmp.append(pin)
    return tmp

