from boot_sector_fat32 import Mbr, BootSector, PartitionEntry, PartitionTable, PbrFat
from partition_boot_sector_ntfs import RawStruct, BootSector, Bpb
import tkinter
import tkinter as tk
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter import Frame, Label, Entry
from tkinter import ttk
from PIL import Image, ImageTk
import win32api
import win32file

# drives = win32api.GetLogicalDriveStrings()
# drives = drives.split('\000') [:-1]




class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def Tab1(self, tab1):

        frame1 = Frame(tab1)
        frame1.pack(fill=X)

        txt1 = Label(frame1, text = 'UNIVERSITY OF SCIENCE', font =("Georgia", 14))
        txt1.pack(anchor = N, padx=5, pady=3)

        frame2 = Frame(tab1)
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

        frame3 = Frame(tab1)
        frame3.pack(fill=BOTH, expand=True)

        stu = "  Students: Võ Hoàng Bảo Duy - 19127027 \n              Trần Ngọc Lam - 19127040\n     Lê Minh Sĩ - 19127064"
        txt6 = Label(frame3, text=stu, font=("Georgia", 12))
        txt6.pack(side=LEFT, padx=5, pady=3)

        frame3.img= Image.open("Ảnh1.png")

        icon = ImageTk.PhotoImage(frame3.img)
        label = Label(frame3, image=icon)
        label.image = icon
        label.pack()

    def onClick(self,selected_drive):
        print(selected_drive.get())
        print(win32api.GetVolumeInformation(selected_drive.get())[4])

    def callback(self,eventObject):
        # you can also get the value off the eventObject
         return eventObject.widget.get()
        # to see other information also available on the eventObject
        # print(dir(eventObject))

    def Tab2(self,tab2):
        frame1 = Frame(tab2)
        frame1.pack(fill=X)

        label1 = Label(frame1, text = 'Select drive', font=("Georgia", 10))
        label1.grid(column = 2 , row = 5, padx=10, pady=25)

        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        for drive in drives:
            print(win32api.GetVolumeInformation(drive)[4])

        selected_drive = tkinter.StringVar()
        combobox = ttk.Combobox(frame1, textvariable = selected_drive)
        combobox['value'] = drives
        combobox['state'] = 'readonly'
        combobox.grid(column = 3, row = 5, padx=10, pady=25)

        button = tkinter.Button(frame1, text = 'Show', font=("Georgia", 10), command =lambda: self.onClick(selected_drive))
        button.grid(column = 4, row = 5, padx=10, pady=25)

    def initUI(self):
        self.parent.title("Đồ án Hệ điều hành")
        self.pack(fill=BOTH, expand=True)
        tab_control = ttk.Notebook(self)

        tab1 = ttk.Frame(tab_control)

        tab2 = ttk.Frame(tab_control)

        tab_control.add(tab1, text="Group's Information")

        tab_control.add(tab2, text="Drive's Information")

        self.Tab1(tab1)
        self.Tab2(tab2)
        tab_control.pack(expand=1, fill='both')



root = Tk()
root.geometry("500x300+300+300")
app = Example(root)
root.mainloop()