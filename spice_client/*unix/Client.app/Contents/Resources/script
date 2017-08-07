# coding=utf-8
from Tkinter import *
import tkMessageBox
import socket
import webbrowser



class Login_Frame:
    def __init__(self):
        self.login_text = Label(root, text = "Логин:")
        self.login_text.grid(row = 0)
        self.login_text.config(height = 4, width = 10, font=("Helvetica", 14))
        self.password_text = Label(root, text = "Пароль:")
        self.password_text.grid(row= 1)
        self.password_text.config(height = 4, width = 10, font=("Helvetica", 14))
        self.login = Entry(root)
        self.login.grid(row= 0, column= 1, padx=(10, 10))
        self.password = Entry(root, show = "*")
        self.password.grid(row= 1, column= 1)
        self.view_pass = Checkbutton(root, text = "Показать пароль", font=("Helvetica", 12), command = self.show_pass)
        self.view_pass.grid(row = 2, column = 1)
        self.login_button = Button(root, text = "Войти", font=("Helvetica", 14))
        self.login_button.grid(row = 3, columnspan = 2, pady=(20, 20))
        self.login_button.config(height = 3, width = 30)
        self.login_button.bind("<Button-1>", self.send)
    def show_pass(self):
        if self.password.cget("show") == '':
            self.password.config(show = '*')
        else:
            self.password.config(show='')
    def send(self, event):
        print("SEND")
        login_pass = self.login.get() + " " + self.password.get()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('10.11.1.75', 23004))
        sock.send(login_pass)
        data = sock.recv(1024)
        if data == "ERROR 204":
            tkMessageBox.showinfo("Ошибка", data +
            " За данным пользователем не закреплено ни одной машины.")
        elif data == "ERROR 401":
            tkMessageBox.showinfo("Ошибка", data +
            " Такого пользователя не существует.")
        webbrowser.open(data)
        sock.close()

root = Tk()
root.title("Авторизация")
obj = Login_Frame()
root.mainloop()
