import datetime

#not little edian
def readByte(data,offset,length):
    return data[offset:offset+length]
def getDateTimeFromDosTime(dosDate, dosTime,dosTenthOfSecond):

    creationYear = readBitsFromByte(dosDate, 16, 7) + 1980
    creationMonth = readBitsFromByte(dosDate, 9, 4)
    creationDay = readBitsFromByte(dosDate, 5, 5)
    creationHour = readBitsFromByte(dosTime, 16, 5)
    creationMinute = readBitsFromByte(dosTime, 11, 6)
    creationSecond = int(readBitsFromByte(dosTime, 5, 5)*2 + dosTenthOfSecond / 100)
    creationMicroSecond = (dosTenthOfSecond % 100) * 10000
    return datetime.datetime(creationYear, creationMonth, creationDay, creationHour, creationMinute, creationSecond, creationMicroSecond)
def readBitsFromByte(value, startIndex, bitCount):
    return (value & (2**startIndex -1)) >> (startIndex - bitCount)

# name in long file name
def decodeUTF8(name):
    name = bytearray(name)
    stringName = ""
    for i in range(0, len(name) - 1, 2):
        if name[i] != 0xff and name[i] != 0x00:
            stringName += bytes(name[i]).decode('utf-8')
    return stringName

READ_ONLY = 0x01
HIDDEN_FILE = 0x02
SYSTEM_FILE = 0x04
VOLUME_ID = 0x08
DIRECTORY = 0x10
ARCHIVE = 0x20
LONG_FILE_NAME = 0x0F
class LongFileNameEntry():
    def __init__(self):
        self.order = None
        self.name1 = None
        self.attribute = None
        self.type = None # 0 -> this is subcomponent of a long name
        self.checkSum = None
        self.name2 = None
        self.fstClusLO = None
        self.name3 = None

    def readDirectionLongEntry(self,data):
        self.order = int.from_bytes(data[0x00:0x0+1],byteorder='little')
        self.name1 = data[0x01:0x01+10].decode('utf-16')
        # self.name1 = bin(int.from_bytes(data[0x01:0x01+10],byteorder='little'))
        self.attribute = int.from_bytes(data[0x0b:0x0b+1],byteorder='little')
        self.type = int.from_bytes(data[0x0c:0x0c+1],byteorder='little')
        self.checkSum = int.from_bytes(data[0x0d:0x0d+1],byteorder='little')
        self.name2 = data[0x0e:0x0e+12].decode('utf-16')
        # self.name2 = bin(int.from_bytes(data[0x0e:0x0e + 12], byteorder='little'))
        self.fstClusLO = int.from_bytes(data[0x1a:0x1a+2],byteorder='little')
        self.name3 = data[0x1c:0x1c+4].decode('utf-16').strip(b'\xff\xff'.decode('utf-16'))
        # self.name1 = bin(int.from_bytes(data[0x1c:0x1c + 4], byteorder='little'))

    def getFileName(self):
        fileName = (self.name1 + self.name2 + self.name3).strip(b'\xff\xff'.decode('utf-16'))
        return fileName
    def convertToByteArray(self):
        self.name1 = bytearray(self.name1)
        self.name2 = bytearray(self.name2)
        self.name1 = bytearray(self.name1)

    def getStringFromLongFilename(self):
        filename = ""
        firstChars = self.name1
        secondChars = self.name2
        thirdChars = self.name3
        for i in range(0, len(firstChars) - 1, 2):
            if firstChars[i] != 0xff and firstChars[i] != 0x00:
                filename += chr(int(firstChars[i]))
        for i in range(0, len(secondChars) - 1, 2):
            if secondChars[i] != 0xff and secondChars[i] != 0x00:
                filename += chr(int(secondChars[i]))
        for i in range(0, len(thirdChars) - 1, 2):
            if thirdChars[i] != 0xff and thirdChars[i] != 0x00:
                filename += chr(int(thirdChars[i]))
        return filename
    def getLongEntryType(self):
        return self.type
class ShortFileNameEntry():
    def __init__(self):
        self.longFileName = ""
        self.shortFileName = ""
        self.shortExtension = ""
        self.attribute = None
        self.entryCount = 1
        self.id = 0
        self.path = ""

        self.isDeleted = None
        self.firstStartSector = None
        self.lastSector = None
        self.numCluster = None
        # lenght of data = 32byte ~ 1 entry

    def readDirectoryShortEntry(self, data):
        if self.isDeleted:
            self.shortFileName = readByte(data, 0x01, 7).decode('utf-8')
        else:
            self.shortFileName = readByte(data, 0x00, 8).decode('utf-8')

        self.shortExtension = readByte(data, 0x08, 3).decode('utf-8')
        self.attribute = int.from_bytes(data[0x0b:0x0b + 1], byteorder='little')
        self.reserved = int.from_bytes(data[0x0c:0x0c + 1], byteorder='little')
        creationTenthOfSeconds = int.from_bytes(data[0x0d:0x0d + 1], byteorder='little')
        creationTime = int.from_bytes(data[0x0e:0x0e + 2], byteorder='little')
        creationDate = int.from_bytes(data[0x10:0x10 + 2], byteorder='little')
        accessedDate = int.from_bytes(data[0x12:0x12 + 2], byteorder='little')
        self.highWordStartCluster = int.from_bytes(data[0x14:0x14 + 2], byteorder='little')
        modificationTime = int.from_bytes(data[0x16:0x16 + 2], byteorder='little')
        modificationDate = int.from_bytes(data[0x18:0x18 + 2], byteorder='little')
        self.lowWordStartCluster = int.from_bytes(data[0x1a:0x1a + 2], byteorder='little')
        self.fileSize = int.from_bytes(data[0x1c:0x1c + 4], byteorder='little')

        # format
        self.firstClusterNumber = self.highWordStartCluster << 16 | self.lowWordStartCluster
        self.setCreationDateTime(getDateTimeFromDosTime(creationDate, creationTime, creationTenthOfSeconds))
        self.setAccessedDateTime(getDateTimeFromDosTime(accessedDate, 0, 0))
        self.setModifiedDateTime(getDateTimeFromDosTime(modificationDate, modificationTime, 0))

    def isDirectoryEntry(self):
        return self.attribute == DIRECTORY
    def isFileEntry(self):
        return self.attribute == ARCHIVE
    def isDeletedEntry(self):
        return self.isDeleted
    def addToLongFileName(self,fileName):
        self.longFileName += fileName
    def addEntryCount(self):
        self.entryCount+=1
    def setId(self,id):
        self.id = id
    def setPath(self,path):
        self.path = path

    def setLongFileName(self,longFileName):
        self.longFileName = longFileName
    def setShortFileName(self,shortFileName):
        self.shortFileName = shortFileName
    def setShortExtension(self,extension):
        self.shortExtension = extension
    def setAttribute(self,attribute):
        self.attribute = attribute
    def setDeletedEntry(self,deletedEntry):
        self.isDeleted = deletedEntry

    def setOccupiedNumberCluster(self,num):
        self.numCluster = num
    def setCreationDateTime(self,creationTime):
        self.creationTime = creationTime
    def setAccessedDateTime(self,accessedTime):
        self.accessedTime = accessedTime
    def setModifiedDateTime(self,modificationTime):
        self.modificationTime = modificationTime
    def setFileSize(self,fileSize):
        self.fileSize = fileSize
    def setFirstClusterStart(self,firstCluster):
        self.firstClusterNumber = firstCluster
    def setFirstStartSector(self,startSector):
        self.firstStartSector = startSector

    def setLastSector(self, lastSector):
        self.lastSector = lastSector

    def getLongFileName(self):
        return self.longFileName
    def getPath(self):
        return self.path
    def getAttribute(self):
        return self.attribute
    def getFirstStartSector(self):
        return self.firstStartSector
    def getLastSector(self):
        return self.lastSector
    def getOccupiedNumberCluster(self):
        return self.numCluster
    def getShortFileName(self):
        return self.shortFileName.strip()
    def getShortExtension(self):
        return self.shortExtension.strip()
    def getEntryCount(self):
        return self.entryCount
    def getFirstClusterNumber(self):
        return self.firstClusterNumber
    def getFullShortName(self):
        if len(self.getShortExtension()) >0:
            return self.getShortFileName() + '.' + self.getShortExtension()
        else:
            return self.getShortFileName()
    def getFileName(self):
        if len(self.longFileName) >0 :
            return self.longFileName
        else:
            return self.getFullShortName()

    def getFirstSectorStart(self, startSector):
        return self.firstStartSector
    def stringOfOutput(self):
        output = "-----------------"
        output += "\nPath: " + self.path
        output += "\nOffset Entry in Data Area: " + str(self.id)
        # output += "\nLong filename: " + self.longFileName
        output += "\nShort filename: " + self.getFileName()
        if (self.attribute == READ_ONLY):
            output += "\n*READ ONLY*"
        if (self.attribute == HIDDEN_FILE):
            output += "\n*HIDDEN*"
        if (self.attribute == SYSTEM_FILE):
            output += "\n*SYSTEM*"
        if (self.attribute == VOLUME_ID):
            output += "\n*VOLUME ID*"
        if (self.attribute == DIRECTORY):
            output += "\n*DIRECTORY*"
        if (self.attribute == ARCHIVE):
            output += "\n*ARCHIVE*"
        if (self.attribute == LONG_FILE_NAME):
            output += "\n*LONG_FILE_NAME*"
        output += "\nCreation time: " + self.creationTime.strftime('%d.%m.%Y %H:%M:%S:%f')
        output += "\nLast Accessed time: " + self.accessedTime.strftime('%d.%m.%Y')
        output += "\nModification time: " + self.modificationTime.strftime('%d.%m.%Y %H:%M:%S')
        output += "\nFirst cluster: " + str(self.firstClusterNumber)
        output+= "\nNum cluster:" + str(self.numCluster)
        output += "\nFilesize: " + str(self.fileSize)
        output += "\nEntry count: " + str(self.entryCount)
        output+= "\nStart Sector - End Sector: " + str(self.firstStartSector) + " - " + str(self.lastSector)
        return output
















