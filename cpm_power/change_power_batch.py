def calculate_avg_peak(data_time: list, data_voltage: list):
    # 数据统计：
    avg_current = 0.0
    for i in range(len(data_time) - 1):
        avg_current += (data_voltage[i + 1] + data_voltage[i]) * (data_time[i + 1] - data_time[i])
    avg_current = avg_current / 2 / (data_time[len(data_time) - 1] - data_time[0])

    peak_current_over_avg = max(data_voltage) - avg_current
    # print("avg_current:", avg_current)
    # print("peak_current:", peak_current)
    return avg_current, peak_current_over_avg


def change_avg_peak(data_voltage: list, avg_current: float, avg_ratio: float):
    # 数据变换：
    # 原数据列表为data_voltage，平均值：avg_current，峰值减均值：peak_current_over_avg
    # 目标平均值avg_target,目标峰值减均值peak_target_over_avg
    avg_offset = avg_current * avg_ratio - avg_current

    for i in range(len(data_voltage)):
        data_voltage[i] = data_voltage[i] + avg_offset


def data_process(data_ori: list, avg_ratio: float):
    # 对data_ori中的电流值进行变换，使得最终的平均值为avg_target，如果stretch为真，则是电流峰减去均值电流的值为peak_target_over_avg
    # stretch表示是否对波形进行y轴方向上的拉伸，如果为True，则以avg_target为中心，在y轴方向上进行拉伸，直到电流峰值达到减去avg_target的值达到peak_target_over_avg

    data_time = []
    data_voltage = []
    tmp = []
    for line in data_ori:
        data_time.append(float(line.split("ps")[0].split()[1]))
        data_voltage.append(float(line.split()[-1]))

    # 数据统计：
    avg_current, peak_current_over_avg = calculate_avg_peak(data_time, data_voltage)
    print("\nbefore process:")
    print("avg_current:", avg_current)
    print("peak_current_over_avg:", peak_current_over_avg)

    # 数据变换：
    # stretch表示是否对波形进行y轴方向上的拉伸
    change_avg_peak(data_voltage, avg_current, avg_ratio)

    # 数据统计：
    avg_current, peak_current_over_avg = calculate_avg_peak(data_time, data_voltage)
    print("\nafter process:")
    print("avg_current:", avg_current)
    print("peak_current_over_avg:", peak_current_over_avg)

    # 编码输出数据
    for i in range(len(data_ori)):
        tmp.append("+ " + str(data_time[i]) + "ps " + str(data_voltage[i]) + '\n')
    return tmp


def if_items_inline(item_list: list, line: str):
    for item in item_list:
        if (" " + item + " ") in line:
            return True
    return False


file_path = "C:/Users/nxf07386/Documents/temp/iMX8QM_B0_PowerModel_partition_6x6_foster.sp"
file_output = "C:/Users/nxf07386/Documents/temp/iMX8QM_B0_PowerModel_partition_6x6_foster.sp.out"

# change_list = ["p175", "p178", "p199", "p201", "p278", "p289", "p155", "p162", "p183", "p189", "p206", "p219"]  # GPU
# change_list = ["p6", "p12", "p22", "p35", "p51", "p70", "p90", "p97", "p100", "p104", "p109", "p113", "p124",
#                "p133", "p135", "p138", "p141", "p144", "p154", "p161", "p165", "p169", "p172", "p176", "p188",
#                "p191", "p194", "p197", "p205", "p218", "p229", "p251", "p275", "p287"]  # MAIN
change_list = ["p45", "p56", "p108", "p112"]  # A53
# change_list = ["p15", "p23", "p36", "p98", "p101", "p105"]  # A72

f = open(file_path, 'r')
lines = f.readlines()
f.close()

f = open(file_output, 'w')

start_flag = False
tmp_mem = []

for line in lines:
    if "Icursig" in line and "pwl" in line and if_items_inline(change_list, line):
        if start_flag:
            print("error: Icursig endding not found")
            f.close()
            break
        tmp_mem.append(line)
        f.writelines(tmp_mem)
        tmp_mem = []
        start_flag = True
        continue

    if start_flag and ")" in line:
        # 此处安放数据处理模块，对存储在tmp_mem中的pwl的数据进行变换
        # 此处也可将数据块移出进行数据分析
        tmp_mem = data_process(data_ori=tmp_mem, avg_ratio=0.691)

        tmp_mem.append(line)
        f.writelines(tmp_mem)
        tmp_mem = []
        start_flag = False
        continue

    tmp_mem.append(line)

f.writelines(tmp_mem)
f.close()




