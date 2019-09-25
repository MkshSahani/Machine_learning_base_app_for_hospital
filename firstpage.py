# first page of the application


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os

import pymysql

import signup2
import ambulance

class Firstpage:
	def __init__(self, root):
		#root.wm_iconbitmap("/home/mukesh/Desktop/ipdgui_/index.ico")
		root.title("Mr.Dr")
		root.geometry("1000x600")
		root.resizable(0, 0)
		self.back = PhotoImage(file = "back.gif")
		self.backlabel = Label(root, image = self.back)
		self.backlabel.pack()


		self.backframe = Frame(root, bg = 'white', height = 500, width = 325)
		self.backframe.place(x = 650, y = 50)

		self.fontt = ('Times', -30, 'bold underline')
		self.loginlabel = Label(root, text = 'Log in', font =  self.fontt, bg = 'white')
		self.loginlabel.place(x = 750, y = 100)

		self.usernamel = Label(root, text = 'User name : ', font = ('Times', -20, 'bold'), bg = 'white')
		self.usernamel.place(x = 680, y = 200)

		self.workas_  = Label(root, text = ' Log in as  : ', font = ('Times', -20, 'bold'), bg = 'white')
		self.workas_.place(x = 680, y = 250)

		self.usernamee = Entry(root, font = ('Times', -20, 'bold'), bg = 'white', width = 15)
		self.usernamee.place(x = 790, y = 200)

		self.work = StringVar()
		self.pos = ('Doctor', 'Patient')

		self.workaspin = Spinbox(root, value = self.pos, textvariable = self.work, font = ('Times', -20, 'bold'), width = 14)
		self.workaspin.place(x = 790, y = 250)

		self.confirml = Label(root, text = 'Confirm  : ', font = ('Times', -20, 'bold'), bg = 'white')
		self.confirml.place(x = 690, y = 300)

		self.confirmb = ttk.Button(root, text = 'Confirm', width = 18, command = self.confirmb)
		self.confirmb.place(x = 790, y = 300)

		self.ambb = ttk.Button(root, text = 'Ambulance log in', command = self.ambulancelogin)
		self.ambb.place(x = 680, y = 350)

		self.signup = ttk.Button(root, text = 'Sign up', width = 16, command = self.signupuser)
		self.signup.place(x = 820, y = 350)
		self.window = root

	def confirmb(self):
		work_ = self.work.get()
		username = self.usernamee.get()

		if username == "":
			messagebox.showinfo("info","please enter a user name")
		else:

			if work_ == "Doctor":
				conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
				sql = f"select * from `Doctor` where username = '{username}'"
				c = conn.cursor()
				c.execute(sql)
				conn.commit()
				data = c.fetchone()
				work_ = "docdata"
				conn.close()
				if data == None:
					messagebox.showinfo("info","you are not registered please register youself")
				else:
					self.window.destroy()
					work_ = work_.lower()
					os.system(f"python3 third.py {work_} {username}")

			else:
				conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mukesh', db = 'mrdr')
				sql = f"select * from `Patient` where username = '{username}'"
				c = conn.cursor()
				c.execute(sql)
				conn.commit()
				data = c.fetchone()

				conn.close()
				if data == None:
					messagebox.showinfo("info","you are not registered please register youself")
				else:
					self.window.destroy()
					work_ = work_.lower()
					work_ = "patdata"
					os.system(f"python3 third.py {work_} {username}")

	def signupuser(self):
		self.window.destroy()
		signuproot = Tk()
		signupobj = signup2.Signup(signuproot, True)
		signuproot.mainloop()


	def ambulancelogin(self):
		self.window.destroy()
		ambroot = Tk()
		ambobj = ambulance.Ambulance(ambroot)
		ambobj.plotdata()
		ambroot.mainloop()

if __name__ == "__main__":
	root1 = Tk()
	obj = Firstpage(root1)
	root1.mainloop()
