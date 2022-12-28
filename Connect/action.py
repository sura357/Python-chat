import socket
import struct
import json
import os
import threading
import time
from tkinter import *

#import Ninja as Ninja
#import numpy as np
import time  # 測時間
from tkinter import filedialog
from pathlib import Path
import re
import math

"""
C等待連線
連線成功，送出連線封包
等待讀取Threading + 隨時送出封包
寄出斷線封包，離開

S等待連線
連線成功，收到連線封包
等待讀取Threading + 隨時送出封包
收到斷線封包

"""


def change_show_SC(target, status, row=0, column=0):
    if (status == TRUE):
        target.grid(row=row, column=column)
    elif (status == FALSE):
        target.grid_remove()


class log:
    def __init__(self):
        self.stage = 0

    def UP(self):
        self.stage = self.stage + 1

    def DW(self):
        self.stage = self.stage - 1


    def lg(self, something):
        st = ""
        for i in range(self.stage):
            st = st + "　"

        print(st + something)

"""——————————————————————————————————————————————————————————————————————————————

　　　　　　　　　　　　　　　　　　　　　　　Server

——————————————————————————————————————————————————————————————————————————————"""


class SC:
    ip = ""
    port = 1025
    C_conn = {}
    C_ID_array = {}
    C_ID = 0
    threading_array = []
    each_piece_size = 10240*10240

    talk_count = {} # 握手計數(沒握到，越高)
    if_talk = {} # 握手布林
    def __init__(self):
        self.share_dir = r'share/'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.server



    def server_start(self, window, S_Frame, R_Frame, addlist,combo):  # 打開執行續等待
        threading_server_accept = threading.Thread(target=self.server_accept,
                                                   args=(self, window, S_Frame, R_Frame, addlist, combo))
        threading_server_accept.start()

    def server_accept(self, window, S_Frame, R_Frame, addlist, combo):  # 打開監聽
        p = log()

        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 要選擇通訊模式
            self.ip = socket.gethostbyname(socket.gethostname())  # 找 IP
            self.server.bind((self.ip, 1025))  # 正式建立連線
            self.server.listen(5)  # 監聽
            p.lg('建置完成,IP 是' + self.ip)
            window.title('Server-' + self.ip)
            p.lg('------建置Server完成')
            change_show_SC(S_Frame, TRUE, 1, 0)
            change_show_SC(R_Frame, TRUE, 2, 0)
            p.lg('------布置Server完成')
        except:
            p.lg('------Server fail,your trash.')
            return

        while True:
            conn, address = self.server.accept()
            p.lg('------新Client到來:' + str(address))
            threading_server_accept = threading.Thread(target=self.server_read,
                                                       args=(self, window, addlist, conn, address,combo))
            threading_server_accept.start()
            self.threading_array.append(threading_server_accept)


        # self.server.listen(1)  # client 數量(從 0 開始算)
        # a = self.server.settimeout(10) #當沒有人
        # 連線時可以設定時間結束->(10)10 秒
        #self.conn, self.addr = self.server.accept()  # 等待接收連線邀請紀錄
        #p.lg("server-連接成功")
        # 成功連線之後，打開 監聽Thread


    def server_read(self, window, addlist, conn, address, combo):
        """
        執行Server對於每個Client的連線讀取
        :param window:  視窗本身
        :param addlist: 顯示訊息的地方
        :param conn:    傳送工具
        :param address: IP位置
        :return:
        """
        p = log()
        ip = str(address[0])+"-"+str(address[1])
        self.C_conn[ip] = conn  # 新增key-value
        id = str(self.C_ID)

        self.C_ID_array[id] = ip
        self.talk_count[id] = 0
        self.if_talk[id] = False

        self.C_ID += 1
        self.update_C_list(self,combo)
        connect_string = "Ninja" + self.ip + "#01$@"
        conn.send(connect_string.encode())

        p.lg("新使用者建立連線：" + ip)
        p.lg("目前清單：")
        print(self.C_conn)

        hreading_server_talk_counting = threading.Thread(target=self.talk_counting,
                                                   args=(self, p, ip, id, combo))
        hreading_server_talk_counting.start()
        self.threading_array.append(hreading_server_talk_counting)
        while True:
            try:
                res = conn.recv(10240)

                try:
                    packet = ninja(res.decode('utf-8'))

                    packet.Disassemble_Ninja()
                    if packet.main_func != "0" and packet.suba_func != "2":
                        print(packet.original)


                    #print(packet.main_func)
                    if packet.main_func == "0":
                        if packet.suba_func == "0":  # 00斷線
                            self.user_disconnect(self, p, ip, id, combo)
                            return

                        elif packet.suba_func == "1":  # 01連線-for client
                            p.lg(packet.main_func + ':' + packet.suba_func)
                        elif packet.suba_func == "2":  # 02握手-for client
                            self.C_conn[ip].send(packet.original.encode('utf-8'))



                    if packet.main_func == "1":  # 10傳訊息
                        if packet.message[0:1] == "!":
                            self.S_read_message(self,packet, self.C_conn[ip])
                        else:
                            addlist.insert('end', '用戶[' + str(id) + ']：' + packet.message)

                    if packet.main_func == "2":
                        if packet.suba_func == "0":  # 20傳檔案(開始)
                            print(20)
                            file_name = packet.file_name + "." + packet.sub_name
                            total_size = packet.size
                            num = 0
                            print('開始收檔案內容-' + file_name)
                            print("大小：" + total_size)
                            with open(r'%s\%s' % ("share", file_name), 'wb') as f:
                                recv_size = 0
                                print('打開檔案成功')
                                while TRUE:
                                    line = self.C_conn[ip].recv(self.each_piece_size)
                                    # print("---")
                                    f.write(line)
                                    recv_size += len(line)
                                    num += 1
                                    if (str(recv_size) == total_size):
                                        break
                                print("is out")



                except Exception as server_read_e:
                    print(server_read_e)
                    print('server_read_e')

            except ConnectionResetError:
                self.user_disconnect(self,p, ip, id, combo)
                return
            except:
                return

    def user_disconnect(self, p, ip, id, combo):
        """
        傳資訊進來執行斷線與刪除
        """
        p.lg("使用者[" + str(id) + "]斷線了")
        del self.C_conn[ip]
        del self.C_ID_array[id]
        print(self.C_conn)
        self.update_C_list(self, combo)



    def S_read_message(self, packet,conn):
        try:
            dot_1 = packet.message.find(':')
            if packet.message[1:14] == "sendto client":
                client_number = packet.message[14:dot_1]
                client_message = packet.message[dot_1 + 1:]
                print(client_number)
                print(client_message)
                print(self.C_ID_array)
                print(self.C_conn)
                # 「防呆」檢查是否有此用戶
                if client_number in self.C_ID_array:
                    ip = self.C_ID_array[client_number]
                    print("查IP")

                else:
                    print('無此用戶，回傳錯誤訊息')
                    return_packet = ninja()
                    return_packet.host = self.ip
                    return_packet.main_func = 1
                    return_packet.suba_func = 0
                    return_packet.message = "無此用戶"
                    return_message = return_packet.Assemble_Ninja()
                    conn.send(return_message.encode('utf-8'))
                    return

                self.C_conn[ip].send(client_message.encode('utf-8'))



        except Exception as S_read_message_e:
            print(S_read_message_e)
            print('S_read_message_e')


    def server_write_message(self, text, addlist, combo):
        """
        先包裝訊息封包，再進行送出動作。
        :param text: 文字方塊
        :param addlist: 訊息清單
        :return: null
        """
        if text.get()=="":
            addlist.insert('end', '無法傳送空訊息')
            return

        packet = ninja()
        packet.host = self.ip
        packet.main_func = 1
        packet.suba_func = 0
        packet.message = text.get()
        self.conn_send(self,combo,packet.Assemble_Ninja())
        addlist.insert('end', 'server-送出:' + text.get())
        #packet.

    def conn_send(self,combo,text):
        """
        送出傳送檔案的 開頭 (會區分是否為廣播 或 單傳)
        :param combo: combobox 元件
        :param text: 傳送內容 字串
        :return: None
        """
        ip = combo.get()
        if ip == "All Client":
            for key, value in self.C_conn.items():
                value.send(text.encode('utf-8'))
        else:
            self.C_conn[ip].send(text.encode('utf-8'))
        #print(ip)
        #print(self.C_conn[ip])


        # self.conn.send(cmd.encode('utf-8'))


    #################################################
    def chose_file1(self, addlist,combo):
        threading_chose_file = threading.Thread(target=self.chose_file2, args=(self, addlist, combo))
        threading_chose_file.start()

    def chose_file2(self, addlist, combo):
        p = log()
        p.lg('選擇檔案-------')
        file_path = filedialog.askopenfilename()
        p.lg('選擇完畢-------')
        print(file_path)
        if not file_path:
            # 沒有選擇檔案
            p.UP()
            p.lg('沒有選擇檔案')
            p.DW()
            addlist.insert('end', 'S-file path is empty: QAQ')
            return
        else:
            # 有選擇檔案

            packet = ninja()
            packet.host = self.ip
            packet.main_func = 2
            packet.suba_func = 0

            # condtion = 'a(.+?)b'
            # file_p = re.findall(r'' + condtion, file_path)
            packet.size = str(Path(file_path).stat().st_size)

            packet.total_times = str(math.ceil(float(packet.size) / float(self.each_piece_size)))

            file_begin = file_path.rfind('/')
            filesub_begin = file_path.rfind('.')
            packet.file_name = file_path[file_begin + 1:filesub_begin]
            packet.sub_name = file_path[filesub_begin + 1:]

            send = packet.Assemble_Ninja()

            print(send)
            # 送出傳送檔案的 開頭 (會區分是否為廣播 或 單傳)
            self.conn_send(self, combo, send)

            ip = combo.get()

            file_array=[];

            if ip == "All Client":
                for key, value in self.C_conn.items():
                    addlist.insert('end', 'Server-廣播:' + send)
                    print("傳送給"+key)
                    # 開始送出後續資料
                    file_array.append(threading.Thread(target=self.send_fileroad,
                                                               args=(self, file_path, packet, key)))
                for thing in file_array:
                    thing.start()
            else:
                addlist.insert('end', 'Server-單傳:' + send)
                # 開始送出後續資料
                threading_send_fileroad = threading.Thread(target=self.send_fileroad,
                                                           args=(self, file_path, packet, ip))
                threading_send_fileroad.start()



    def send_fileroad(self, file_path, packet, ip):
        try:
            packet.suba_func = 1  # 改成目前/結束
            alltime = packet.total_times
            packet.total_times = 0
            pointer = 0

            timer = timing()
            print('傳送內容')
            print(file_path)
            #i=0
            with open(file_path, 'rb') as f:
                for line in f:
                    self.C_conn[ip].send(line)
                    #print(i)
                    #i+=1
            print("END")
            print("傳送檔案-執行時間：" + str(round(timer.endTiming(), 4)) + "秒")
        except Exception as send_fileroad_e:
            # print(send_fileroad_e)
            """exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print('send_fileroad_e')"""


    #################################################
    def update_C_list(self, com):
        com["value"] = []
        list = []

        for key in self.C_conn:
            list.append(key)

        if len(list) !=0:

            list.insert(0,"All Client")

        com["value"] = list

    def dis_connect(self, window, connect, com):
        print('傳送斷線封包')
        packet = ninja()
        packet.main_func = 0
        packet.suba_func = 0
        packet.host = self.ip
        packet.Assemble_Ninja()

        print(packet.original)
        self.C_conn.clear()
        self.update_C_list(self, com)
        """for key in self.C_conn:
            self.C_conn[key].send(packet.original.encode('utf-8'))

        for key in self.C_conn:
            del self.C_conn[key]"""

        window.title('Server- 已斷線')
        change_show_SC(connect, FALSE)

        del self.client

    def talk_counting(self, p, ip, id, combo):
        while True:
            if self.talk_count[id] == True:
                self.talk_count[id] = False
                self.talk_count[id] = 0
                time.sleep(8)
            else:
                self.talk_count[id] += 1

                if self.talk_count[id] >= 6:
                    self.user_disconnect(self, p, ip, id, combo)



"""——————————————————————————————————————————————————————————————————————————————

　　　　　　　　　　　　　　　　　　　　　　　Client

——————————————————————————————————————————————————————————————————————————————"""


class CC:
    ip = ""
    port = 1025
    close = TRUE
    Handshake = False
    handshake_meesage = ""
    each_piece_size = 10240*10240
    th=[]
    def __init__(self):
        self.share_dir = r'share/'
        self.location = ''
        self.client
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

    def client_start(self, window, connect):
        change_show_SC(connect, TRUE, 1, 0)
        self.ip = socket.gethostbyname(socket.gethostname())  # 找 IP
        window.title('client- 請選擇連線')

    def client_connect(self, window, connect, C_Frame, R_Frame, text, addlist):
        try:
            download_dir = r'download/'
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 網路通訊,tcp
            self.location = text.get()
            self.client.connect((self.location, 1025))
            change_show_SC(connect, FALSE)
            change_show_SC(C_Frame, TRUE, 1, 0)
            change_show_SC(R_Frame, TRUE, 2, 0)
            window.title('client- 已連線')
            # 用於判斷是否結束
            self.close = False

            threading_client_read = threading.Thread(target=self.client_read, args=(self, window, addlist))
            threading_client_read.start()

        except:
            addlist.insert('end', '連線失敗')
            window.title('client- 連線失敗')

    def client_read(self, window, addlist):
        while self.close == False: # 如果沒被關閉的話，就讀訊息
            try:
                res = self.client.recv(10240)
            except:
                try:
                    window.title('client- 斷線')
                    change_show_SC()
                except:
                    break
                break

            if not res:
                continue

            try:
                packet = ninja(res.decode('utf-8'))

                packet.Disassemble_Ninja()
                # print(packet.main_func + packet.suba_func)
                if packet.main_func != "0" and packet.suba_func != "2":
                    print(packet.original)

                if packet.main_func == "0":
                    if packet.suba_func == "0":  # 00斷線
                        i = 0
                    elif packet.suba_func == "1":  # 01連線
                        print("連線成功")

                        self.handshake = True
                        self.handshake_meesage = "Ninja" + packet.host + "#02$@"
                        threading_handshaking = threading.Thread(target=self.handshaking, args=(self,))
                        threading_handshaking.start()

                    elif packet.suba_func == "2":  # 02握手
                        # print("收到握手")
                        i=0

                if packet.main_func == "1":  # 10傳訊息
                    # print(2)
                    addlist.insert('end', 'client-收到：' + packet.message)

                if packet.main_func == "2":
                    if packet.suba_func == "0":  # 20傳檔案(開始)
                        self.handshake = False
                        print(20)
                        file_name = packet.file_name + "." + packet.sub_name
                        total_size = packet.size
                        num = 0
                        print('開始收檔案內容-' + file_name)
                        print("大小：" + total_size)
                        with open(r'%s\%s' % ("share", file_name), 'wb') as f:
                            recv_size = 0
                            print('打開檔案成功')
                            while TRUE:
                                line = self.client.recv(self.each_piece_size)
                                # print(line)
                                f.write(line)
                                recv_size += len(line)
                                num += 1
                                if (str(recv_size) == total_size):
                                    break
                            print("is out")

                            self.handshake = True

                    elif packet.suba_func == "1":  # 21傳檔案(途中 - 結束)
                        self.C_read_file_Road(packet)

            except Exception as client_read_e:
                print(client_read_e)
                print('client_read_e')
                return




    def client_write_message(self, text, addlist):
        try:
            cmd = text.get()  # input('>>: ').strip()
            packet = ninja()
            packet.main_func = 1
            packet.suba_func = 0
            packet.host = self.ip
            packet.message = cmd
            message = packet.Assemble_Ninja()

            self.client.send(message.encode('utf-8'))
            addlist.insert('end', 'client-送出：' + cmd)
        except:
            addlist.insert('end', 'client-送出訊息失敗')

    ################################################################
    def chose_file2(self, addlist, combo):
        p = log()
        p.lg('選擇檔案-------')
        file_path = filedialog.askopenfilename()
        p.lg('選擇完畢-------')
        print(file_path)
        if not file_path:
            # 沒有選擇檔案
            p.UP()
            p.lg('沒有選擇檔案')
            p.DW()
            addlist.insert('end', 'C-file path is empty: QAQ')
            self.handshake = True
            return
        else:
            # 有選擇檔案
            self.handshake = False
            packet = ninja()
            packet.host = self.ip
            packet.main_func = 2
            packet.suba_func = 0

            # condtion = 'a(.+?)b'
            # file_p = re.findall(r'' + condtion, file_path)
            packet.size = str(Path(file_path).stat().st_size)

            packet.total_times = str(math.ceil(float(packet.size) / float(self.each_piece_size)))

            file_begin = file_path.rfind('/')
            filesub_begin = file_path.rfind('.')
            packet.file_name = file_path[file_begin + 1:filesub_begin]
            packet.sub_name = file_path[filesub_begin + 1:]

            send = packet.Assemble_Ninja()
            self.close = True
            print(send)
            # 送出傳送檔案的 開頭
            self.client.send(send.encode('utf-8'))
            addlist.insert('end', 'client-送出:' + send)
            # 開始送出後續資料
            threading_send_fileroad = threading.Thread(target=self.send_fileroad,
                                                       args=(self, file_path, packet, combo))
            threading_send_fileroad.start()
            # threading_send_fileroad.join()

    def chose_file1(self, addlist, combo):
        threading_chose_file = threading.Thread(target=self.chose_file2, args=(self, addlist, combo))
        threading_chose_file.start()

    def send_fileroad(self, file_path, packet, combo):
        try:

            packet.suba_func = 1  # 改成目前/結束
            alltime = packet.total_times
            packet.total_times = 0
            pointer = 0
            ip = combo.get()
            timer = timing()

            print('傳送內容')
            print(file_path)
            with open(file_path, 'rb') as f:
                for line in f:
                    self.client.send(line)
                    #print(line)
            print("END")
            print("傳送檔案-執行時間："+str(round(timer.endTiming(),4))+"秒")
            self.handshake = True
        except Exception as send_fileroad_e:
            print(send_fileroad_e)
            print('send_fileroad_e')

    ################################################################
    def dis_connect(self, window = None, connect = None):

        packet = ninja()
        packet.main_func = 0
        packet.suba_func = 0
        packet.host = self.ip
        packet.Assemble_Ninja()
        print('傳送斷線封包')
        print(packet.original)
        self.client.send(packet.original.encode('utf-8'))

        if window != None:
            window.title('client- 已斷線')
            change_show_SC(connect, FALSE)


        self.close = TRUE
        del self.client

    def handshaking(self):
        """
        握手thread
        :return:
        """
        try:
            while self.close == False:
                while self.handshake == True:
                    self.client.send(self.handshake_meesage.encode('utf-8'))
                    # print("hand")
                    time.sleep(5)
        except Exception as handshaking_e:
            print(handshaking_e)
            print('handshaking_e')
            return




class ninja:
    head = "Ninja"
    host = ""
    main_func = 0
    suba_func = 0
    message = ""
    size = ""
    total_times = ""
    sub_name = ""
    file_name = ""

    def __init__(self, all=""):
        self.original = all
        self.len = len(self.original)

    def Disassemble_Ninja(self):

        try:
            self.dot_1 = self.original.find('#')  # 「#」
            self.dot_2 = self.original.rfind('$')  # 「$」
            self.dot_3 = self.original.rfind('@')  # 「@」

            self.head = self.original[0:5]  # head:「Ninja」
            self.host = self.original[5:self.dot_1]  # host:「127.0.0.1」
            self.main_func = self.original[self.dot_1 + 1:self.dot_1 + 2]  # main_func:「1」
            self.suba_func = self.original[self.dot_1 + 2:self.dot_1 + 3]  # suba_func:「1」

            # if int(self.main_func) == 0:
            print(self.main_func)
            if int(self.main_func) == 1:
                self.message = self.original[self.dot_2 + 1:self.dot_3]
                print("取出訊息"+self.message)
            if int(self.main_func) == 2:
                self.dot_4 = self.original.rfind('?')  # 「?」
                self.dot_5 = self.original.rfind('!')  # 「!」
                self.dot_6 = self.original.rfind('&')  # 「&」

                self.size = self.original[self.dot_2 + 1: self.dot_4]
                self.total_times = self.original[self.dot_4 + 1: self.dot_5]
                self.sub_name = self.original[self.dot_5 + 1: self.dot_6]
                self.file_name = self.original[self.dot_6 + 1: self.dot_3]

            return TRUE
        except:
            #print('封包拆解錯誤')
            return FALSE

    def Assemble_Ninja(self):  # yj
        if int(self.main_func) == 0:
            self.original = self.head + self.host + "#" + str(self.main_func) + str(self.suba_func) + "@"
        if int(self.main_func) == 1:
            self.original = self.head + self.host + "#" + str(self.main_func) + str(self.suba_func) + "$" + self.message + "@"
        if int(self.main_func) == 2:
            self.original = self.head + self.host + "#" + \
                            str(self.main_func) + str(self.suba_func) + "$" + \
                            str(self.size) + "?" + str(self.total_times) + "!" + \
                            str(self.sub_name) + "&" + str(self.file_name) + "@"
        return self.original





    def print_Ninja(self):
        print(self.head)
        print(self.host)
        print(self.main_func)
        print(self.suba_func)

        if int(self.main_func) == 2 & int(self.suba_func) == 0:
            print(self.size)
            print(self.total_times)
            print(self.sub_name)
            print(self.file_name)

    # ---------------------------------------Server_parse

    # ---------------------------------------Client_parse


def close_window(win, CL, SV):
    try:
        i=1
        CL.dis_connect(CL)
        #CL.close = True
        #CL.handshake = False

    except Exception as close_window_e:
        print(close_window_e)
        print('close_window_e')

    try:
        for key,conn in SV.C_conn.items():
            conn.close()
        #for thread_ in SV.threading_array:
            #thread_.

    except Exception as close_window_e:
        print(close_window_e)
        print('close_window_e')
    os._exit(0)
    win.destroy()


class timing:
    start = 0
    end = 0
    def __init__(self):
        self.start = time.time()

    def endTiming(self):
        self.end = time.time()

        return (self.end - self.start)