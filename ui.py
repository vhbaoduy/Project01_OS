from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter import Frame, Label, Entry
import win32api

drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000') [:-1]




class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Đồ án Hệ điều hành")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self)
        frame1.pack(fill=X)

        txt1 = Label(frame1, text = 'UNIVERSITY OF SCIENCE', font =("Georgia", 14))
        txt1.pack(anchor = N, padx=5, pady=3)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        txt2 = Label(frame2, text="FACULTY OF INFORMATION TECHNOLOGY", font=("Georgia", 12))
        txt2.pack(anchor = N, padx=5, pady=3)

        symbol = Label(frame2, text=" ~~~ ", font=("Georgia", 12))
        symbol.pack(anchor=N, padx=5)

        txt3 = Label(frame2, text="OPERATING SYSTEM", font=("Georgia", 12))
        txt3.pack(anchor=N, padx=5, pady=3)

        txt4 = Label(frame2, text="Project: File System Management", font=("Georgia", 12), bg='navy', fg='white', width=32)
        txt4.pack(anchor=N, padx=5, pady=3)

        txt5= Label(frame2, text="  Teacher: Lê Viết Long", font=("Georgia", 12))
        txt5.pack(side=LEFT, padx=5, pady=3, fill = BOTH)

        frame3 = Frame(self)
        frame3.pack(fill=BOTH, expand=True)

        stu = "  Students: Võ Hoàng Bảo Duy - 19127027 \n              Trần Ngọc Lam - 19127040\n     Lê Minh Sĩ - 19127064"
        txt6 = Label(frame3, text=stu, font=("Georgia", 12))
        txt6.pack(side=LEFT, padx=5, pady=3)


root = Tk()
# root.geometry("500x300+300+300")
app = Example(root)
root.mainloop()