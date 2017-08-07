# coding=utf-8
from Tkinter import *
import tkMessageBox
import psycopg2


class Login_Frame:
     def __init__(self):
          self.login_text = Label(root, text = "Логин")
          self.login_text.grid(row = 0, sticky = W)

          self.password_text = Label(root, text = "Виртуальная машина")
          self.password_text.grid(row= 1)


          self.login = Entry(root)
          self.login.grid(row= 0, column= 1)

          self.password = Entry(root, show = "*")
          self.password.grid(row= 1, column= 1)


          self.login_button = Button(root, text = "Добавить")
          self.login_button.grid(row = 4, columnspan = 2)
          self.login_button.bind("<Button-1>", self.send)


     def send(self, event):
         print("SEND")
         login_pass = self.login.get() + " " + self.password.get()

         conn = psycopg2.connect("host=localhost dbname=out_db user=dima")

         cur = conn.cursor()

         cur.execute("SELECT * FROM foreign_table_users;")

         # print(cur.fetchall())

         rows_users = cur.fetchall()

        for item in rows_users:
            item[0].rstrip()

         if "0" in rows_users:
            print "find"



root = Tk()
obj = Login_Frame()
root.mainloop()
