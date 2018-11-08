import os, sys
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *
from tkinter.messagebox import *
import matplotlib.pyplot as plt


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
    voltage_dict = voltage_gen(file_path)

    tmp = {}
    pin_info_pattern = re.compile(r'^\*\s.*:\s.*:\s.*[a-zA-Z0-9]+')
    line = ""
    f = open(file_path, 'r')
    while "End Chip Package Protocol" not in line:
        line = f.readline()
        if re.match(pin_info_pattern, line):
            p_name = line.split(':')[-1].split()[0]
            location = line.split('(')[1].split(')')[0].split()
            location_x = float(location[0])
            location_y = float(location[1])
            name = line.split()[1]
            if name not in tmp.keys():
                tmp[name] = [location_x, location_y, p_name]
            else:
                print("ERROR, there are two nodes have a same name.")
                print("ERROR node name is:", name, "location is:", location)
                return tmp
    f.close()

    for key_map in tmp.keys():
        if tmp[key_map][2] in voltage_dict.keys():
            # print(tmp[key_map])
            tmp[key_map].append(voltage_dict[tmp[key_map][2]])
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


def voltage_gen(file_path: str):
    tmp = {}
    beginning = "* CPM Port Name | Average current (A) | Max. magnitude of current | Net voltage *"
    endding = "* Average power ="
    processing = False
    f = open(file_path, 'r')
    while True:
        line = f.readline()
        if beginning in line:
            processing = True
            continue
        if endding in line:
            break
        if not processing:
            continue
        else:
            if line.split()[1] not in tmp.keys():
                tmp[line.split()[1]] = line.split()[-1]
    f.close()
    return tmp


def get_pin_names(file_path: str):
    # 这个函数用于从spice网表中获取子电路的pin名称
    tmp = []
    beginning = ".SUBCKT "
    endding = "*"
    processing = False
    f = open(file_path, 'r')
    while True:
        line = f.readline()
        if beginning in line:
            processing = True
            continue
        if endding in line and processing:
            break
        if not processing:
            continue
        else:
            tmp1 = line.split()
            for item in tmp1:
                if item != '+':
                    tmp.append(item)
    f.close()
    return tmp


class Application_ui(Frame):
    # 这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('CPM mapping tool   by Chad Wan')
        self.master.geometry('1120x468')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.style.configure('Frame1.TLabelframe', font=('宋体', 9))
        self.Frame1 = LabelFrame(self.top, text='input/output', style='Frame1.TLabelframe')
        self.Frame1.place(relx=0.05, rely=0.15, relwidth=0.5, relheight=0.5)

        self.style.configure('Frame2.TLabelframe', font=('宋体', 9))
        self.Frame2 = LabelFrame(self.top, text='offset setting', style='Frame2.TLabelframe')
        self.Frame2.place(relx=0.58, rely=0.15, relwidth=0.35, relheight=0.5)

        self.style.configure('Command_map.TButton', font=('宋体', 9))
        self.Command_map = Button(self.top, text='generate map', command=self.Command_map_Cmd,
                                  style='Command_map.TButton')
        self.Command_map.place(relx=0.37, rely=0.75, relwidth=0.25, relheight=0.14)

        self.style.configure('Command_scatter.TButton', font=('宋体', 9))
        self.Command_scatter = Button(self.top, text='plot scatter', command=self.Command_scatter_Cmd,
                                      style='Command_scatter.TButton')
        self.Command_scatter.place(relx=0.06, rely=0.75, relwidth=0.25, relheight=0.14)

        self.style.configure('Command_netlists.TButton', font=('宋体', 9))
        self.Command_netlists = Button(self.top, text='generate netlists', command=self.Command_netlists_Cmd,
                                       style='Command_netlists.TButton')
        self.Command_netlists.place(relx=0.68, rely=0.75, relwidth=0.25, relheight=0.14)

        self.Text1Var = StringVar(value="C:/Users/nxf07386/Documents/temp/cpm_qxp/PowerModel_main.sp")
        self.Text1 = Entry(self.Frame1, text="C:/Users/nxf07386/Documents/temp/cpm_qxp/PowerModel_main.sp", textvariable=self.Text1Var, font=('宋体', 9))
        self.Text1.place(relx=0.3, rely=0.12, relwidth=0.65, relheight=0.15)

        self.Text2Var = StringVar(value="C:/Users/nxf07386/Documents/temp/cpm_qxp/x_vdd_gnd_only__sig2gnd_SPICE_t_17X17.ckt")
        self.Text2 = Entry(self.Frame1, text="C:/Users/nxf07386/Documents/temp/cpm_qxp/x_vdd_gnd_only__sig2gnd_SPICE_t_17X17.ckt", textvariable=self.Text2Var, font=('宋体', 9))
        self.Text2.place(relx=0.3, rely=0.35, relwidth=0.65, relheight=0.15)

        self.Text3Var = StringVar(value='C:/Users/nxf07386/Documents/temp/cpm_qxp/test')
        self.Text3 = Entry(self.Frame1, text='C:/Users/nxf07386/Documents/temp/cpm_qxp/test', textvariable=self.Text3Var, font=('宋体', 9))
        self.Text3.place(relx=0.3, rely=0.7, relwidth=0.65, relheight=0.15)

        self.Text4Var = StringVar(value='4575')
        self.Text4 = Entry(self.Frame2, text='4575', textvariable=self.Text4Var, font=('宋体', 9))
        self.Text4.place(relx=0.554, rely=0.05, relwidth=0.17, relheight=0.15)

        self.Text5Var = StringVar(value='4350')
        self.Text5 = Entry(self.Frame2, text='4350', textvariable=self.Text5Var, font=('宋体', 9))
        self.Text5.place(relx=0.554, rely=0.3, relwidth=0.17, relheight=0.15)

        self.Text6Var = StringVar(value='1.111')
        self.Text6 = Entry(self.Frame2, text='0.9', textvariable=self.Text6Var, font=('宋体', 9))
        self.Text6.place(relx=0.554, rely=0.55, relwidth=0.17, relheight=0.15)

        self.Text7Var = StringVar(value='2')
        self.Text7 = Entry(self.Frame2, text='2', textvariable=self.Text7Var, font=('宋体', 9))
        self.Text7.place(relx=0.554, rely=0.8, relwidth=0.17, relheight=0.15)

        self.style.configure('Label1.TLabel', anchor='w', font=('宋体', 9))
        self.Label1 = Label(self.Frame1, text='die_file_path', style='Label1.TLabel')
        self.Label1.place(relx=0.06, rely=0.12, relwidth=0.229, relheight=0.15)

        self.style.configure('Label2.TLabel', anchor='w', font=('宋体', 9))
        self.Label2 = Label(self.Frame1, text='pkg_file_path', style='Label2.TLabel')
        self.Label2.place(relx=0.06, rely=0.35, relwidth=0.198, relheight=0.15)

        self.style.configure('Label3.TLabel', anchor='w', font=('宋体', 9))
        self.Label3 = Label(self.Frame1, text='output_dir', style='Label3.TLabel')
        self.Label3.place(relx=0.06, rely=0.7, relwidth=0.198, relheight=0.15)

        self.style.configure('Label4.TLabel', anchor='w', font=('宋体', 9))
        self.Label4 = Label(self.Frame2, text='offset_on_X', style='Label4.TLabel')
        self.Label4.place(relx=0.18, rely=0.05, relwidth=0.187, relheight=0.15)

        self.style.configure('Label5.TLabel', anchor='w', font=('宋体', 9))
        self.Label5 = Label(self.Frame2, text='offset_on_Y', style='Label5.TLabel')
        self.Label5.place(relx=0.18, rely=0.3, relwidth=0.242, relheight=0.15)

        self.style.configure('Label6.TLabel', anchor='w', font=('宋体', 9))
        self.Label6 = Label(self.Frame2, text='shrink', style='Label6.TLabel')
        self.Label6.place(relx=0.18, rely=0.55, relwidth=0.261, relheight=0.15)

        self.style.configure('Label7.TLabel', anchor='w', font=('宋体', 9))
        self.Label7 = Label(self.Frame2, text='error tolerance', style='Label7.TLabel')
        self.Label7.place(relx=0.18, rely=0.8, relwidth=0.298, relheight=0.15)


class Application(Application_ui):
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
        self.dict_die_ports = []
        self.dict_pkg_ports = []

        # 偏移量设置,缩放设置,mapping误差设置
        self.offset = [4572, 4359.85]
        self.alpha = 1 / 0.9
        self.error_tolerance = 2

        # 存储map结果
        self.mapping_result = []

        # 这个列表用于存储未被matched的bump信息
        self.bump_not_matched = []

        # 这个网表是否被划分过片区
        self.use_division = False

        self.path_die_file = ''
        self.path_pkg_file = ''
        self.path_output_file = ''

    def extract_ports(self):
        # 此函数的作用是将gui上的信息读入实例实例变量中

        self.path_die_file = self.Text1Var.get().replace('\\', '/')
        self.path_pkg_file = self.Text2Var.get().replace('\\', '/')
        self.path_output_file = self.Text3Var.get().replace('\\', '/')

        # 偏移量设置,缩放设置,mapping误差设置
        self.offset[0] = float(self.Text4Var.get())
        self.offset[1] = float(self.Text5Var.get())
        self.alpha = float(self.Text6Var.get())
        self.error_tolerance = float(self.Text7Var.get())
        # print("get error_tolerance:", self.error_tolerance)

        # 生成package和die的port字典
        self.dict_die_ports = port_dict_gen(self.path_die_file)
        self.dict_pkg_ports = pkg_dict_gen(self.path_pkg_file)

    def Command_map_Cmd(self, event=None, msg_en=True):
        # 此函数的功能是将pkg和die上匹配的bump进行零电阻链接
        # output文件夹下生成：
        # 电阻网络网表r_mapping.ckt
        # 未被匹配的bump名称列表bump_not_matched.txt

        self.extract_ports()
        # 电阻实例编号
        resistance_num = 0

        temp_list = []
        voltage_list = []
        # mapping pkg ports and die bumps
        for key_die in self.dict_die_ports.keys():
            die_bump_matched = False
            for key_pkg in self.dict_pkg_ports.keys():
                if abs((0.0 - self.dict_pkg_ports[key_pkg][0]) * self.alpha + self.offset[0] -
                       self.dict_die_ports[key_die][0]) < self.error_tolerance and \
                        abs(self.dict_pkg_ports[key_pkg][1] * self.alpha + self.offset[1] -
                            self.dict_die_ports[key_die][1]) < self.error_tolerance:
                    die_bump_matched = True
                    # 打印mapping电阻列表
                    temp = self.dict_die_ports[key_die][2] + ' ' + key_pkg.split('-')[0] + ' ' + '0'
                    # print(self.error_tolerance)
                    if temp not in temp_list:
                        temp_list.append(temp)
                        self.mapping_result.append("R_pkg2die_{num}".format(num=resistance_num) + ' ' + temp + ' ' + '\n')

                        tmp_vol = key_pkg.split('-')[0] + ' ' + self.dict_die_ports[key_die][3] + '\n'
                        if tmp_vol not in voltage_list:
                            voltage_list.append(tmp_vol)

                        print("R_pkg2die_{num}".format(num=resistance_num) + ' ' + temp)
                    resistance_num += 1
                    break

            if not die_bump_matched:
                self.bump_not_matched.append(key_die + '\n')

        # 生成map电阻网络
        f = open(self.path_output_file + '/r_mapping.ckt', 'w')
        f.writelines(self.mapping_result)
        f.close()

        # 报告没有被匹配的bump结点
        f = open(self.path_output_file + '/bump_not_matched.txt', 'w')
        f.writelines(self.bump_not_matched)
        f.close()

        # voltage_list是pkg bump与电压的对应关系，此处是将该关系转化成BGA与电压的关系
        temp_list = get_pin_names(self.path_pkg_file)
        for i in range(len(voltage_list)):
            temp = 'BGA_' + '_'.join(voltage_list[i].split('_', 1)[1].split('_')[:-1])
            # print(temp_list)
            for item in temp_list:
                if temp in item:
                    voltage_list[i] = item + ' ' + voltage_list[i].split()[1]

        # 生成电压参数表
        f = open(self.path_output_file + '/voltage_param.ckt', 'w')
        for line in voltage_list:
            f.writelines(".param voltage__" + line.split()[0] + ' = ' + line.split()[1] + '\n')
        f.close()

        # 生成电压源
        f = open(self.path_output_file + '/voltage_source.ckt', 'w')
        for line in voltage_list:
            f.writelines("v_" + line.split()[0] + ' ' + line.split()[0] + ' 0 ' + 'voltage__' + line.split()[0] + '\n')
        f.close()

        self.bump_not_matched = []
        self.mapping_result = []

        if msg_en:
            showinfo(title='Msg', message='mapping done')

    def Command_scatter_Cmd(self, event=None):
        self.extract_ports()

        x_pkg_bump = []
        y_pkg_bump = []
        x_die_bump = []
        y_die_bump = []

        # 提取pkg中die一侧的坐标，x坐标序列存储到x_pkg_bump, y坐标序列存储到y_pkg_bump
        for key in self.dict_pkg_ports.keys():
            x_pkg_bump.append(self.dict_pkg_ports[key][0])
            y_pkg_bump.append(self.dict_pkg_ports[key][1])

        # 提取die中pkg一侧的坐标，x坐标序列存储到x_die_bump, y坐标序列存储到y_die_bump
        for key in self.dict_die_ports.keys():
            x_die_bump.append(self.dict_die_ports[key][0])
            y_die_bump.append(self.dict_die_ports[key][1])

        # package坐标变换
        for i in range(len(x_pkg_bump)):
            x_pkg_bump[i] = (0.0 - x_pkg_bump[i]) * self.alpha + self.offset[0]
        for i in range(len(y_pkg_bump)):
            y_pkg_bump[i] = y_pkg_bump[i] * self.alpha + self.offset[1]

        # 画die位置图，用叉号
        plt.scatter(x_die_bump, y_die_bump, s=50, marker='x', c='g')

        # 画pkg位置图，用空心圈
        plt.scatter(x_pkg_bump, y_pkg_bump, s=90, marker='o', c='', edgecolors='y')
        plt.show()

    def Command_netlists_Cmd(self, event=None):
        self.extract_ports()
        f = open(self.path_output_file + "/test_top.sp", 'w')
        f.writelines("**********")
        f.writelines("\n\n\n")
        f.writelines(".include \"<pkg_path>\"")
        f.writelines("\n")
        f.writelines(".include \"<die_path>\"")
        f.writelines("\n\n")
        f.writelines(".inc \"<voltage_param_file>\"")
        f.writelines("\n\n")
        f.writelines(".tran 1n 100n")
        f.writelines("\n\n")
        f.writelines("* i/v probe")
        f.writelines("\n\n")
        f.writelines("* package_inst")
        f.writelines("\n\n")
        f.writelines("* die_inst")
        f.writelines("\n\n")
        f.writelines("* voltage source")
        f.writelines("\n\n")
        f.writelines(".END")
        f.close()
        print("done")


if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
    try:
        top.destroy()
    except:
        pass
