import struct
class RawStruct(object):
    def __init__(self, data=None, offset=None, length=None, filename=None):
        if data is not None:
            self.data = data[offset:offset+length]
        elif filename is not None:
            with open(filename, 'rb') as fp:
                fp.seek(offset)
                self.data = fp.read(length)
    def data(self):
        return self.data
    def size(self):
        return len(self.data)
    def get_chunk(self, offset, length):
        return self.data[offset:offset+length]
    def get_uchar(self, offset):
        return struct.unpack("B", self.data[offset:offset + 1])[0]
    def get_char(self, offset):
        return struct.unpack("b", self.data[offset:offset + 1])[0]
    def get_ushort(self, offset):
        return struct.unpack("<H", self.data[offset:offset + 2])[0]
    def get_uint(self, offset):
        return struct.unpack("<I", self.data[offset:offset + 4])[0]
    def get_ulonglong(self, offset):
        return struct.unpack("<Q", self.data[offset:offset + 8])[0]
    def get_string(self, offset, length):
        return struct.unpack(str(length) + "s", self.data[offset:offset + length])[0]


class PartitionEntry():
    def __init__(self,data):
        self.active = int.from_bytes(data[0:1],byteorder = 'little')
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

    def getStatus(self):
        if self.active == 0x00:
            return "Non bootable"
        else:
            if self.active == 0x80:
                return 'Bootable'
            else:
                return 'Invalid bootable byte'
    def showInfor(self):
        print("Active: ",self.getStatus())
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

    def __init__(self, data):
        self.BootCode = data[:440]
        self.DiskSig = int.from_bytes(data[440:444],byteorder='little')
        self.Unused = data[444:446]
        self.Partitions = PartitionTable(data[446:510])
        self.MBRSig = int.from_bytes(data[510:512],byteorder='little')


    def showInforOfPart(self):
        print("Disk signature: ", self.DiskSig)
        self.Partitions.showInfor()
        print(self.checkMbrSig())
    def checkMbrSig(self):
        if (self.MBRSig == 0xAA55):
            return "Correct MBR signature"
        else:
            return "Incorrect MBR signature"