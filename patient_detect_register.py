# patient detected for the

from tkinter import *
from tkinter import ttk
from threading import *
import os
import time
import signup2
import pymysql
from tkinter import messagebox

# self created modules

import counter_get_register

class PatientDetect:
    def __init__(self, root):
        self.window = root
        self.window.geometry("700x300")
        self.window.title("Confirmation for UID")
        self.window.resizable(0, 0)
        self.qfont = ('Times', -30, 'bold underline')
        self.qlabel = Label(self.window, text = "Do you have the UID number ?", font = self.qfont)
        self.qlabel.place(x = 150, y = 50)
        self.nobutton = ttk.Button(self.window, text = "No", width = 15, command = self.no_uid)
        self.nobutton.place(x = 100, y = 170)
        self.yesbutton = ttk.Button(self.window, text = "YES", width = 15, command = self.yes_uid)
        self.yesbutton.place(x = 250, y = 170)
        self.exitbutton = ttk.Button(self.window, text = "EXIT", width = 15, command = self.exit_uid)
        self.exitbutton.place(x = 400, y = 170)

    def no_uid(self):
        self.window.destroy()
        root = Tk()
        obj = signup2.Signup(root, False)
        root.mainloop()

    def yes_uid(self):
        self.window.destroy()
        root = Tk()
        obj = EnterUID(root)
        root.mainloop()

    def exit_uid(self):
        self.window.destroy()
        os.system("python3 counter_camera.py")



class EnterUID:
    def __init__(self, root):
        self.window = root
        self.window.geometry("650x200")
        self.window.title("Enter your UID number")
        self.window.resizable(0, 0)
        self.ffont = ('Times', -25, 'bold underline')
        self.fffont = ('Times', -25, 'bold')
        self.label = Label(self.window, text = "Your UID number : ", font = self.ffont)
        self.euid = ttk.Entry(self.window, font = self.fffont)
        self.label.place(x = 20, y = 50)
        self.euid.place(x = 250, y = 50)
        self.okbutton = ttk.Button(self.window, text = "Enter", command = self.get_data)
        self.okbutton.place(x = 520, y = 50)
        self.notelabel = ttk.Label(self.window, text = "Note : UID is sended on you registered mail.Please check you mail for you UID number.")
        self.notelabel.place(x = 10, y = 170)
        self.uid = ""
    def get_data(self):
        self.uid = self.euid.get()
        if self.uid == "":
            messagebox.showinfo("Info","Pleaes enter a UID Number")
        else:
            conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
            lst = []
            c = conn.cursor()
            lst.append(self.uid)
            try:
                val = list(map(int, lst))[0]
            except:
                messagebox.showinfo("Info","Please enter a valid UID number.")
            sql = f"select * from pat_uid where p_uid = {val}"
            c.execute(sql)
            data = c.fetchone()
            if data is not None:
                self.window.destroy()
                root = Tk()
                obj = counter_get_register.ConterRegister(root, self.uid)
                root.mainloop()

            else:
                messagebox.showinfo("Info","This UID number is not registered")

if __name__ == '__main__':
    root = Tk()
    obj = EnterUID(root)
    root.mainloop()
