#this is ambulance tab

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter import ttk
from socket import *
import pymysql
from threading import *

class Ambulance:
	def __init__(self, root):
		root.title("Ambulance server tab")
		root.geometry("1360x768")

		self.count = 0

		self.menubar = Menu(root)
		root.config(menu = self.menubar)

		self.ambmenu = Menu(root, tearoff = 0)
		self.ambmenu.add_command(label = "Close server", command = self.closeserver)
		self.ambmenu.add_command(label = "Exit", command = root.destroy)
		self.menubar.add_cascade(label = "Ambulance", menu = self.ambmenu)

		self.graphc = Canvas(root, height = 300, width = 700)
		self.graphc.place(x = 300, y = 100)

		self.fontbig = ('Times', -50, 'bold')
		self.amblancelabel = Label(root, text = "Ambulance server..", font = self.fontbig)
		self.amblancelabel.place(x = 500, y = 20)

		self.plabel = Label(root, text = "Place", bg = 'white')
		self.plabel.place(x = 700, y = 370)


		######## registered cases


		self.rlabel = Label(root, text = "Registered case")
		self.rlabel.place(x = 200, y = 430)



		######### txt for the registred casesss............
		self.registerframe = Frame(root, height = 400, width = 600, bg = 'pink')
		self.registerframe.place(x = 100, y = 450)
		self.registertext = Text(self.registerframe, width=130, height=8, font=("Helvetica", 12))
		self.registertext.pack(side="left", fill="y")
		self.scrollbar = Scrollbar(self.registerframe, orient="vertical")
		self.scrollbar.config(command=self.registertext.yview)
		self.scrollbar.pack(side="right", fill="y")
		self.registertext.config(yscrollcommand=self.scrollbar.set)


		data  = "s.no		fname		sname		address		location" + "\t\t\tphone 			email"
		self.registertext.insert(END, data)
		self.registertext.config(state = 'disable')
		self.close = False

		self.regdata = None
		self.reg = False
	def plotdata(self):
		x = [5,6,7,8,8]
		y = [14,10,11,5,15]
		label_ = ["a","b","c","d","e"]
		fig = Figure(figsize=(8,3))
		a = fig.add_subplot(111)
		#a.scatter(v,x,color='red')
		a.bar(x,y,tick_label = label_)
		a.set_title ("place vs cases", fontsize=16)
		a.set_ylabel("cases")
		#a.set_xlabel("place")
		a.grid()
		canvas = FigureCanvasTkAgg(fig, master=self.graphc)
		canvas.get_tk_widget().pack()
		canvas.draw()


	def startserver(self):
		self.h = '127.0.0.1'
		self.p = 9003
		self.s = socket()
		self.s.bind((self.h, self.p))
		self.s.listen(5)
		if self.close == True:
			self.s.close()
		else:
			while True:
				c,addr = self.s.accept()
				print("a emerency")
				data = c.recv(1024)
				data = data.decode()
				data = str(data)
				self.dataworking(data)
				self.regdata = data
				c.close()
				if self.close == False:
					pass
				else:
					break
				#do something with that data
			#self.s.close()
	def closeserver(self):
		self.close = True
		self.s.close()


	def dataworking(self, d):
		conn = pymysql.connect(host = 'localhost', user = 'root', password = "mukesh", db = 'mrdr')
		c = conn.cursor()
		self.regdata = d
		print(self.regdata)
		if self.regdata != None:
			self.registertext.config(state = 'normal')
			val = self.regdata.split("-")
			username = val[0]
			print(username)

			location = val[1]
			print(location)
			self.count += 1
			sql = f"select * from Patient where username = '{username}'"
			c.execute(sql)
			data = c.fetchone()
			print(data)
			fname = data[1]
			lname = data[2]
			address_ = data[3]
			phone_ = data[4]
			email = data[5]
			data1 = f"\n{self.count}		{fname}		{lname}		{address_}		{location}		   \t{phone_}		  {email}"
			self.registertext.insert(END, data1)
			self.registertext.config(state = 'disable')
			self.regdata = None
			if self.close == True:
				conn.close()
		else:
			if self.close == True:
				conn.close()


if __name__ == "__main__":
	root = Tk()
	obj = Ambulance(root)
	obj.plotdata()
	t1 = Thread(target = obj.startserver)
	t1.start()
	root.mainloop()
