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


class ShowMessage:
	def __init__(self, root,user_name, doc_username):
		self.user = user_name
		self.doc = doc_username
		root.resizable(0,0)
		root.title(f"Message / from - {self.user} / to - {self.doc}")
		root.geometry("900x500")
		self.fontl = ('Times', -20, 'bold')
		self.mailabel = Label(root, text = "Details of the patinet", font = self.fontl)
		self.mailabel.place(x = 50, y = 50)
		self.maintext = Text(root, height = 5, width = 80, state='disable')
		data_ = "Name 				Age 			phone no\n"
		self.maintext.config(state = 'normal')
		self.maintext.insert(END, data_)
		self.maintext.config(state='disable')
		self.maintext.place(x = 50, y = 100)
		conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
		c = conn.cursor()
		sql = f"select * from Patient where username = '{self.user}'"
		c.execute(sql)
		data_ = c.fetchone()
		print(data_)
		lst = []
		lst.append(data_[1])
		lst.append(data_[6])
		lst.append(data_[4])


		self.maintext.config(state = 'normal')
		self.txt = f"{lst[0]} 				{lst[1]} 			{lst[2]}"
		self.maintext.insert(END, self.txt)
		self.maintext.config(state = 'disable')


		################################# message tab ###########################################

		self.ml = Label(root, text = "Message", font = self.fontl)
		self.ml.place(x = 50, y = 200)
		self.mtab = Text(root, height = 10, width = 80, state = 'disable')
		self.mtab.place(x = 50, y = 250)

		sql = f"select * from message where sender = '{self.user}' and reciver = '{self.doc}'"
		c.execute(sql)
		data_ = c.fetchall()

		lst = list(data_)
		self.mtab.config(state = 'normal')
		for i in range(len(lst)):
			data = "\n" + str(i+1) + str(". ")
			self.mtab.insert(END, data)
			self.mtab.insert(END, lst[i][2])

		self.mtab.config(state = 'disable')

		self.graphb = ttk.Button(root, text = "Get data", command = self.plot)
		self.graphb.place(x = 700, y = 160)

		self.graphc = Canvas(root, height = 250, width = 700)
		self.window = root


	def plot (self):
		self.window.geometry("800x700")
		self.graphc.place(x = 30, y = 430)
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
	obj = ShowMessage(root,"@test","satvik115")
	root.mainloop()
