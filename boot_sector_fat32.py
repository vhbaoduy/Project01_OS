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
        str1 = '\tJump instrution  '+self.BS_jmpBoot
        # print("Lệnh nhảy qua vùng thông số: ", self.BS_jmpBoot)

        str2 = '\n\tOEM ID:  ' + self.BS_OEM_Name
        # print("OEM ID: ", self.BS_OEM_Name)

        str3 = '\n\tBytes per Sector:  '+str(self.BPB_BytesPerSec)
        # print("Số bytes trên Sector: ", self.BPB_BytesPerSec)

        str4 = '\n\tSectors Per Cluster (Sc):  '+str(self.BPB_SecPerClus)
        # print("Số Sector trên Cluster (SC): ",self.BPB_SecPerClus)

        str5 = '\n\tReserved Sectors:  '+str(self.BPB_RsvdSecCnt)
        # print("Số Sector thuộc vùng BootSector(SB): ", self.BPB_RsvdSecCnt)

        str6 = '\n\tNumber of FATs (Nf):  '+str(self.BPB_NumFATs)
        # print("Số bảng FAT(NF): ",self.BPB_NumFATs)

        str7 = '\n\tRoot entries:  '+str(self.BPB_RootEntCnt)
        # print("Số Entry của RDET: ", self.BPB_RootEntCnt)

        # str8 = '\nSmall sectors: '+str(self.BPB_ToatalSec16)
        # print("Số Sector của Vol: ", self.BPB_ToatalSec16)

        str8 = '\n\tMedia type:  '+str(self.BPB_Media)
        # print("Loại thiết bị: ",self.BPB_Media)

        # str10 = '\nSectors per FAT: '+str(self.BPB_FATSz16)
        # print("Số sector của bảng FAT: ",self.BPB_FATSz16)

        str9 = '\n\tSectors per Track:  '+str(self.BPB_SecPerTrack)
        # print("Số sector của track: ", self.BPB_SecPerTrack)

        str10 = '\n\tNumbers of Heads:  '+str(self.BPB_NumHeads)
        # print("Số lượng đầu đọc: ",self.BPB_NumHeads)

        str11 = '\n\tHidden Sectors:  '+str(self.BPB_HiddSec)
        # print("Khoảng cách từ nơi mô tả vol đền đầu vol: ", self.BPB_HiddSec)

        str12 = '\n\tSize of the partition, in sectors:  '+str(self.BPB_TotalSec32)
        # print("Kích thước Volume(SV): ",self.BPB_TotalSec32)

        str13 = '\n\tSectors per FAT:  '+str(self.BPB_FATsz32)
        # print("Kích thước bảng FAT(SF):",self.BPB_FATsz32 )

        str14 = '\n\tPhysical Disk Number:  '+str(self.BS_DriveNum)
        # print("Kí hiệu vật lý: ", self.BS_DriveNum)

        str15 = '\n\tReserve (for Windows NT):  '+str(self.BS_Revervedl)
        # print("Dành riêng ", self.BS_Revervedl)

        str16 = '\n\tBoot Signature:  '+str(self.BS_BootSig)
        # print("Kí hiệu nhận diện HĐH: ",self.BS_BootSig)

        str17 = '\n\tVolume Serial Number:  '+str(self.BS_VolumeID)
        # print("SerialNumber của Volumne: ",self.BS_VolumeID)

        str18 = '\n\tVolume Label:  '+str(self.BS_VolumLabel)
        # print("Volume Label: ", self.BS_VolumLabel)

        str19 = '\n\tSystem ID: '+str(self.BS_FileSysType)
        # print("Loại FAT: ", self.BS_FileSysType)

        str20 = '\n\tFlags describing the drive:  '+str(self.BPB_ExtFlags)
        # print("----: ",self.BPB_ExtFlags)

        str21 = '\n\t\t+ Version of FAT32:  '+str(self.BPB_FSver)
        # print("Version: ", self.BPB_FSver)

        str22 = "\n\t\t+ The first cluster in FAT32 RDET:  "+str(self.BPB_RootStartClus)
        # print("Cluter bắt đầu bảng RDET(!!!!): ", self.BPB_RootStartClus)

        str23 = '\n\t\t+ The sector number of the file system information sector:  '+str(self.BPB_FSInfo)
        # print("Sector chứa thông tin phụ(!!!):", self.BPB_FSInfo)

        str24 = '\n\t\t+ The sector number of the backup boot sector:  '+str(self.BPB_BackupBootSec)
        # print("Sector chứa bản lưu của BS(!!!): ",self.BPB_BackupBootSec)

        str25 = '\n\t\t+ Reversed number:  '+str(self.BPB_Reserved)
        # print("Dành riêng cho phiên bản sau: ",self.BPB_Reserved)

        return str1+str2+str3+str4+str5+str6+str7+str8+str9+str10 \
            +str11+str12+str13+str14+str15+str16+str17+str18+str19+str20 \
            +str21+str22+str23+str24+str25
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

class FatTable():
    def __init__(self,disk,pbrFat):
        self.data = None
        self.disk = disk
        self.pbr_fat = pbrFat
        self.cluster = []
        self.fats = []
        self.readData()
        # self.readFatTable()

        self.directoryTree = [self.getRootDirectory()]
    def readData(self):
        fatStart, fatSector = self.pbr_fat.getFatTableInfor()
        self.data = readDataFromDisk(self.disk,fatStart,fatSector)
    # def readFatTable(self):
    #     for i in range(0,len(self.data),4):
    #         fat = int.from_bytes(self.data[i:i+4],byteorder='little')
    #         self.fats.append(fat)
    def getValueOfCluster(self,index):
        return int.from_bytes(self.data[index:index+4],byteorder='little')
    def getClusterList(self):
        return self.fats
    def getRootDirectory(self):
        return Directory(open(self.disk,'rb'),self,self.pbr_fat,self.disk+"/",0)
    def getDirectory(self,rootDirectory):
        dirEntries = rootDirectory.getDirectoryEntries()
        if len(dirEntries) > 0:
            for entry in dirEntries:
                dir = Directory(open(self.disk,'rb'),self,self.pbr_fat,entry.getPath()+"/",rootDirectory.getDepth()+1,entry.getFirstStartSector())
                self.directoryTree.append(dir)
                self.getDirectory(dir)

    def getNumberOfFoldersAndFiles(self):
        folder,file = 0,0
        for v in self.directoryTree:
            folder += len(v.getDirectoryEntries())
            file += len(v.getArchiveFileEntries())
        return folder,file
    def getDir(self):
        return self.directoryTree
    def show(self):
        for v in self.directoryTree:
            v.show(v.getDepth())



if __name__ == "__main__":
    disk = r"\\.\G:"

    bootSectorData = BootSectorFAT32().readBootSector(disk)
    pbr_fat = PbrFat(bootSectorData)
    pbr_fat.readFat()
    fat_table = FatTable(disk,pbr_fat)
    dir = fat_table.getRootDirectory()
    fat_table.getDirectory(dir)
    root= Root(fat_table.getDir())
    entries = root.getNodeList()
    for v in entries:
        if not v.isEmpty():
            print(v.getFileName())











