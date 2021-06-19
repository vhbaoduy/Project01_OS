from boot_sector_fat32 import *
from partition_boot_sector_ntfs import *
from mbr import *
import tkinter
from tkinter import *
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter import Frame, Label, Entry
from tkinter import ttk
from PIL import Image, ImageTk
import win32api
import win32file

# drives = win32api.GetLogicalDriveStrings()
# drives = drives.split('\000') [:-1]




class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def Tab1(self, tab1):

        frame1 = Frame(tab1, bg="#fffbe6")
        frame1.pack(fill=X)

        txt1 = Label(frame1, text='UNIVERSITY OF SCIENCE', font=("Georgia", 14, 'bold'), bg="#fffbe6")
        txt1.pack(anchor = N, padx=5, pady=3)

        frame2 = Frame(tab1, bg="#fffbe6")
        frame2.pack(fill=X)

        txt2 = Label(frame2, text="FACULTY OF INFORMATION TECHNOLOGY", font=("Georgia", 12, 'bold'), bg="#fffbe6")
        txt2.pack(anchor=N, padx=5, pady=10)

        symbol = Label(frame2, text=" ~~~ ", font=("Georgia", 12), bg="#fffbe6")
        symbol.pack(anchor=N, padx=5)

        txt3 = Label(frame2, text="OPERATING SYSTEM", font=("Georgia", 12), bg="#fffbe6")
        txt3.pack(anchor=N, padx=5, pady=5)

        txt4 = Label(frame2, text="Project: Manage file system on Windows", font=("Georgia", 14, 'bold'),
                     bg='#0D4CB2', fg='white', width=34)
        txt4.pack(anchor=N, padx=5, pady=20)

        txt5= Label(frame2, text="  Teacher: Lê Viết Long", font=("Georgia", 12), bg="#fffbe6")
        txt5.pack(anchor='w', side=LEFT, padx=5, pady=20, fill=BOTH)

        frame3 = Frame(tab1, bg="#fffbe6")
        frame3.pack(fill=BOTH, expand=True)

        stu = "  Students:  Võ Hoàng Bảo Duy - 19127027 \n              Trần Ngọc Lam - 19127040\n      Lê Minh Sĩ - 19127064"
        txt6 = Label(frame3, text=stu, font=("Georgia", 12), bg="#fffbe6")
        txt6.pack(anchor='n', side=LEFT, padx=5, pady=20)

        frame3.img= Image.open("Ảnh1.png")

        icon = ImageTk.PhotoImage(frame3.img)
        label = Label(frame3, image=icon, bg="#fffbe6")
        label.image = icon
        label.pack(anchor='se', padx=10 )

    def FAT32(self, drive, frame):
        path="\\\.\\"
        for i in range (0, len(drive)-1):
            path += drive[i]

        label = Label(frame, text="BIOS Parameter Block information", font=("Georgia", 10), bg="#fffbe6")
        label.pack(anchor=N, padx=5, pady=5)

        data = BootSectorFAT32().readBootSector(path)
        pbr_fat = PbrFat(data)
        pbr_fat.readFat()
        txt = pbr_fat.showInfo()
        text = Text(frame, font=("Cambria", 12), bg="#fffbe6", spacing1=4, relief=FLAT)
        text.delete('1.0', "end")
        text.insert(END, txt)
        text.pack(side=LEFT, padx=10, pady=5)

        print("--------------")
        print("MBR info:  ")
        mbr = Mbr(data)
        mbr.showInforOfPart()

    def NTFS(self,drive, frame):
        path = "\\\.\\"
        for i in range(0, len(drive) - 1):
            path += drive[i]
        print(path)

        boots = BootSectorNTFS(None, 0, 512, path)
        txt = boots.show_infor()

        label = Label(frame, text="BIOS Parameter Block information", font=("Georgia", 10), bg="#fffbe6")
        label.pack(anchor=N, padx=5, pady=5)

        text = Text(frame, font=("Cambria", 12), bg="#fffbe6", spacing1=4, relief=FLAT)
        text.delete('1.0', "end")
        text.insert(END, txt)
        text.pack(side=LEFT, padx=10, pady=5)

        MFTable = MFT(filename=path, offset=boots.mft_offset)
        MFTable.preload_entries(1)

    def onClick(self,selected_drive, frame):
        selected = selected_drive.get()
        print(selected)
        list = frame.pack_slaves()
        for l in list:
            l.destroy()
        if (win32api.GetVolumeInformation(selected)[4]=='FAT32'):
            self.FAT32(selected, frame)
        if (win32api.GetVolumeInformation(selected_drive.get())[4]=='NTFS'):
            self.NTFS(selected, frame)

    def callback(self,eventObject):
         return eventObject.widget.get()
        # print(dir(eventObject))

    def Tab2(self,tab2):
        frame1 = Frame(tab2, bg="#fffbe6")
        frame1.pack()

        label1 = Label(frame1, text='Drive Selection', font=("Georgia", 10), bg="#fffbe6")
        label1.pack(side=LEFT, padx=10, pady=25)

        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        # for drive in drives:
        #     print(win32api.GetVolumeInformation(drive)[4])

        selected_drive = tkinter.StringVar()
        combobox = ttk.Combobox(frame1, textvariable=selected_drive)
        combobox['value'] = drives
        combobox['state'] = 'readonly'
        combobox.pack(side=LEFT, padx=10, pady=25)
        combobox.bind("<<ComboboxSelected>>", self.callback)
        # combobox.grid(column=3, row=5, padx=10, pady=25)

        frame2 = Frame(tab2, bg="#fffbe6")
        frame2.pack()
        button = tkinter.Button(frame1, text='Boot Sector', font=("Georgia", 10), bg="#7be37b", activeforeground='white',
                                activebackground='firebrick4', command=lambda: self.onClick(selected_drive, frame2))
        button.pack(side=LEFT, padx=10, pady=25)

        button1 = tkinter.Button(frame1, text='MBR / MFT', font=("Georgia", 10), bg="#7be37b", activeforeground='white',
                                activebackground='firebrick4', command=lambda: self.onClick(selected_drive, frame2))
        button1.pack(side=LEFT, padx=10, pady=25)
        # button.grid(column=4, row=5, padx=10, pady=25)

    def initUI(self):
        self.parent.title("Operating System")
        mygreen = "#d2ffd2"
        myred = "#dd0202"
        self.style = ttk.Style()
        self.style.configure("TNotebook", background="green")

        self.style.theme_create("yummy", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] }},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background": mygreen},
                "map": {"background": [("selected", "#fffbe6")],
                        "expand": [("selected", [1, 1, 1, 0])]}}})

        self.pack(fill=BOTH, expand=True)
        self.style.theme_use("yummy")
        tab_control = ttk.Notebook(self)

        tab1 = Frame(tab_control, background="#fffbe6")
        tab1.pack()
        tab2 = Frame(tab_control, background="#fffbe6")
        tab2.pack()

        tab_control.add(tab1, text="General Information")

        tab_control.add(tab2, text="Drive information")

        self.Tab1(tab1)
        self.Tab2(tab2)
        tab_control.pack(expand=1, fill='both')



root = Tk()
root.geometry("600x400+300+200")
app = App(root)
root.mainloop()