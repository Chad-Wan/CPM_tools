

def calculate_avg_peak(data_time: list, data_voltage: list):
    # 数据统计：
    peak_current = max(data_voltage)
    avg_current = 0.0
    for i in range(len(data_time) - 1):
        avg_current += (data_voltage[i + 1] + data_voltage[i]) * (data_time[i + 1] - data_time[i])
    avg_current = avg_current / 2 / (data_time[len(data_time) - 1] - data_time[0])
    # print("avg_current:", avg_current)
    # print("peak_current:", peak_current)
    return avg_current, peak_current


def change_avg_peak(data_voltage: list, avg_current: float, peak_current: float, avg_target: float, peak_target: float):
    # 数据变换：
    # 原数据列表为data_voltage，平均值avg_current，峰值peak_current
    # 目标平均值avg_target,目标峰值peak_target
    for i in range(len(data_voltage)):
        data_voltage[i] = (data_voltage[i] - avg_current) * (peak_target - avg_target) / (peak_current - avg_current) \
                          + avg_target


def data_process(data_ori: list, avg_ratio: float, peak_target: float, stretch: bool):
    # 对data_ori中的电流值进行变换，使得最终的平均值为原来的avg_ratio倍，如果stretch为真，则是电流峰值为peak_target
    # stretch表示是否对波形进行y轴方向上的拉伸，如果为True，则在y轴方向上进行拉伸，直到电流峰值达到peak_target

    data_time = []
    data_voltage = []
    tmp = []
    for line in data_ori:
        data_time.append(float(line.split("ps")[0].split()[1]))
        data_voltage.append(float(line.split()[-1]))

    # 数据统计：
    avg_current, peak_current = calculate_avg_peak(data_time, data_voltage)
    print("\nbefore process:")
    print("avg_current:", avg_current)
    print("peak_current:", peak_current)

    # 数据变换：
    # stretch表示是否对波形进行y轴方向上的拉伸
    avg_target = avg_current * avg_ratio
    if not stretch:
        change_avg_peak(data_voltage, avg_current, peak_current, avg_target, peak_current + avg_target - avg_current)
    else:
        change_avg_peak(data_voltage, avg_current, peak_current, avg_target, peak_target)

    # 数据统计：
    avg_current, peak_current = calculate_avg_peak(data_time, data_voltage)
    print("\nafter process:")
    print("avg_current:", avg_current)
    print("peak_current:", peak_current)

    # 编码输出数据
    for i in range(len(data_ori)):
        tmp.append("+ " + str(data_time[i]) + "ps " + str(data_voltage[i]) + '\n')
    return tmp

def if_items_inline(item_list: list, line: str):
    # 该函数判断在line字串里是否包含item_list中的内容
    for item in item_list:
        if (" " + item + " ") in line:
            return True
    return False
