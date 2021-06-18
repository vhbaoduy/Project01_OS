
from file_entry_fat32 import *
import struct
import sys
class Directory(object):
    def __init__(self,file,clusterList,pbrFat,path):
        # pointer in file
        self.inputFile = file
        # pbr - fat
        self.pbrFat = pbrFat
        self.clusterList = clusterList

        # data area
        self.dataStartSector, dummy = self.pbrFat.getDataInfor()
        self.dataOffset =  self.dataStartSector* self.pbrFat.getSectorSize()

        #file entry
        self.entries = []
        self.path = path
        self.readAllEntry()


    def isEmpty(self):
        return self.clusterList[0] == 0x00

    def readAllEntry(self):
        index = 0
        while(self.isDirectionEntry(index) and index* 32 < len(self.clusterList) * self.pbrFat.getClusterSize()):
            fileEntry = self.getEntry(index)
            self.entries.append(fileEntry)
            index += fileEntry.getEntryCount()


    def getOffsetOfEntry(self, index):
        # clusterIndex = int(index / self.pbrFat.getEntriesPerCluster())
        # clusterOffset = self.clusterList[clusterIndex]* self.pbrFat.getClusterSize()
        #indexOffset = (index % self.pbrFat.getEntriesPerCluster()) * 32
        # return int(round(self.dataOffset + clusterOffset + indexOffset))
        return self.dataOffset + index*32

    def getAttributeFile(self,index):
        self.inputFile.seek(self.getOffsetOfEntry(index) + 0xB)
        return struct.unpack_from("<B",self.inputFile.read(1))[0]

    def isLongFileName(self,index):
        self.inputFile.seek(self.getOffsetOfEntry(index) + 0xB)
        return struct.unpack_from("<B", self.inputFile.read(1))[0] == LONG_FILE_NAME
        # return self.getAttributeFile(index) == LONG_FILE_NAME
    # first byte == 0
    def isDirectionEntry(self,index):

        self.inputFile.seek(self.getOffsetOfEntry(index))
        return struct.unpack_from("<B",self.inputFile.read(1))[0] != 0x0

    def isDeletedEntry(self, index):
        self.inputFile.seek(self.getOffsetOfEntry(index))
        return struct.unpack_from("<B", self.inputFile.read(1))[0] == 0xE5

    def getEntry(self, index):
        if self.isLongFileName(index):
            offset = self.getOffsetOfEntry(index)
            self.inputFile.seek(offset)
            data = self.inputFile.read(32)

            lfnEntry = LongFileNameEntry()
            lfnEntry.readDirectionLongEntry(data)

            if lfnEntry.getLongEntryType() == 0:
                if sys.version_info.major < 3:
                    lfnEntry.convertToByteArray()

                fileEntry = self.getEntry(index + 1)
                fileEntry.addToLongFileName(lfnEntry.getStringFromLongFilename())
                fileEntry.addEntryCount()
            return fileEntry
        else:
            fileEntry = ShortFileNameEntry()
            self.inputFile.seek(self.getOffsetOfEntry(index))
            data = self.inputFile.read(32)
            fileEntry.setDeletedEntry(self.isDeletedEntry(index))
            fileEntry.readDirectoryShortEntry(data)
            if self.isDeletedEntry(index):
                fileEntry.setShortFileName("[?]" + fileEntry.getShortFileName()[1:])
            fileEntry.setId(self.getOffsetOfEntry(index))
            fileEntry.setPath(self.path)
            return fileEntry

    def show(self):
        for entry in self.entries:
            out = entry.stringOfOutput()
            print(out)