from tkinter import *
from tkinter import ttk
import pymysql
import datetime
import pandas as pd

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Appshow:
	def __init__(self, root,user_name, doc_username):
		self.user = user_name
		self.doc = doc_username
		root.title(f"appointment of/ {self.user} / doctor - {self.doc}")
		root.geometry("900x300")
		self.fontl = ('Times', -20, 'bold')
		self.mailabel = Label(root, text = "Details of the patinet", font = self.fontl)
		self.mailabel.place(x = 50, y = 50)
		self.maintext = Text(root, height = 5, width = 80, state='disable')
		data_ = "Name 				Age 			Timings\n"
		self.maintext.config(state = 'normal')
		self.maintext.insert(END, data_)
		self.maintext.config(state='disable')
		self.maintext.place(x = 50, y = 100)
		self.patient_uid = None
		conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
		c = conn.cursor()
		sql = f"select * from `Patient` where username = '{self.user}'"
		c.execute(sql)
		data_ = c.fetchone()
		print(data_)
		lst = []
		lst.append(data_[1])
		lst.append(data_[6])
		val = datetime.date.today()
		self.val = str(val)
		sql = f"select * from `appoint` where p_username = '{self.user}' and d_username = '{self.doc}'"
		c.execute(sql)
		data_ = c.fetchone()
		print(data_)
		self.slot = data_[2]
		lst.append(self.slot)

		self.maintext.config(state = 'normal')
		self.txt = f"{lst[0]} 				{lst[1]} 			{lst[2]}"
		self.maintext.insert(END, self.txt)
		self.maintext.config(state = 'disable')
		sql = f"select p_uid from pat_uid where username = '{self.user}'"
		c.execute(sql)
		uid_data = c.fetchone()
		uid_data = uid_data[0]
		self.patient_uid = uid_data
		self.graphb = ttk.Button(root, text = "Get data", command = self.plot2)
		self.graphb.place(x = 700, y = 160)

		self.graphc = Canvas(root, height = 250, width = 700)
		self.window = root


	def plot2(self):
		self.window.geometry("900x500")
		self.graphc.place(x = 30, y = 200)
		try:
			patient_data_file = pd.read_csv(f"patient_data/{self.patient_uid}/department_hostpital.csv")
			x = self.dlist
			patient_data = patient_data_file.iloc[:,1].values
			print(patient_data)
			y = patient_data
			data_str = "Department vs visit"
		except:
			x = []
			y = []
			data_str = "No data yet"

		fig = Figure(figsize = (9, 2.5))
		a = fig.add_subplot(111)
		a.scatter(x, y, color = "blue")
		a.legend([data_str], loc = 4)
		a.set_title("Department vs No of visits", fontsize = 16)
		a.set_ylabel("No of visit", fontsize = 14)
		a.set_xlabel("Department", fontsize = 14)
		a.grid()
		canvas = FigureCanvasTkAgg(fig, master = self.graphc)
		canvas.get_tk_widget().pack()
		canvas.draw()


	def plot (self):
		self.window.geometry("900x500")
		self.graphc.place(x = 30, y = 200)
		data = pd.read_csv('patdata/health.csv')
		data_x = data.iloc[:,0]
		x = np.arange(1,100,0.1)
		y = x ** 2
		data_y = data.iloc[:,1]
		fig = Figure(figsize=(7,2.5))
		a = fig.add_subplot(111)
		#a.scatter(v,x,color='red')
		a.plot(data_x,data_y,color='blue')
		a.set_title ("Health value vs age", fontsize=16)
		a.set_ylabel("Health value", fontsize=14)
		#a.set_xlabel("X", fontsize=14)
		a.grid()
		canvas = FigureCanvasTkAgg(fig, master=self.graphc)
		canvas.get_tk_widget().pack()
		canvas.draw()
		self.graphb.config(state = 'disable')






if __name__ == '__main__':
	root = Tk()
	obj = Appshow(root,"sati","Ishan_gambir")
	root.mainloop()
