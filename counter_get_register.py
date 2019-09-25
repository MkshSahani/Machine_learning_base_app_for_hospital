# for the registrtion as counter
from tkinter import *
import pandas as pd
from tkinter import ttk
from tkinter import messagebox
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pymysql
import os

class ConterRegister:
    def __init__(self, root,uid):

        self.patuid = uid
        self.window =  root
        self.window.geometry("1300x600")
        self.window.title("Registration counter")
        self.window.resizable(0, 0)

        ### graph
        self.graphc = Canvas(self.window, height = 250, width = 700)
        self.graphc.place(x = 50, y = 200)


        self.dlabelfont = ('Times', -30, 'bold underline')
        self.departmenetlabel = Label(self.window, text = "Select Department", font = self.dlabelfont)
        self.departmenetlabel.place(x = 1000, y = 30)
        self.dlist = ["Medicine","ENT Specialist", "Eye Specialist","Heart Specialist","Allergist","Psychiatrist","Surgeon"]
        self.cdept = IntVar()
        self.dfont = ('Times', -25, 'bold')
        self.d1 = Radiobutton(self.window, text = "Medicine", variable = self.cdept, value = 1, font = self.dfont)
        self.d1.place(x = 1000, y = 100)
        self.d2 = Radiobutton(self.window, text = "ENT Specialist", variable = self.cdept, value = 2, font = self.dfont)
        self.d2.place(x = 1000, y = 150)
        self.d3 = Radiobutton(self.window, text = "Eye Specialist", variable = self.cdept, value = 3, font = self.dfont)
        self.d3.place(x = 1000, y = 200)
        self.d4 = Radiobutton(self.window, text = "Heart Specialist", variable = self.cdept, value = 4, font = self.dfont)
        self.d4.place(x = 1000, y = 250)
        self.d5 = Radiobutton(self.window, text = "Allergist", variable = self.cdept, value = 5, font = self.dfont)
        self.d5.place(x = 1000, y = 300)
        self.d6 = Radiobutton(self.window, text = "Psychiatrist", variable = self.cdept, value = 6, font = self.dfont)
        self.d6.place(x = 1000, y = 350)
        self.d7 = Radiobutton(self.window, text = "Surgeon", variable = self.cdept, value = 7, font = self.dfont)
        self.d7.place(x = 1000, y = 400)
        self.register_data = ttk.Button(self.window, text = "Register", command = self.register_data, width = 30)
        self.register_data.place(x = 1000, y = 450)
        self.exit_button = ttk.Button(self.window, text = "Exit", command =  self.exit_button, width = 30)
        self.exit_button.place(x = 1000, y = 500)
        conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
        c = conn.cursor()
        sql = f"select username from pat_uid where p_uid = {self.patuid}"
        c.execute(sql)
        data = c.fetchone()
        self.user_name = data[0]
        self.user_name = data[0]
        print(self.user_name)
        sql = f"select * from Patient where username = '{self.user_name}'"
        c.execute(sql)
        conn.close()
        self.maindata = c.fetchone()
        self.window.title(f"Welcome {self.maindata[1]} {self.maindata[2]}")
        print(self.maindata)

        ### data feeding in the Value
        self.mlfont = ('Times', -30, 'bold underline')
        self.mlabel = Label(root, text = "Patient profile", font = self.mlfont)
        self.mlabel.place(x = 10, y = 10)
        self.txtdata = f"UID Number : {self.patuid}\n"
        self.txtdata += f"Username : {self.maindata[0]} \t\t Name : {self.maindata[1]} {self.maindata[2]}"
        self.txtdata += f"\nAddress : {self.maindata[3]} \temail : {self.maindata[5]}"
        self.mainmessage = Message(self.window, text = self.txtdata, width = 450)
        self.mainmessage.place(x = 60, y = 90)
        self.res = True

        try:
            datafile = pd.read_csv(f"patient_data/{self.patuid}/department_hostpital.csv")
            x = self.dlist
            patient_data = datafile.iloc[:,1].values
            print(patient_data)
            patient_data = list(patient_data)
            y = patient_data
            data_str = "Department vs visit"
        except:
            x = []
            y = []
            data_str = "No data yet"
        fig = Figure(figsize=(9,2.5))
        a = fig.add_subplot(111)
        #a.scatter(v,x,color='red')
        a.scatter(x, y, color = "blue")
        a.legend([data_str], loc = 4)
        a.set_title ("Department vs No of visits", fontsize=16)
        a.set_ylabel("No of visit", fontsize=14)
        a.set_xlabel("Department", fontsize=14)
        a.grid()
        canvas = FigureCanvasTkAgg(fig, master=self.graphc)
        canvas.get_tk_widget().pack()
        canvas.draw()
        self.notefont =  ('Times', -20, 'bold underline')
        self.notelabel  = Label(self.window, text = "Note: Medicine department is selected if you not select any department", font = self.notefont)
        self.notelabel.place(x = 10, y = 550)
    def exit_button(self):
        self.window.destroy()
        os.system("python3 counter_camera.py")


    def register_data(self):
        reg_dept = self.cdept.get()
        print(f"this is the number : {reg_dept}")
        print(reg_dept)
        if reg_dept not in [i for i in range(0, len(self.dlist) + 1)]:
            messagebox.showinfo("Info", "Please choose Department.")
        else:
            try:
                if self.res ==  True:
                    data_file_load = pd.read_csv(f"patient_data/{self.patuid}/department_hostpital.csv")
                    print(data_file_load)
                    # data_from_patient = pd.DataFrame(data_file_load)
                    # print(data_from_patient)
                    patient_data = data_file_load.iloc[:,1].values
                    print(patient_data)
                    patient_data = list(patient_data)
                    patient_data[reg_dept - 1] += 1
                    print(patient_data)
                    dict_data = {}
                    dict_data[self.patuid] = patient_data
                    data_frame_result = pd.DataFrame(dict_data)
                    data_frame_result.to_csv(f"patient_data/{self.patuid}/department_hostpital.csv")
                    print("registerd")
                    messagebox.showinfo("Info","Your name is registerd.\nPlease go to the department.")
                    self.res = False
                else:
                    messagebox.showinfo("Info","You are already registered.\nPlease exit the window\n")
            except FileNotFoundError:
                 dict_data = {}
                 data_list = [0 for i in range(0,len(self.dlist))]
                 data_list[reg_dept - 1] += 1
                 dict_data[self.patuid] = data_list
                 data_frame_result = pd.DataFrame(dict_data)
                 data_frame_result.to_csv(f"patient_data/{self.patuid}/department_hostpital.csv")
                 messagebox.showinfo("Info","You are already registered.\nPlease exit the window\n")



if __name__ == '__main__':
    root = Tk()
    obj = ConterRegister(root, 61003)
    root.mainloop()
