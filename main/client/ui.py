# import tkinter as tk
# from tkinter import simpledialog
# from Client import Client
#
# class UserInterface(Client):
#     def __init__(self, host, port):
#         super().__init__(host, port)
#         self.root = tk.Tk()
#         self.root.withdraw()  # 隐藏主窗口
#
#     def login_or_register(self):
#         answer = simpledialog.askstring("登录/注册", "选择 'login' 或 'register':")
#         if answer == "login":
#             self.login()
#         elif answer == "register":
#             self.register()
#         else:
#             print("无效的输入，请输入 'login' 或 'register'。")