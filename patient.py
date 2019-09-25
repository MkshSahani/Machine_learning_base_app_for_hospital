import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter import ttk
import re
from socket import *

import pymysql
#self defined modules.........
import mail
#import softcure
import appointment

import os
from pynput.mouse import Controller
from tkinter import messagebox
import patient_mail_gen
import mail

class Patient:
	def __init__(self, root, username):
		self.cur = Controller()
		self.user_name = username
		root.title(f"patient tab/ {self.user_name}")
		root.geometry("1360x768")
		self.patient_uid = None
		self.graphc = Canvas(root, height = 250, width = 700)
		self.graphc.place(x = 255, y = 30)


		self.menubar = Menu(root)
		self.menubar.config(bg = 'sky blue')
		root.config(menu = self.menubar)

		##########doctor menu
		self.doctormenu = Menu(root, tearoff = 0)
		self.doctormenu.add_command(label = "Get Appointment", command = self.appoint)
		self.doctormenu.add_command(label = "Complaint", command = self.comp)
		self.doctormenu.add_command(label = "Exit", command = root.destroy)

		###########ambulance
		self.ambmenu = Menu(root, tearoff = 0)
		self.ambmenu.add_command(label = "Call ambulance", command = self.amm)
		self.ambmenu.add_command(label = "Complaint", command = self.comp)

		self.menubar.add_cascade(label = "Doctor", menu = self.doctormenu)
		self.menubar.add_cascade(label = "Ambulance", menu = self.ambmenu)

		self.ambframe = Frame(root, height = 250, width = 300, bg = 'blue')
		self.ambframe.place(x = 10, y = 30)
		self.font1 = ('Times', -20, 'bold')
		self.amblabel = Label(root, text = 'Call Ambulance', fg = 'white', bg = 'blue', font = self.font1)
		self.amblabel.place(x = 60, y  = 60)
		self.ambl = Label(root, text = "Enter location", fg  = 'white', bg = 'blue', font = self.font1)
		self.ambl.place(x = 20, y = 110)
		self.add = ttk.Entry(root, font = self.font1, width = 28)
		self.add.place(x = 20, y = 145)
		self.call = ttk.Button(root, text = 'call location at this addresss', command = self.callambulance)
		self.call.place(x = 50, y = 180)



		#machine curing.........

		self.machinecuref = Frame(root, height = 250, width = 290, bg = 'blue')
		self.machinecuref.place(x = 1070, y = 30)

		self.dislabel = Label(root, text = 'description :', bg = 'blue', fg = 'white')
		self.dislabel.place(x = 1090, y = 50)

		self.ditext = Text(root, height = 5, width = 29)
		self.ditext.insert(END,"This part is build on\nyour visit to the doctor\na mail will send to you for\n health tips")
		self.ditext.config(state = 'disable')
		self.ditext.place(x = 1090, y = 80)

		self.cbu = ttk.Button(root, text = 'Soft cure', width = 30, command = self.soft_cure_function)
		self.cbu.place(x = 1090, y = 200)
		#lower mailing opetion

		self.dlist = ["Medicine","ENT Specialist", "Eye Specialist","Heart Specialist","Allergist","Psychiatrist","Surgeon"]
		self.mailf = Frame(root, height = 100, width = 1360, bg = 'blue')
		#self.mailf.place(x = 0, y = 1200)
		self.mailf.pack(side =  BOTTOM, pady = 20)
		self.font3 = ('Times', -30, 'bold')
		self.mail = Label(root, text = "Send comment : ", fg = 'white', bg = 'blue', font = self.font3)
		self.mail.place(x = 20, y = 580)

		self.mailtext = Text(root, height = 4, width = 110)
		self.mailtext.place(x = 270, y = 580)
		#self.mailtext.config(state = 'disable')
		self.mailsend = Button(root, text = 'Send', font = self.font3, command = self.sendmail)
		self.mailsend.place(x = 1200, y = 590)
		self.window = root
		self.tipindex = None
		self.amb = True
		self.deplabel = None

	def amm(self):
		self.cur.move(0, 200)

	def comp(self):
		self.cur.move(500, 600)

	def appoint(self):
		os.system(f"python3 appointment.py {self.user_name}")

	def plot (self):
		data = pd.read_csv('patient_data/61000/department_hostpital.csv')
		data_x = data.iloc[:,1].values
		data_y = dlist = ["Medicine","ENT Specialist", "Eye Specialist","Heart Specialist","Allergist","Psychiatrist","Surgeon"]
		fig = Figure(figsize=(9,2.5))
		a = fig.add_subplot(111)
		a.scatter(data_y,data_x,color='blue')
		a.legend(["Department vs visit"], loc = 4)
		a.set_title ("Department vs No of visits", fontsize=16)
		a.set_ylabel("No of visits", fontsize=14)
		a.grid()
		canvas = FigureCanvasTkAgg(fig, master=self.graphc)
		canvas.get_tk_widget().pack()
		canvas.draw()


	def callambulance(self):
		if self.amb == True:
			try:
				self.h = '127.0.0.1'
				self.p = 9003
				s = socket()
				s.connect((self.h, self.p))
				data =  self.add.get()
				data = self.user_name + "-" + data
				s.send(data.encode())
				s.close()
				self.amb = False
				messagebox.showinfo("Ambulance","Your Request has been registerd")
			except:
		 		messagebox.showinfo("info","Ambulance server is not responding")
		else:
			messagebox.showwarning("info","Your request is already registered")

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
			sql = f"select email from `Doctor` where username = '{doc}'"
			c.execute(sql)
			docmail_ =  c.fetchone()
			conn.close()

			#structure the mail.........

			reg1 = r"\S+@\S+"
			refrence_ = re.findall(reg1,main_text)
			refrence = "Refrence -- these are the email accounts that user mention in the message \n"
			for i in refrence_:
				refrence = refrence + i + "\n"

			msgtext = "Message : \n"
			msgtext = msgtext + main_text

			body =  msgtext + refrence
			try:
				mail.mail_function(docmail_[0], body)
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
				messagebox.showinfo("info","mail not sended \nplease connect to internet")

			messagebox.showinfo("info",f"the mail sended to doctor {doc}")
			print("mail sended.......")
		except:
			messagebox.showinfo("info","the username you entered not found")

	def get_uid(self):
		sql_server = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
		sql_cursor = sql_server.cursor()
		sql = f"select p_uid from pat_uid where username = '{self.user_name}'"
		sql_cursor.execute(sql)
		data = sql_cursor.fetchone()
		data = data[0]
		data = data
		self.patient_uid = data
		print(self.patient_uid)
		sql_server.close()

	def plot_graph(self):
		try:
			patient_data_file = pd.read_csv(f"patient_data/{self.patient_uid}/department_hostpital.csv")
			x = ["Medicine","ENT Specialist", "Eye Specialist","Heart Specialist","Allergist","Psychiatrist","Surgeon"]
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

	def mltab_funtion(self):
		print(self.patient_uid)
		try:
			data_file_load = pd.read_csv(f"patient_data/{self.patient_uid}/department_hostpital.csv")
			print(data_file_load)
			patient_data = data_file_load.iloc[:,1].values
			print(patient_data)
			patient_data = list(patient_data)
			max_visit_department = max(patient_data)
			max_index = patient_data.index(max_visit_department)
			self.tipindex = max_index
			dlist = ["Medicine","ENT Specialist", "Eye Specialist","Heart Specialist","Allergist","Psychiatrist","Surgon"]
			data_department = dlist[max_index]
		except:
			data_department = "Not Have Enough Data"
		self.depfont = ('Times', -50, 'bold underline')
		self.deplabel = Label(self.window, text = "Consulting To : "  + data_department, font =  self.depfont)
		self.deplabel.place(x = 400, y = 350)

	def soft_cure_function(self):
		try:
			sql_server = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
			sql_cursor = sql_server.cursor()
			sql_statement = f"select email from Patient where username = '{self.user_name}'"
			sql_cursor.execute(sql_statement)
			mail_address = sql_cursor.fetchone()
			mail_address = mail_address[0]
			sql_server.close()
			filelist = ["tips_medicine_patient.txt","tips_ent_patient.txt","tips_eye_patient.txt","tips_heart_patient.txt","tips_allergy_patient.txt","tips_psycho_patient.txt","tips_surgery_patient.txt"]
			fname = filelist[self.tipindex]
			print(fname)
			file = open(str(fname), 'r')
			send_txt = file.read()
			dlist = ["Medicine","ENT Specialist", "Eye Specialist","Heart Specialist","Allergist","Psychiatrist","Surgon"]
			file.close()
			mail_body = patient_mail_gen.gen_patient_mail("system",dlist[self.tipindex],send_txt,mail_address)
			mail.mail_function(mail_address, mail_body)
			print(f"mail sent {mail_address} department {dlist[self.tipindex]}")
			messagebox.showinfo("Info","tips are sended on you mail.")
		except:
			message.showinfo("Info","Some Error Occured.")
if __name__ == "__main__":
	root = Tk()
	obj = Patient(root,"sati")
	obj.get_uid()
	obj.plot_graph()
	obj.mltab_funtion()
	root.mainloop()
