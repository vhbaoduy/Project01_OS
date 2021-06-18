import os
from directory_fat32 import *

def readDataFromDisk(disk,sectorNo,numSector):
    with open(disk, 'rb') as fp:
        fp.seek(sectorNo * 512)
        data = fp.read(numSector*512)
    return data

class BootSectorFAT32():
    def __init__(self):
        self.data = None
    def readBootSector(self,disk,sector_no = 0):
        with open(disk, 'rb') as fp:
            fp.seek(sector_no * 512)
            self.data = fp.read(512)
        return self.data

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
        print("OEM ID: ", self.BS_OEM_Name)
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
        print("Kích thước bảng FAT(SF):",self.BPB_FATsz32 )
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
    def getFatTableInfor(self):
        fatStartSector = self.BPB_RsvdSecCnt
        fatSectors = self.BPB_NumFATs* self.BPB_FATsz32
        #last sector =
        return fatStartSector,fatSectors
    def getRootDirInfor(self):
        fatStartSector,fatSectors = self.getFatTableInfor()

        rootDirStartSector = fatStartSector + fatSectors
        rootDirSectors = (32 * self.BPB_RootEntCnt + self.BPB_BytesPerSec - 1) / self.BPB_BytesPerSec
        return rootDirStartSector,int(rootDirSectors)

    def getSectorsPerCluster(self):
        return self.BPB_SecPerClus
    def getDataInfor(self):
        rootDirStart, rootDirSectors = self.getRootDirInfor()
        dataStartSector = rootDirStart + rootDirSectors
        dataSectors = self.BPB_TotalSec32 - dataStartSector
        return dataStartSector,dataSectors

    def getSectorSize(self):
        return self.BPB_BytesPerSec
    def getClusterSize(self):
        return self.BPB_BytesPerSec * self.BPB_SecPerClus

    ## ....
    def getEntriesPerCluster(self):
        return self.getClusterSize() / 32
    def getNumOfCluster(self):
        dummy, dataSectors = self.getDataInfor()
        return dataSectors/self.getSectorsPerCluster()
    def getReservedSector(self):
        return self.BPB_RsvdSecCnt

class FatTable(object):
    def __init__(self,disk,pbrFat):
        self.data = None
        self.disk = disk
        self.pbr_fat = pbrFat
        self.cluster = []
        self.fats = []
        self.readData()
        self.readFatTable()
    def readData(self):
        fatStart, fatSector = self.pbr_fat.getFatTableInfor()
        self.data = readDataFromDisk(self.disk,fatStart,fatSector)

    def readFatTable(self):
        for i in range(0,len(self.data),4):
            fat = int.from_bytes(self.data[i:i+4],byteorder='little')
            if fat == 0x0:
                break
            self.fats.append(fat)


        for i in range(len(self.fats)):
            print(hex(self.fats[i]), end = ' ')
        print(len(self.fats))
    # def getNextSector(self,index):
    def getElementOfFatTable(self,index):
        return self.fats[index]
    def getClusterList(self):
        return self.fats

    def getFirstSectorOfCluster(self,indexCluster):
        dataStartSector = self.pbr_fat.getDataInfor()[0]
        return dataStartSector + (indexCluster - 2) * self.pbr_fat.getSectorsPerCluster()

    def getPositionEntryFromCluster(self,indexCluster):
        sectorNum = self.pbr_fat.getReservedSector() + int(indexCluster*4 /self.pbr_fat.getSectorSize())
        entryOffset = (indexCluster * 4 ) % self.pbr_fat.getSectorSize()
        return sectorNum, entryOffset

    def getRootDirectory(self):
        return Directory(open(self.disk,'rb'),self.fats,self.pbr_fat,self.disk+"/")





if __name__ == "__main__":
    disk = r"\\.\H:"
    bootSectorData = BootSectorFAT32().readBootSector(disk)
    pbr_fat = PbrFat(bootSectorData)
    pbr_fat.readFat()
    # pbr_fat.showInfo()
    # print(pbr_fat.getDataInfor()[0])
    # data = readDataFromDisk(disk,pbr_fat.getDataInfor()[0],2)
    # for i in range(len(data)):
    #     print(hex(data[i]),end=' ')
    #     if (i+1) % 16 == 0:
    #         print()
    fat_table = FatTable(disk,pbr_fat)
    dir = fat_table.getRootDirectory()
    dir.show()









