import os
import ctypes, sys
class BootSector():
    def __init__(self):
        self.data = None
    def readBootSector(self,disk,sector_no = 0):
        with open(disk, 'rb') as fp:
            fp.seek(sector_no * 512)
            self.data = fp.read(512)
        return self.data
class PartitionEntry():
    def __init__(self,data):
        self.active = hex(int.from_bytes(data[0:1],byteorder = 'little'))
        self.startHead = int.from_bytes(data[1:2],byteorder='little')

        #decode
        temp = int.from_bytes(data[2:3],byteorder='little')
        self.startSector = temp & 0x3F
        self.startCylinder =   (((temp & 0XC0) >>6) <<8) + int.from_bytes(data[3:4],byteorder='little')

        self.type = hex(int.from_bytes(data[4:5],byteorder = 'little'))
        self.endHead = int.from_bytes(data[5:6],byteorder='little')

        #m để cho t pull code thằng Sĩ cái conflict quá trời nè
        temp = int.from_bytes(data[6:7], byteorder='little')
        self.endSector = temp & 0x3F
        self.endCylinder =  (((temp & 0XC0) >> 6) << 8) +int.from_bytes(data[7:8], byteorder='little')
        self.LBA = int.from_bytes(data[8:12], byteorder='little')
        self.numSec = int.from_bytes(data[12:16], byteorder='little')
    # def readInfoPartition(self,data):
    #     self.active = hex(int.from_bytes(data[0:1],byteorder = 'little'))
    #     self.startHead = int.from_bytes(data[1:2],byteorder='little')
    #
    #     #decode
    #     temp = int.from_bytes(data[2:3],byteorder='little')
    #     self.startSector = temp & 0x3F
    #     self.startCylinder = int.from_bytes(data[3:4],byteorder='little') + (((temp & 0XC0) >>6) <<8)
    #
    #     self.type = hex(int.from_bytes(data[4:5],byteorder = 'little'))
    #     self.endHead = int.from_bytes(data[5:6],byteorder='little')
    #
    #     #decode
    #     temp = int.from_bytes(data[6:7], byteorder='little')
    #     self.endSector = temp & 0x3F
    #     self.endCylinder = int.from_bytes(data[7:8], byteorder='little') + (((temp & 0XC0) >> 6) << 8)
    #     self.LBA = int.from_bytes(data[8:12], byteorder='little')
    #     self.numSec = int.from_bytes(data[12:16], byteorder='little')

    def showInfor(self):
        print("Active: ",end='')
        print("Bootable") if self.active == 0x80 else print("Non bootable")
        print("Start CHS: (%d,%d,%d)" % (self.startCylinder,self.startHead,self.startSector))
        print("End CHS: (%d,%d,%d)" % (self.endCylinder, self.endHead, self.endSector))
        print("Partition Type:", self.type)
        print("LBA of first absolute sector: ", self.LBA)
        print("Number of sectors in partition: ", self.numSec)
class PartitionTable:
    def __init__(self, data):
        self.Partitions =[PartitionEntry(data[16*i:16*(i+1)]) for i in range (0, 4)]
    def showInfor(self):
        for i in range(len(self.Partitions)):
            print("Partition ",i)
            self.Partitions[i].showInfor()
            print("--------------------------------")

class Mbr():
    def __init__(self, data):# WTF bên t hiện cái này khác. thì để t pull cái đã mà t đâu chỉnh mấy cái này
        self.BootCode = data[:440]
        self.DiskSig = int.from_bytes(data[440:444],byteorder='little')
        self.Unused = data[444:446]
        self.Partitions = PartitionTable(data[446:510])
        self.MBRSig = hex(int.from_bytes(data[510:512],byteorder='little'))

    def showInforOfPart(self):
        self.Partitions.showInfor()
        print(self.MBRSig)
class PbrFat():
    #BS -- Boot Sector
    #BPB -- BIOS Parameter Block
    def __init__(self,data):
        self.data = data
    def readFat(self):
        self.BS_jmpBoot = hex(int.from_bytes(self.data[0:3],byteorder = 'little'))
        self.BS_OEM_Name = self.data[3:11].decode('utf-8')
        self.BPB_BytesPerSec = int.from_bytes(self.data[11:13], byteorder='little')
        #Sc
        self.BPB_SecPerClus = int.from_bytes(self.data[13:14], byteorder='little')
        #Sb
        self.BPB_RsvdSecCnt = int.from_bytes(self.data[14:16], byteorder='little')
        #Nf
        self.BPB_NumFATs = int.from_bytes(self.data[16:17], byteorder='little')
        self.BPB_RootEntCnt = int.from_bytes(self.data[17:19], byteorder='little')
        self.BPB_ToatalSec16 = int.from_bytes(self.data[19:21], byteorder='little')
        self.BPB_Media = hex(int.from_bytes(self.data[21:22], byteorder='little'))
        self.BPB_FATSz16 = int.from_bytes(self.data[22:24], byteorder='little')
        self.BPB_SecPerTrack = int.from_bytes(self.data[24:26], byteorder='little')
        self.BPB_NumHeads = int.from_bytes(self.data[26:28], byteorder='little')
        self.BPB_HiddSec = int.from_bytes(self.data[28:32], byteorder='little')
        #Sv
        self.BPB_TotalSec32 = int.from_bytes(self.data[32:36], byteorder='little')

        ##Sf
        self.BPB_FATsz32 = int.from_bytes(self.data[36:40], byteorder='little')
        self.BPB_ExtFlags = int.from_bytes(self.data[40:42], byteorder='little')
        self.BPB_FSver = int.from_bytes(self.data[42:44], byteorder='little')
        self.BPB_RootStartClus = int.from_bytes(self.data[44:48], byteorder='little')
        self.BPB_FSInfo = int.from_bytes(self.data[48:50], byteorder='little')
        self.BPB_BackupBootSec = int.from_bytes(self.data[50:52], byteorder='little')
        self.BPB_Reserved = int.from_bytes(self.data[52:64], byteorder='little')
        self.BS_DriveNum = hex(int.from_bytes(self.data[64:65], byteorder='little'))
        self.BS_Revervedl = int.from_bytes(self.data[65:66], byteorder='little')
        self.BS_BootSig = hex(int.from_bytes(self.data[66:67], byteorder='little'))
        self.BS_VolumeID = hex(int.from_bytes(self.data[67:71], byteorder='little'))
        self.BS_VolumLabel = self.data[71:82].decode('utf-8')
        self.BS_FileSysType = self.data[82:90].decode('utf-8')

    def showInfo(self):
        print("Lệnh nhảy qua vùng thông số: ", self.BS_jmpBoot)
        print("OEM IL: ", self.BS_OEM_Name)
        print("Số bytes trên Sector: ", self.BPB_BytesPerSec)
        print("Số Sector trên Cluster (SC): ",self.BPB_SecPerClus)
        print("Số Sector thuộc vùng BootSector(SB): ", self.BPB_RsvdSecCnt)
        print("Số bảng FAT(NF): ",self.BPB_NumFATs)
        print("Số Entry của RDET: ", self.BPB_RootEntCnt)
        print("Số Sector của Vol: ", self.BPB_ToatalSec16)
        print("Loại thiết bị: ",self.BPB_Media)
        print("Số sector của bảng FAT: ",self.BPB_FATSz16)
        print("Số sector của track: ", self.BPB_SecPerTrack)
        print("Số lượng đầu đọc: ",self.BPB_NumHeads)
        print("Khoảng cách từ nơi mô tả vol đền đầu vol: ", self.BPB_HiddSec)
        print("Kích thước Volume(SV): ",self.BPB_TotalSec32)
        print("Kích thước bảng FAT():",self.BPB_FATsz32 )
        print("----: ",self.BPB_ExtFlags)
        print("Version: ", self.BPB_FSver)
        print("Cluter bắt đầu bảng RDET(!!!!): ", self.BPB_RootStartClus)
        print("Sector chứa thông tin phụ(!!!):", self.BPB_FSInfo)
        print("Sector chứa bản lưu của BS(!!!): ",self.BPB_BackupBootSec)
        print("Dành riêng cho phiên bản sau: ",self.BPB_Reserved)
        print("Kí hiệu vật lý: ", self.BS_DriveNum)
        print("Dành riêng ", self.BS_Revervedl)
        print("Kí hiệu nhận diện HĐH: ",self.BS_BootSig)
        print("SerialNumber của Volumne: ",self.BS_VolumeID)
        print("Volume Label: ", self.BS_VolumLabel)
        print("Loại FAT: ", self.BS_FileSysType)



# def is_admin():
#     try:
#             return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#             return False
#
# if is_admin():
#             boots = BootSector()
#             data = boots.readBootSector(r"\\.\E:")
#             print("PBR FAT info:  ")
#             pbr_fat = PbrFat(data)
#             pbr_fat.readFat()
#             pbr_fat.showInfo()
#             print("--------------")
#             print("MBR info:  ")
#             mbr = Mbr(data)
#             mbr.showInforOfPart()
#             # for v in data:
#             #     print(hex(v), end=' ')
# else:
#             # Re-run the program with admin rights
#             ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
# input()


boots = BootSector()
data = boots.readBootSector(r"\\.\E:")
print("PBR FAT info:  ")
pbr_fat = PbrFat(data)
pbr_fat.readFat()
pbr_fat.showInfo()
print("--------------")
print("MBR info:  ")
mbr = Mbr(data)
mbr.showInforOfPart()


# if __name__ == "__main__":
#     # test pbr- fat
#     boots = BootSector()
#     data = boots.readBootSector(r"\\.\E:")
#     print("PBR FAT info:  ")
#     pbr_fat = PbrFat(data)
#     pbr_fat.readFat()
#     pbr_fat.showInfo()
#     print("--------------")
#     print("MBR info:  ")
#     mbr = Mbr(data)
#     mbr.showInforOfPart()






