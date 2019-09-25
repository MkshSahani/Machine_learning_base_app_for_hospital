from tkinter import *
from tkinter import ttk 
from tkinter import messagebox


import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import mail
import pymysql
import pandas as pd
import appshow
import showm
import mail_gen


class Doctor:
	def __init__(self, root, user):
		self.user_name = user
		root.geometry("1360x768")
		root.title(f"doctor/ {self.user_name}")

		self.menubar = Menu(root)
		root.config(menu = self.menubar)

		self.helpmenu = Menu(root, tearoff = 0)
		self.helpmenu.add_command(label = "Help")
		self.helpmenu.add_command(label = "Exit", command = root.destroy)
		self.menubar.add_cascade(label = 'Help', menu = self.helpmenu)

		###### status bar

		self.statusbar  = Label(root, relief = SUNKEN, text = 'this is the status bar', anchor = W)
		self.statusbar.pack(side = BOTTOM, fill = X)


		#graph.....
		self.graphc = Canvas(root, height = 250, width = 700)
		self.graphc.place(x = 340, y = 30)
		#graph.....


		# tab for machine learning the prediction
		self.mllabel = Label(root, text = "Machine prediction")
		self.mllabel.place(x = 200, y = 320)
		self.mltext = Text(root, height = 10, width = 120, state = 'disable')
		self.mltext.place(x = 200, y = 340)


		######    appointment
		self.applabel =  Label(root, text = "Today appointment")
		self.applabel.place(x = 20, y = 30)
		self.appframe = Frame(root, height = 400, width = 300, bg = 'pink')
		self.appframe.place(x = 10, y = 50)
		self.applist = Listbox(self.appframe, width=20, height=10, font=("Helvetica", 12))
		self.applist.pack(side="left", fill="y")
		self.scrollbar = Scrollbar(self.appframe, orient="vertical")
		self.scrollbar.config(command=self.applist.yview)
		self.scrollbar.pack(side="right", fill="y")
		self.applist.config(yscrollcommand=self.scrollbar.set)

		self.applist.bind('<<ListboxSelect>>', self.appointmentab)

		conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
		c = conn.cursor()
		sql = f"select * from `appoint` where d_username = '{self.user_name}'"
		c.execute(sql)
		data = c.fetchall() 
		print(data)
		data = list(data)
		print(data)
		conn.close()
		for i in range(0, len(data)):
			self.applist.insert(END, data[i][1])


		#######   message
		self.mgslabel =  Label(root, text = "Patient's message")
		self.mgslabel.place(x = 1170, y = 30)
		self.msgframe = Frame(root, height = 400, width = 300, bg = 'pink')
		self.msgframe.place(x = 1100, y = 50)
		self.msglist = Listbox(self.msgframe, width=20, height=10, font=("Helvetica", 12))
		self.msglist.pack(side="left", fill="y")
		self.scrollbar2 = Scrollbar(self.msgframe, orient="vertical")
		self.scrollbar2.config(command=self.msglist.yview)
		self.scrollbar2.pack(side="right", fill="y")
		self.msglist.config(yscrollcommand=self.scrollbar2.set)

		self.msglist.bind('<<ListboxSelect>>', self.messagetabl)

		conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
		c = conn.cursor()
		sql = f"select * from `message` where reciver = '{self.user_name}'"
		c.execute(sql)
		data = c.fetchall() 
		data = list(data)
		conn.close()
		print(data)
		for i in range(0,len(data)):
			self.msglist.insert(END, data[i][0])


		####### mailing

		self.mailf = Frame(root, height = 100, width = 1360, bg = 'blue')
		#self.mailf.place(x = 0, y = 1200)
		self.mailf.place(x = 0, y = 585)
		self.font3 = ('Times', -30, 'bold')
		self.mail = Label(root, text = "Send comment : ", fg = 'white', bg = 'blue', font = self.font3)
		self.mail.place(x = 20, y = 600)

		self.mailtext = Text(root, height = 4, width = 110)
		self.mailtext.place(x = 270, y = 600)
		#self.mailtext.config(state = 'disable')
		self.mailsend = Button(root, text = 'Send', font = self.font3, command = self.sendmail)
		self.mailsend.place(x = 1200, y = 610)



	########	mailing function............


	def sendmail(self):
		body = self.mailtext.get(0.0, END)
		print(body)
		reg = r"@[\w]+"
		docusername = re.search(reg, body)
		doc = docusername.group()
		doc = doc[1:]
		print(doc)

		body = body[len(doc)+2 : ]
		main_text = body
		try:
			conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
			c = conn.cursor()
			sql = f"select email from `Patient` where user_name = '{doc}'"
			c.execute(sql)
			docmail_ =  c.fetchone()
			conn.close()

			#structure of the mail
				
			msgtext = main_text
			body =  mail_gen.generate_mail("Doctor",self.user_name, msgtext, doc)

			print("mail sended.......")

			try:
				mail.mail_function(docmail_[0], body)
				self.mailtext.delete('1.0', END)
				messagebox.showinfo("info",f"the mail sended to patient {doc}")
				conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
				c = conn.cursor()
				sql = f"insert into `message` values('{self.user_name}', '{doc}','{main_text}')"
				c.execute(sql)
				conn.commit()
				conn.close()

			except:
				conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
				c = conn.cursor()
				sql = f"insert into `message` values('{self.user_name}', '{doc}','{main_text}')"
				c.execute(sql)
				conn.commit()
				conn.close()
				
				
				
		except:
			messagebox.showinfo("info","the username you entere not found \n or you are not online")


	def appointmentab(self, event):
		index = self.applist.curselection()
		pa = self.applist.get(index)
		print(pa)

		approot = Tk()
		appobj = appshow.Appshow(approot, pa, self.user_name)
		approot.mainloop()

	def messagetabl(self, event):
		index = self.msglist.curselection()
		pa = self.msglist.get(index)
		print(pa)
		msgroot = Tk()
		msgobj = showm.ShowMessage(msgroot,pa,self.user_name)
		msgroot.mainloop()


	def plot_graph(self):
		datafile = pd.read_csv("docdata/probleam.csv")
		print(datafile)
		x = datafile.iloc[:, 2]
		print(x)
		y = datafile.iloc[:, 1]
		print(y)
		fig = Figure(figsize=(7,2.5))
		a = fig.add_subplot(111)
		#a.scatter(v,x,color='red')
		a.bar([1,2,3,4],x,tick_label = y,color='blue')
		a.set_title ("Patient no vs disease", fontsize=16)
		a.set_ylabel("No of patient", fontsize=14)
		a.set_xlabel("disease", fontsize=14)
		a.grid()
		canvas = FigureCanvasTkAgg(fig, master=self.graphc)
		canvas.get_tk_widget().pack()
		canvas.draw()

if __name__ == "__main__":
	root1 = Tk()
	obj = Doctor(root1, "master")
	obj.plot_graph()
	root1.mainloop()