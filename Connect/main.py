import Gui as GUI
import action as ACT
import math
import sys
sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=10, cols=10))

'''class APP:

    def __init__(self, gui, act):
        self.gui = gui
        self.act = act

    def ap(self):
        print(555)

    def start(self):
        self.window = self.gui.Window('Connect', '400', '400', '550', '400')
        self.window.pack()

        self.menu = self.gui.menu(self.window.Windows)
        self.menu.add('server', self.ap)  # SV.server_start
        self.menu.add('client', self.ap)  # CL.client_start


        self.window.end()




app = APP(GUI, ACT)
app.start()'''
"""packet = ACT.ninja("Ninjaserver#20$1034?1!spec&main@")
print(packet.original)
packet.Disassemble_Ninja()
print(packet.host)
print(packet.main_func)
print(packet.suba_func)
print(packet.size)
print(packet.total_times)
print(packet.file_name)
print(packet.sub_name)
"""

menu = GUI.GU
menu.win(menu)
