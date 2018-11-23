#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys
from tkinter import *
# Python 3.x
PythonVersion = 3
from tkinter.font import Font
from tkinter.ttk import *
from tkinter.messagebox import *
#import tkinter.filedialog as tkFileDialog
#import tkinter.simpledialog as tkSimpleDialog    #askstring()

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('CPM文件功率调整 by Chad')
        self.master.geometry('940x515')

        self.sp_file_path = ""
        self.port_to_process = ""
        self.avg_target = 0.0
        self.peak_target_over_avg = 0.0

        # 以下为窗口定义
        self.top = self.winfo_toplevel()

        # 该变量决定工作模式，False代表频率变换，True代表峰值均值变化
        self.work_mode = False

        self.style = Style()

        self.style.configure('Label1.TLabel',anchor='w', font=('Calibri',9))
        self.Label1 = Label(self.top, text='.sp文件路径', style='Label1.TLabel')
        self.Label1.place(relx=0.051, rely=0.124, relwidth=0.137, relheight=0.049)

        self.Text1Var = StringVar(value="C:/Users/nxf07386/Documents/temp/PowerModel_main.sp")
        # self.Text1Var = StringVar(value="Test1")
        self.Text1 = Entry(self.top, text='Text1', textvariable=self.Text1Var, font=('宋体',9))
        self.Text1.place(relx=0.221, rely=0.124, relwidth=0.614, relheight=0.064)

        self.style.configure('Frame1.TLabelframe',font=('宋体',9))
        self.Frame1 = LabelFrame(self.top, text='Frame1', style='Frame1.TLabelframe')
        self.Frame1.place(relx=0.043, rely=0.342, relwidth=0.427, relheight=0.483)

        self.style.configure('Frame2.TLabelframe',font=('宋体',9))
        self.Frame2 = LabelFrame(self.top, text='Frame2', style='Frame2.TLabelframe')
        self.Frame2.place(relx=0.511, rely=0.357, relwidth=0.435, relheight=0.468)


        self.style.configure('Command1.TButton',font=('宋体',9))
        self.Command1 = Button(self.top, text='功率分析', command=self.power_analysis, style='Command1.TButton')
        self.Command1.place(relx=0.638, rely=0.217, relwidth=0.188, relheight=0.08)

        self.style.configure('Label2.TLabel',anchor='w', font=('Calibri',9))
        self.Label2 = Label(self.top, text='需要调整的功率端口', style='Label2.TLabel')
        self.Label2.place(relx=0.06, rely=0.217, relwidth=0.137, relheight=0.049)

        self.Text2Var = StringVar(value='Text2')
        self.Text2 = Entry(self.top, text='Text2', textvariable=self.Text2Var, font=('宋体',9))
        self.Text2.place(relx=0.221, rely=0.202, relwidth=0.359, relheight=0.064)

        self.style.configure('Command2.TButton',font=('宋体',9))
        self.Command2 = Button(self.top, text='开始变换+重新分析', command=self.power_change, style='Command2.TButton')
        self.Command2.place(relx=0.655, rely=0.885, relwidth=0.256, relheight=0.08)

        self.style.configure('Label3.TLabel',anchor='w', font=('宋体',9))
        self.Label3 = Label(self.Frame1, text='当前频率为：', style='Label3.TLabel')
        self.Label3.place(relx=0.12, rely=0.257, relwidth=0.282, relheight=0.133)

        self.style.configure('Label4.TLabel',anchor='w', font=('宋体',9))
        self.Label4 = Label(self.Frame1, text='Label4', style='Label4.TLabel')
        self.Label4.place(relx=0.459, rely=0.257, relwidth=0.342, relheight=0.133)

        self.style.configure('Label5.TLabel',anchor='w', font=('宋体',9))
        self.Label5 = Label(self.Frame2, text='当前峰值为：', style='Label5.TLabel')
        self.Label5.place(relx=0.117, rely=0.266, relwidth=0.257, relheight=0.104)

        self.style.configure('Label6.TLabel',anchor='w', font=('宋体',9))
        self.Label6 = Label(self.Frame2, text='Label6', style='Label6.TLabel')
        self.Label6.place(relx=0.528, rely=0.232, relwidth=0.276, relheight=0.104)

        self.style.configure('Label7.TLabel',anchor='w', font=('宋体',9))
        self.Label7 = Label(self.Frame2, text='当前平均值为：', style='Label7.TLabel')
        self.Label7.place(relx=0.117, rely=0.432, relwidth=0.335, relheight=0.104)

        self.style.configure('Label8.TLabel',anchor='w', font=('宋体',9))
        self.Label8 = Label(self.Frame2, text='Label8', style='Label8.TLabel')
        self.Label8.place(relx=0.528, rely=0.398, relwidth=0.237, relheight=0.104)

        self.style.configure('Label9.TLabel',anchor='w', font=('宋体',9))
        self.Label9 = Label(self.Frame1, text='目标频率：', style='Label9.TLabel')
        self.Label9.place(relx=0.14, rely=0.578, relwidth=0.202, relheight=0.1)

        self.style.configure('Label10.TLabel',anchor='w', font=('宋体',9))
        self.Label10 = Label(self.Frame2, text='目标峰值：', style='Label10.TLabel')
        self.Label10.place(relx=0.117, rely=0.631, relwidth=0.237, relheight=0.104)

        self.style.configure('Label11.TLabel',anchor='w', font=('宋体',9))
        self.Label11 = Label(self.Frame2, text='目标平均值：', style='Label11.TLabel')
        self.Label11.place(relx=0.117, rely=0.797, relwidth=0.276, relheight=0.104)

        self.Text3Var = StringVar(value='Text3')
        self.Text3 = Entry(self.Frame1, text='Text3', textvariable=self.Text3Var, font=('宋体',9))
        self.Text3.place(relx=0.399, rely=0.578, relwidth=0.282, relheight=0.1)

        self.Text4Var = StringVar(value='Text4')
        self.Text4 = Entry(self.Frame2, text='Text4', textvariable=self.Text4Var, font=('宋体',9))
        self.Text4.place(relx=0.411, rely=0.598, relwidth=0.276, relheight=0.104)

        self.Text5Var = StringVar(value='Text5')
        self.Text5 = Entry(self.Frame2, text='Text5', textvariable=self.Text5Var, font=('宋体',9))
        self.Text5.place(relx=0.411, rely=0.797, relwidth=0.276, relheight=0.104)

        self.style.configure('Option3.TRadiobutton', font=('宋体',9))
        self.Option3 = Radiobutton(self.top, text='频率变换', variable=self.work_mode, value=False, style='Option3.TRadiobutton')
        self.Option3.place(relx=0.077, rely=0.373, relwidth=0.086, relheight=0.064)

        self.style.configure('Option1.TRadiobutton', font=('宋体',9))
        self.Option1 = Radiobutton(self.top, text='平均值峰值调整', variable=self.work_mode, value=True, style='Option1.TRadiobutton')
        self.Option1.place(relx=0.579, rely=0.388, relwidth=0.163, relheight=0.064)

    # 可以被调用的内部函数
    def calculate_avg_peak(self, data_time: list, data_voltage: list):
        # 数据统计：
        avg_current = 0.0
        for i in range(len(data_time) - 1):
            avg_current += (data_voltage[i + 1] + data_voltage[i]) * (data_time[i + 1] - data_time[i])
        avg_current = avg_current / 2 / (data_time[len(data_time) - 1] - data_time[0])

        peak_current_over_avg = max(data_voltage) - avg_current
        # print("avg_current:", avg_current)
        # print("peak_current:", peak_current)
        return avg_current, peak_current_over_avg

    def change_avg_peak(self, data_voltage: list, avg_current: float, peak_current_over_avg: float, avg_target: float, peak_target_over_avg: float):
        # 数据变换：
        # 原数据列表为data_voltage，平均值：avg_current，峰值减均值：peak_current_over_avg
        # 目标平均值avg_target,目标峰值减均值peak_target_over_avg
        for i in range(len(data_voltage)):
            data_voltage[i] = (data_voltage[i] - avg_current) / peak_current_over_avg * peak_target_over_avg + avg_target

    def data_process(self, data_ori: list, avg_target: float, peak_target_over_avg: float, stretch: bool):
        # 对data_ori中的电流值进行变换，使得最终的平均值为avg_target，如果stretch为真，则是电流峰减去均值电流的值为peak_target_over_avg
        # stretch表示是否对波形进行y轴方向上的拉伸，如果为True，则以avg_target为中心，在y轴方向上进行拉伸，直到电流峰值达到减去avg_target的值达到peak_target_over_avg

        data_time = []
        data_voltage = []
        tmp = []
        for line in data_ori:
            data_time.append(float(line.split("ps")[0].split()[1]))
            data_voltage.append(float(line.split()[-1]))

        # 数据统计：
        avg_current, peak_current_over_avg = self.calculate_avg_peak(data_time, data_voltage)
        print("\nbefore process:")
        print("avg_current:", avg_current)
        print("peak_current_over_avg:", peak_current_over_avg)

        # 数据变换：
        # stretch表示是否对波形进行y轴方向上的拉伸
        if not stretch:
            self.change_avg_peak(data_voltage, avg_current, peak_current_over_avg, avg_target, peak_current_over_avg)
        else:
            self.change_avg_peak(data_voltage, avg_current, peak_current_over_avg, avg_target, peak_target_over_avg)

        # 数据统计：
        avg_current, peak_current_over_avg = self.calculate_avg_peak(data_time, data_voltage)
        print("\nbefore process:")
        print("avg_current:", avg_current)
        print("peak_current_over_avg:", peak_current_over_avg)

        # 编码输出数据
        for i in range(len(data_ori)):
            tmp.append("+ " + str(data_time[i]) + "ps " + str(data_voltage[i]) + '\n')
        return tmp
    
    def if_items_inline(self, item_list: list, line: str):
        # 该函数判断在line字串里是否包含item_list中的内容
        for item in item_list:
            if (" " + item + " ") in line:
                return True
        return False


class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    def power_analysis(self, event=None):
        # 此函数的作用是将gui上的信息读入实例实例变量中
        self.sp_file_path = self.Text1Var.get().replace('\\', '/')
        self.port_to_process = self.Text2Var.get().split("")

        f = open(self.sp_file_path, 'r')
        lines = f.readlines()
        f.close()

        tmp_mem = []
        start_flag = False

        avg_current = 0.0
        peak_current = 0.0

        for line in lines:
            # 此处self.port_to_process前后加空格，表示只有完全满足命名规则时才能被处理，可根据实际情况修改
            if "Icursig" in line and "pwl" in line and (" " + self.port_to_process + " ") in line:
                if start_flag:
                    print("error: Icursig endding not found")
                    f.close()
                    break
                tmp_mem = []
                start_flag = True
                continue

            if start_flag and ")" in line:
                # 运行到此处，标志当前pwl电流源已经载入完成
                # 对已经载入的电流信息进行数据统计，并且将数据显示到UI上
                data_time = []
                data_voltage = []

                for each_line in tmp_mem:
                    data_time.append(float(each_line.split("ps")[0].split()[1]))
                    data_voltage.append(float(each_line.split()[-1]))

                avg_current_tmp, peak_current_tmp = self.calculate_avg_peak(data_time, data_voltage)
                avg_current += avg_current_tmp
                peak_current = max((peak_current, abs(peak_current_tmp)))   # 此处逻辑错误，单个子电流最大峰值不一定是总电流的最大峰值。。。。待改善

                tmp_mem = []
                start_flag = False
                continue

            tmp_mem.append(line)

        # print(avg_current, peak_current)
        self.Label8.config(text=str(avg_current))
        self.Label6.config(text=str(peak_current))

    def power_change(self, event=None):
        # 此函数的作用是将gui上的信息读入实例实例变量中
        self.sp_file_path = self.Text1Var.get().replace('\\', '/')
        self.port_to_process = self.Text2Var.get().split("")
        self.avg_target = float(self.Text5Var.get())
        self.peak_target_over_avg = float(self.Text4Var.get())

        f = open(self.sp_file_path, 'r')
        lines = f.readlines()
        f.close()

        f = open(self.sp_file_path, 'w')

        start_flag = False
        tmp_mem = []

        for line in lines:
            if "Icursig" in line and "pwl" in line and self.if_items_inline(self.port_to_process, line):
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

                tmp_mem = self.data_process(data_ori=tmp_mem, avg_target=self.avg_target, peak_target_over_avg=self.peak_target_over_avg, stretch=False)
                # 此处data_process函数中stretch变量尚未在GUI中体现出来，待完善。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。

                tmp_mem.append(line)
                f.writelines(tmp_mem)
                tmp_mem = []
                start_flag = False
                continue

            tmp_mem.append(line)

        f.writelines(tmp_mem)
        f.close()

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
    try: top.destroy()
    except: pass
