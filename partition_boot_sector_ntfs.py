import struct
BPB_SIZE = 25
BPB_OFFSET = 0x0B
EXTENDED_BPB_SIZE = 48
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

class BootSector(RawStruct):
    def __init__(self, data=None, offset=None, length=None, filename=None):
        RawStruct.__init__(self, data=data, offset=offset, length=length, filename=filename)
        self.oem_id = self.get_string(3, 8)
        self.bpb = Bpb(self.get_chunk(BPB_OFFSET, BPB_SIZE + EXTENDED_BPB_SIZE), 0)
        self.data=self.data
    def data_boot(self):
        return self.data
    def show_infor(self):
        print("OEM ID:", self.oem_id)
        self.bpb.show_infor()
class Bpb(RawStruct):
    def __init__(self, data=None, offset=None, filename=None):
        RawStruct.__init__(self, data=data, offset=offset, length=BPB_SIZE + EXTENDED_BPB_SIZE, filename=filename)

        self.bytes_per_sector = self.get_ushort(0)
        self.sectors_per_cluster = self.get_uchar(2)
        self.reserved_sectors = self.get_ushort(3)
        self.media_descriptor = self.get_uchar(10)
        self.sectors_per_track = self.get_ushort(13)
        self.number_of_heads = self.get_ushort(15)
        self.hidden_sectors = self.get_uint(17)

        self.total_sectors = self.get_ulonglong(29)
        self.mft_cluster = self.get_ulonglong(37)
        self.mft_mirror_cluster = self.get_ulonglong(45)
        self.clusters_per_mft = self.get_uint(53)
        self.clusters_per_index = self.get_uchar(57)
        self.volume_serial = self.get_ulonglong(61)
        self.checksum = self.get_uint(69)

    def show_infor(self):
        print("Bytes per sector:", self.bytes_per_sector)
        print("Sectors Per Cluster:", self.sectors_per_cluster)
        print("Reserved Sectors:", self.reserved_sectors)
        print("Media Descriptor:", self.media_descriptor)
        print("Sectors Per Track:", self.sectors_per_track)
        print("Number Of Heads:", self.number_of_heads)
        print("Hidden Sectors:", self.hidden_sectors)
        print("Total Sectors:", self.total_sectors)
        print("Logical Cluster Number for the file $MFT:", self.mft_cluster)
        print("Logical Cluster Number for the file $MFTMirr:", self.mft_mirror_cluster)
        print("Clusters Per File Record Segment:", self.clusters_per_mft)
        print("Clusters Per Index Buffer:", self.clusters_per_index)
        print("Volume Serial Number:", self.volume_serial)
        print("Checksum:", self.checksum)

# class MFT(object):
#     def __init__(self, entry_size=1024, offset=None, filename=None):
#         self.offset=offset
#         self.entry_size=entry_size
#         self.filename=filename
#         self.entries={}
#     def get_entry(self,entry_id):
#         if entry_id in self.entries:
#             return self.entries[entry_id]
#         else:
#             entry_offset=entry_id*self.entry_size
#             # entry=MFTEntry(self.filename,self.offset+entry_offset,self.entry_size,entry_size)
#             # self.entries[entry_id]=entry
#             # return entry
#
#     def preload_entries(self, count):
#         for n in range(0, count):
#             self.get_entry(n)
#     def __str__(self):
#         result = ""
#         for entry_id in self.entries:
#             result += str(self.entries[entry_id]) + "\n\n"
#         return result
def NTFS():
    boots = BootSector(None, 0, 512, r"\\.\E:")
    boots.show_infor()
    print("--------------")
    print("MBR info:  ")
    mbr = Mbr(boots.data_boot())
    mbr.showInforOfPart()

if __name__ == "__main__":
    boots = BootSector(None, 0, 512, r"\\.\E:")
    boots.show_infor()
    print("--------------")
    print("MBR info:  ")
    mbr = Mbr(boots.data_boot())
    mbr.showInforOfPart()

