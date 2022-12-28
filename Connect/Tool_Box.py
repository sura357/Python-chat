from tkinter import *
from tkinter import ttk

###「」


#############################################################「容器」

###「視窗」(標題,視窗大小)
class form:
    def begin(self,title,size):
        self.form = Tk()
        self.form.title(title)
        self.form.geometry(size)

    def loop(self):
        self.form.mainloop()


###「分頁本(母)」
class notebook:
    def pack(self,form):
        self.notebook = ttk.Notebook(form)
        self.notebook.pack(pady=15)


###「分頁本(子)」(分頁本(母),分頁文字標題,寬,高)
class page:
    def pack(self,note,txt,width,height):
        self.FRAME = Frame(note, width=width, height=height)
        self.FRAME.pack(fill="both", expand=1)

        note.add(self.FRAME, text=txt)  ###「加入」

        self.PUT = Frame(self.FRAME)                    ## 「PUT」 = 物件要放的地方
        self.PUT.pack(side=TOP)

###「Form」(目標,寬,高
class frame:
    def pack(self,goto,width,height):
        self.FRAME = Frame(goto, width=width, height=height)
        self.FRAME.pack(fill="both", expand=1)



#############################################################「物件」

###「標籤」(來源,文字內容,列,列位)
class label:
    def pack(self,pg,text,row,column):
        self.LABEL = Label(pg, text=text)
        self.LABEL.grid(row=row, column=column)


###「輸入框」(來源,文字內容,列,列位)
class entry:
    def pack(self,pg,text,row,column):
        self.ENTRY = Entry(pg, text=text)
        self.ENTRY.insert(0, text)
        self.ENTRY.grid(row=row, column=column)

###「多行輸入框」()
class text:
    def pack(self, pg):
        self.text = Text(pg,
                      width=44,
                      height=4,
                      font=('arial', 14),
                      foreground='gray')
        self.text.pack()

###「按鈕」(來源,文字內容,列,列位,按鈕事件)
class button:
    def pack(self,pg,text,row,column,computer):
        self.BUTTON = Button(pg, text=text, command=computer)
        self.BUTTON.grid(row=row, column=column)

###「單選按鈕」(來源,文字內容,共同值,代表值,列,列位)8
class radiobutton:
    def pack(self, pg, text,variable,value,row, column,computer):
        self.RADIOBUTTON = Radiobutton(pg, text=text, variable=variable, value=value,command=computer)
        self.RADIOBUTTON.grid(row=row, column=column)



###「畫布」
class canvas:
    def pack(self,pg,row,column,img):
        self.cv = Canvas(pg,bg = 'white',width = 512,height= 512)
        self.cv.grid(row=row, column=column)



###「滑桿」#set(來源,標題文字,高,長,事件)     #pack(初始,最小,最大,間隔,位數,列,列位)
class scale:
    def set(self,pg,text,width,length,computer):#(來源,標題文字,高,長,事件)
        # 方向, 寬度, 長度
        self.SCALE = Scale(pg,orient=HORIZONTAL, width=width, length=length,command=computer)
        # 標題
        self.SCALE.config(label=text)

    def pack(self,first,min,max,tickinterval,digits,row,column):#(初始,最小,最大,間隔,位數,列,列位)
        # 設置範圍 mini 10 ~ max 100
        # 顯示value, 間隔刻度:10, 解析度, 設置顯示位數:0
        self.SCALE.config(from_=min, to=max,showvalue=1, tickinterval=tickinterval, resolution=1, digits=digits)

        # 預設值
        self.SCALE.set(first)

        self.SCALE.grid(row=row, column=column)


class picturebox:
    def pack(self,pg,row,column):#,fileform
        #self.img_gif = PhotoImage(file=fileform)
        self.label_img = Label(pg)#, image=self.img_gif
        self.label_img.grid(row=row, column=column)

    def set(self,changeimage):
        self.img_gif = PhotoImage(file=changeimage)
        self.label_img.config(image = self.img_gif)

