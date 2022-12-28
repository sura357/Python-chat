from tkinter import *
from tkinter import ttk, Frame
from functools import partial

import action

SV = action.SC
CL = action.CC

class GU:

    def __init__(self):
        self.Windows
        self.read_message

    def frame(self): #父容器

        self.S_Frame = Frame(self.Windows, bg='lime', width=400, height=400)
        #self.S_Frame.grid(row=0, column=0)

        self.C_connect_Frame = Frame(self.Windows, bg='yellow', width=400, height=400)
        self.C_Frame = Frame(self.Windows, bg='orange', width=400, height=400)
        #self.C_Frame.grid(row=1, column=0)

        self.read_Frame = Frame(self.Windows, bg='yellow', width=400, height=400)
        #self.read_Frame.grid(row=2, column=0)



    def menu_(self):
        # 創建菜單框架
        self.menu = Menu(self.Windows)

        # tearoff=False 關閉菜單裡的虛線欄
        self.filemenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(menu=self.filemenu, label='chose')
        self.C_combo = ttk.Combobox(self.S_Frame, state='readonly')
        self.filemenu.add_command(label='Server',
                                  command=partial(SV.server_start, SV, self.Windows, self.S_Frame, self.read_Frame, self.read_message,self.C_combo))
        self.filemenu.add_command(label='Client',
                                  command=partial(CL.client_start, CL, self.Windows, self.C_connect_Frame))

        self.Windows.config(menu=self.menu)



    def S_Frame_(self): #布置s容器
        self.T_server = Entry(self.S_Frame, text="", width=30)
        self.T_server.insert(0, "")
        self.T_server.grid(row=0, column=0)


        self.C_combo.grid(row=2, column=0)

        self.B_server_send = Button(self.S_Frame, text="S送出",
                                    command=partial(SV.server_write_message, SV, self.T_server, self.read_message, self.C_combo))  # , command=partial(SV.server_start, SV, self.T_server.get())
        self.B_server_send.grid(row=0, column=1)

        self.B_server_file = Button(self.S_Frame, text="S傳送檔案" ,command=partial(SV.chose_file1, SV, self.read_message, self.C_combo))
        self.B_server_file.grid(row=2, column=1)
        self.B_client_discont = Button(self.S_Frame, text="S斷線",
                                       command=partial(SV.dis_connect, SV, self.Windows, self.S_Frame, self.C_combo))
        self.B_client_discont.grid(row=3, column=1)

    def C_connect_Frame_(self):
        self.T_connect = Entry(self.C_connect_Frame, text="")
        self.T_connect.insert(0, "")
        self.T_connect.grid(row=0, column=0)

        self.B_connect_send = Button(self.C_connect_Frame, text="連線",
                                    command=partial(CL.client_connect, CL, self.Windows, self.C_connect_Frame, self.C_Frame, self.read_Frame, self.T_connect, self.read_message))
        self.B_connect_send.grid(row=0, column=1)

    def C_Frame_(self): #布置c容器
        self.T_client = Entry(self.C_Frame, text="", width=30)
        self.T_client.insert(0, "")
        self.T_client.grid(row=0, column=0)

        self.B_client_send = Button(self.C_Frame, text="C送出",
                                    command=partial(CL.client_write_message, CL, self.T_client, self.read_message))
        self.B_client_send.grid(row=0, column=1)
        self.B_client_file = Button(self.C_Frame, text="C傳送檔案",
                                    command=partial(CL.chose_file1, CL, self.read_message, self.C_combo))
        self.B_client_file.grid(row=2, column=1)
        self.B_client_discont = Button(self.C_Frame, text="C斷線",
                                    command=partial(CL.dis_connect, CL, self.Windows, self.C_Frame))
        self.B_client_discont.grid(row=3, column=1)


    def read_Frame_(self): #布置read容器
        var = StringVar()
        #var.set(['內容一', '內容二'])
        self.read_message = Listbox(self.read_Frame, listvariable=var, width=50, height=22)
        self.read_message.grid(row=1, column=0)
        #self.read_message.insert('end', "yee")


    def win(self):
        # 視窗
        self.Windows = Tk()
        self.Windows.title('Connect')
        self.Windows.geometry("350x200+550+400")

        self.frame(self)
        self.read_Frame_(self)
        self.menu_(self)

        self.S_Frame_(self)
        self.C_Frame_(self)
        self.C_connect_Frame_(self)

        self.Windows.protocol("WM_DELETE_WINDOW", partial(action.close_window, self.Windows, CL, SV))
        # loop
        self.Windows.mainloop()

# ------------------------------------------------------------------------------------------------