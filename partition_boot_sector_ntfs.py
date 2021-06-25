from mft_attribute_ntfs import *
from directory_ntfs import *
BPB_SIZE = 25
BPB_OFFSET = 0x0B
EXTENDED_BPB_SIZE = 48
HEADER_SIZE=56

READ_ONLY=0x0001
HIDDEN=0x0002
SYSTEM=0x0004
ARCHIVE=0x0020
COMPRESSED=0x0800
ENCRYPTED=0x4000
DIRECTORY=0x10000000

class BootSectorNTFS(RawStruct):
    def __init__(self, data=None, offset=None, length=None, filename=None):
        RawStruct.__init__(self, data=data, offset=offset, length=length, filename=filename)
        self.oem_id = self.get_string(3, 8).decode('utf-8')
        self.bpb = Bpb(self.get_chunk(BPB_OFFSET, BPB_SIZE + EXTENDED_BPB_SIZE), 0)
        self.data=self.data
        self.mft_offset=self.bpb.mft_offset()
        self.mft_mirror_offet=self.bpb.mft_mirror_offset()
        self.mft_record_size=self.bpb.mft_record_size()
    def data_boot(self):
        return self.data
    def show_infor(self):
        # print("OEM ID:", self.oem_id)
        return '\tOEM ID:  '+str(self.oem_id)+self.bpb.show_infor()
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
        self.volume_serial = self.get_ulonglong_b(61)
        self.checksum = self.get_uint(69)

    def show_infor(self):
        str1 = "\n\tBytes per sector:  "+str(self.bytes_per_sector)
        # print("Bytes per sector:", self.bytes_per_sector)

        str2 = '\n\tSectors Per Cluster:  '+str(self.sectors_per_cluster)
        # print("Sectors Per Cluster:", self.sectors_per_cluster)

        str3 = '\n\tReserved Sectors:  '+str(self.reserved_sectors)
        # print("Reserved Sectors:", self.reserved_sectors)

        str4 = '\n\tMedia Descriptor:  '+str(self.media_descriptor)
        # print("Media Descriptor:", self.media_descriptor)

        str5 = '\n\tSectors Per Track:  '+str(self.sectors_per_track)
        # print("Sectors Per Track:", self.sectors_per_track)

        str6 = '\n\tNumber Of Heads:  '+str(self.number_of_heads)
        # print("Number Of Heads:", self.number_of_heads)

        str7 = '\n\tHidden Sectors:  '+str(self.hidden_sectors)
        # print("Hidden Sectors:", self.hidden_sectors)

        str8 = '\n\tTotal Sectors:  '+str(self.total_sectors)
        # print("Total Sectors:", self.total_sectors)

        str9 = '\n\tLogical Cluster Number for the file $MFT:  '+str(self.mft_cluster)
        # print("Logical Cluster Number for the file $MFT:", self.mft_cluster)

        str10 = '\n\tLogical Cluster Number for the file $MFTMirr:  '+str(self.mft_mirror_cluster)
        # print("Logical Cluster Number for the file $MFTMirr:", self.mft_mirror_cluster)

        str11 = '\n\tClusters Per File Record Segment:  '+str(self.clusters_per_mft)
        # print("Clusters Per File Record Segment:", self.clusters_per_mft)

        str12 = '\n\tClusters Per Index Buffer:  '+str(self.clusters_per_index)
        # print("Clusters Per Index Buffer:", self.clusters_per_index)

        str13 = '\n\tVolume Serial Number:  '+str(hex(self.volume_serial))
        # print("Volume Serial Number:", self.volume_serial)

        str14 = '\n\tChecksum:  '+str(self.checksum)
        # print("Checksum:", self.checksum)
        return str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8 + str9 + str10 \
               + str11 + str12 + str13 + str14

    def mft_record_size(self):
        if (self.clusters_per_mft < 0):
            return 2 ** abs(self.clusters_per_mft)
        else:
            return self.clusters_per_mft * self.sectors_per_cluster * self.bytes_per_sector
    def mft_offset(self):
        return self.bytes_per_sector * (self.sectors_per_cluster * self.mft_cluster+78)

    def mft_mirror_offset(self):
        return self.bytes_per_sector * self.sectors_per_cluster * self.mft_mirror_cluster

class MFT(object):
    def __init__(self, entry_size=1024, offset=None, filename=None):
        self.offset=offset
        self.entry_size=entry_size
        self.filename=filename
        self.entries=[filename]
    def get_entry(self,entry_id):
        entry_offset = entry_id * self.entry_size
        self.entry = MFTEntry(filename=self.filename, offset=self.offset + entry_offset, length=self.entry_size,index=entry_id)
        if str(self.entry.header.file_signature)[2:6]!="FILE":
            return False
        self.entries.append(self.entry)
        return True

    def preload_entries(self):
        n=0
        while (self.get_entry(n)):
            n += 1

class MFTEntryHeader(RawStruct):
    def __init__(self,data):
        RawStruct.__init__(self,data)
        self.file_signature=self.get_string(0,4)
        self.update_seq_offset=self.get_ushort(4)
        self.update_seq_size=self.get_ushort(6)
        self.LogFile_seq_number=self.get_ulonglong(8)
        self.seq_number=self.get_ushort(16)
        self.hardlink_count=self.get_ushort(18)
        self.first_attr_offset=self.get_ushort(20)
        self.flags=self.get_ushort(22)
        self.used_size=self.get_uint(24)
        self.allocated_size=self.get_uint(28)
        self.file_ref_to_baseFile=self.get_ulonglong(32)
        self.next_attr=self.get_ushort(40)
        self.ID = self.get_uint(44)

class MFTEntry(RawStruct):
    def __init__(self, data=None, offset=None, length=None, filename=None, index=None):
        RawStruct.__init__(self, data=data, filename=filename, offset=offset, length=length)
        self.index=index
        self.attributes=[]
        self.fname_str=""
        self.check_data=0
        self.property=""
        self.real_size=None
        self.header=MFTEntryHeader(self.get_chunk(0, HEADER_SIZE))
        self.load_attributes()
        if self.check_data:
            self.property += "\nFilesize: " + str(self.real_size) + " (bytes)"
        self.property += "\n[Start Sector - End Sector]: " + str(int(offset/512)) + " - " + str(int(offset/512+self.header.allocated_size/512))
    def is_directory(self):
        return self.header.flags & 0x0002

    def is_file(self):
        return not self.is_directory

    def is_in_use(self):
        return self.header.flags & 0x0001

    def used_size(self):
        return self.header.used_size

    def getFileName(self):
        return self.fname_str

    def getID(self):
        return self.header.ID
    def getProperties(self):
        return self.property
    def get_attribute(self, offset):
        attr_type = self.get_uint(offset)
        if attr_type==0xFFFFFFFF:
            return None
        length = self.get_uint(offset + 0x04)
        data = self.get_chunk(offset, length)
        return MFTAttr.factory(attr_type, data)

    def lookup_attribute(self, attr_type_id):
        for attr in self.attributes:
            if attr.header.type == attr_type_id:
                return attr
        return None


    def load_attributes(self):
        free_space = self.header.used_size - HEADER_SIZE
        offset= self.header.first_attr_offset
        while free_space > 0:
            attr = self.get_attribute(offset)
            if (attr is not None):
                if attr.header.type == MFT_ATTR_FILENAME:
                    self.fname_str = attr.fname
                    self.parent_ID = attr.parent_ref
                    self.property += "\nFile name: " + attr.fname
                    self.property += "\nAttribute: "
                    if (attr.flags == READ_ONLY):
                        self.property += "*READ ONLY*"
                    if (attr.flags == HIDDEN):
                        self.property += "*HIDDEN*"
                    if (attr.flags == SYSTEM):
                        self.property += "*SYSTEM*"
                    if (attr.flags == ARCHIVE):
                        self.property += "*ARCHIVE*"
                    if (attr.flags == COMPRESSED):
                        self.property += "*COMPRESSED*"
                    if (attr.flags == ENCRYPTED):
                        self.property += "*ENCRYPTED*"
                    if (attr.flags == DIRECTORY):
                        self.property += "*DIRECTORY*"
                    self.property += "\nCreation time: " + attr.ctime_dt().strftime('%d.%m.%Y %H:%M:%S')
                    self.property += "\nModification time: " + attr.mtime_dt().strftime('%d.%m.%Y %H:%M:%S')
                    self.property += "\nLast Accessed time: " + attr.atime_dt().strftime('%d.%m.%Y %H:%M:%S')
                if attr.header.type == MFT_ATTR_DATA:
                    if self.check_data==0:
                        self.real_size = attr.header.real_size
                    self.check_data+=1
                self.attributes.append(attr)
                free_space = free_space - attr.header.length
                offset = offset + attr.header.length
            else:
                break