from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql
import datetime
import sys
class Appointment:
	def __init__(self, root, pattt):
		self.pa = pattt
		root.geometry("900x400")
		root.resizable(0, 0)
		root.title("appointment")

		#################### docotor list ######################

		self.applabel = Label(root, text = "please choose a doctor")
		self.applabel.place(x = 30, y = 20)
		self.appframe = Frame(root, height = 400, width = 300, bg = 'pink')
		self.appframe.place(x = 10, y = 50)
		self.applist = Listbox(self.appframe, width=20, height=10, font=("Helvetica", 12), selectmode = SINGLE)
		self.applist.pack(side="left", fill="y")
		self.scrollbar = Scrollbar(self.appframe, orient="vertical")
		self.scrollbar.config(command=self.applist.yview)
		self.scrollbar.pack(side="right", fill="y")
		self.applist.config(yscrollcommand=self.scrollbar.set)
		self.applist.bind('<<ListboxSelect>>', self.generate)

		self.doctext = Text(root, height = 5, width = 120)
		self.doctext.place(x = 20, y = 300)

		bodytext =  "fname\t\tlname\t\taddress\t\t\t\tphone\t\temail"
		self.doctext.insert(END, bodytext)
		self.doctext.config(state = 'disable')
		conn = pymysql.connect(host =  'localhost', user = 'root', password ='mukesh', db = 'mrdr')
		c = conn.cursor()

		sql = "select * from Doctor"
		c.execute(sql)
		data = c.fetchall()
		conn.close()
		for x in range(0,len(data)):
		    self.applist.insert(END, data[x][0])


		###############		appoint ment slot

		self.tl = Label(root, text = "Time - slot : ", font = ('Times', -20, 'bold'))
		self.tl.place(x = 250, y = 50)

		self.times = ("9-10","10-11","11-12","12-13","15-16","16-17")
		self.timing = StringVar()

		self.app = Spinbox(root, values = self.times, textvariable = self.timing,font = ('Times', -20, 'bold'), width = 10)
		self.app.place(x = 370, y =  50)

		self.appb = ttk.Button(root, text = "Get appointment", width = 30, command = self.getapp)
		self.appb.place(x = 250, y = 100)

		self.generatepdf = ttk.Button(root, text = "Generate pdf", width = 30)
		self.generatepdf.place(x = 250, y = 150)


		self.exitb = ttk.Button(root, text = "Exit", width = 30, command = root.destroy)
		self.exitb.place(x = 250, y = 200)


		############   make it registerd..........
		'''

		self.regtext = Text(root, height = 10, width = 40)
		self.regtext.place(x = 600, y = 50)


		self.username = ""
		'''


	def generate(self, event):
		self.doctext.config(state = 'normal')
		self.doctext.delete(0.0, END)
		bodytext =  "fname\t\tlname\t\taddress\t\t\t\tphone\t\temail"
		self.doctext.insert(END, bodytext)
		self.doctext.config(state = 'disable')
		conn = pymysql.connect(host =  'localhost', user = 'root', password ='mukesh', db = 'mrdr')
		c = conn.cursor()

		self.indexs = self.applist.curselection()

		self.username = self.applist.get(self.indexs)

		sql = f"select * from `Doctor` where username = '{self.username}'"
		c.execute(sql)
		data = c.fetchone()
		conn.close()
		self.doctext.config(state = 'normal')
		data_ = f"\n{data[1]}\t\t{data[2]}\t\t{data[3]}\t\t\t\t{data[4]}\t{data[5]}"
		self.doctext.insert(END, data_)
		self.doctext.config(state =  'disable')



	def getapp(self):
		#try:
		print(self.timing.get())
		conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
		c = conn.cursor()
		sql = f"select * from `appoint` where time_slot = '{self.timing.get()}' and d_username = '{self.username}'"
		c.execute(sql)
		data = c.fetchone()
		if data == None:
			d = datetime.date.today()
			val = str(d)
			sql = f"insert into `appoint` values('{self.username}','{self.pa}','{self.timing.get()}','{val}')"
			c.execute(sql)
			conn.commit()
			conn.close()
			messagebox.showinfo("info","Your appointment is fixed \nthanks for using the app")
		else:
			messagebox.showinfo("info","This time slot is already taken")
			conn.close()

if __name__ == '__main__':
	root = Tk()
	obj = Appointment(root, sys.argv[1])
	root.mainloop()
