import boot_sector_fat32 as bsfat32
from partition_boot_sector_ntfs import RawStruct
def readByte(data,offset,length):
    return data[offset:offset+length]

READ_ONLY = 0x01
HIDDEN_FILE = 0x02
SYSTEM_FILE = 0x04
VOLUME_ID = 0x08
DIRECTION = 0x10
ARCHIVE = 0x20
LONG_FILE_NAME = 0x0F

class FileEntry(object):
    def __init__(self):
        self.longFileName = ""
        self.shortFileName = ""
        self.shortExtension = ""
        self.attribute = None
        self.entryCount = 1

    def addToLongFileName(self,fileName):
        self.longFileName +=fileName

    def addEntryCount(self):
        self.entryCount+=1
    def setShortFileName(self,shortFileName):
        self.shortFileName = shortFileName

class RootDirector():
    def __init__(self,file,clusterList,pbrFat):
        self.pbrFat = pbrFat
        self.clusterList = clusterList
        self.dataOffset, dummy = pbrFat.getDataInfor()
        self.entries = []


    def isEmpty(self):
        return self.clusterList[0] == 0

    def readAllEntry(self):
        return None

    # def getAttributeFile(self,indexOfEntry):











