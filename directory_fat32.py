from file_entry_fat32 import *
import struct
import sys
class Directory(object):
    def __init__(self,file,fatTable,pbrFat,path,startSector = None):
        # pointer in file
        self.inputFile = file
        # pbr - fat
        self.pbrFat = pbrFat
        self.fatTable = fatTable

        # data area
        self.dataStartSector, dummy = self.pbrFat.getDataInfor()
        if startSector == None:
            self.dataOffset =  self.dataStartSector* self.pbrFat.getSectorSize()
        else:
            self.dataOffset = startSector*self.pbrFat.getSectorSize()

        #file entry
        self.entries = []
        self.path = path
        self.readAllEntry()
    # def isEmpty(self):
    #     return self.clusterList[0] == 0x00
    def readAllEntry(self):
        index = 0
        while(self.isDirectionEntry(index)):
            fileEntry = self.getEntry(index)
            #check error decode utf - 16:
            fileEntry = self.checkErrorDecodeUTF16AtLNFEntry(fileEntry)
            if not fileEntry.isDirectoryEntry():
                fileEntry.setPath(self.path + fileEntry.getFileName())
            else:
                fileEntry.setPath(self.path + fileEntry.getFileName()+"/")
            firstCluster = fileEntry.getFirstClusterNumber()

            if firstCluster > 2 and not fileEntry.isDeletedEntry():
                fileEntry.setOccupiedNumberCluster(self.getNumberOfClusterFileEntry(firstCluster))
                fileEntry.setFirstStartSector(self.getFirstStartSector(firstCluster))
                fileEntry.setLastSector(self.getLastSector(fileEntry))

            if not self.isSubDirectory(index):
                self.entries.append(fileEntry)
            index += fileEntry.getEntryCount()

    def getDirectoryAndFileEntries(self):
        entries = []
        for entry in self.entries:
            if (entry.getAttribute() == DIRECTORY or entry.getAttribute() == ARCHIVE) and not entry.isDeletedEntry():
                entries.append(entry)
        return entries
    def getDirectoryEntries(self):
        entries = []
        for entry in self.entries:
            if entry.getAttribute() == DIRECTORY and not entry.isDeletedEntry():
                entries.append(entry)
        return entries
    def getArchiveFileEntries(self):
        entries = []
        for entry in self.entries:
            if entry.getAttribute() == ARCHIVE and not entry.isDeletedEntry():
                entries.append(entry)
        return entries
    def getOffsetOfEntry(self, index):
        return self.dataOffset + index*32

    def getNumberOfClusterFileEntry(self,firstCluster):
        counter = 1
        while(self.fatTable.getValueOfCluster(firstCluster) < 0xFFFFFF8):
            counter+=1
            firstCluster = self.fatTable.getValueOfCluster(firstCluster)
            if firstCluster == 0x0FFFFFF7:
                raise Exception("Tried to read a cluster marked as bad, cluster: " + firstCluster)
        return counter
    def getFirstStartSector(self,firstCluster):
        return self.dataStartSector + (firstCluster-2)*self.pbrFat.getSectorsPerCluster()
    def getLastSector(self,fileEntry):
        firstCluster = fileEntry.getFirstClusterNumber()
        num = fileEntry.getOccupiedNumberCluster()
        return self.getFirstStartSector(firstCluster+num) - 1

    def isLongFileName(self,index):
        self.inputFile.seek(self.getOffsetOfEntry(index) + 0xB)
        return struct.unpack_from("<B", self.inputFile.read(1))[0] == LONG_FILE_NAME
    # first byte == 0
    def isDirectionEntry(self,index):
        self.inputFile.seek(self.getOffsetOfEntry(index))
        return struct.unpack_from("<B",self.inputFile.read(1))[0] != 0x0

    def isDeletedEntry(self, index):
        self.inputFile.seek(self.getOffsetOfEntry(index))
        return struct.unpack_from("<B", self.inputFile.read(1))[0] == 0xE5
    def isSubDirectory(self,index):
        self.inputFile.seek(self.getOffsetOfEntry(index))
        return struct.unpack_from("<B", self.inputFile.read(1))[0] == 0x2e or struct.unpack_from("<I", self.inputFile.read(4))[0] == 0x2e2e
    def checkErrorDecodeUTF16AtLNFEntry(self,fileEntry):
        fileName = fileEntry.getLongFileName()
        count = len(fileName)
        if (count > 0):
            if not fileName[-1].isalpha():
                fileEntry.setLongFileName(fileName[0:count-1])
        return fileEntry
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
                fileEntry.addToLongFileName(lfnEntry.getFileName())
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
            fileEntry.setId(index)
            fileEntry.setPath(self.path)
            return fileEntry

    def show(self):
        for entry in self.getDirectoryAndFileEntries():
            out = entry.stringOfOutput()
            print(out)