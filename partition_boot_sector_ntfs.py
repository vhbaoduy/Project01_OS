from mbr import *
from mft_attribute_ntfs import *
BPB_SIZE = 25
BPB_OFFSET = 0x0B
EXTENDED_BPB_SIZE = 48
HEADER_SIZE=42
class BootSectorNTFS(RawStruct):
    def __init__(self, data=None, offset=None, length=None, filename=None):
        RawStruct.__init__(self, data=data, offset=offset, length=length, filename=filename)
        self.oem_id = self.get_string(3, 8)
        self.bpb = Bpb(self.get_chunk(BPB_OFFSET, BPB_SIZE + EXTENDED_BPB_SIZE), 0)
        self.data=self.data
        self.mft_offset=self.bpb.mft_offset()
        self.mft_mirror_offet=self.bpb.mft_mirror_offset()
        self.mft_record_size=self.bpb.mft_record_size()
        # print(self.mft_record_size)
        # print(self.mft_offset)
    def data_boot(self):
        return self.data
    def show_infor(self):
        print("OEM ID:", self.oem_id)
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
        self.volume_serial = self.get_ulonglong(61)
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

        str13 = '\n\tVolume Serial Number:  '+str(self.volume_serial)
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
        return self.bytes_per_sector * self.sectors_per_cluster * self.mft_cluster

    def mft_mirror_offset(self):
        return self.bytes_per_sector * self.sectors_per_cluster * self.mft_mirror_cluster

class MFT(object):
    def __init__(self, entry_size=1024, offset=None, filename=None):
        self.offset=offset
        self.entry_size=entry_size
        self.filename=filename
        self.entries={}
    def get_entry(self,entry_id):
        if entry_id in self.entries:
            return self.entries[entry_id]
        else:
            entry_offset = entry_id * self.entry_size
            # load entry
            entry = MFTEntry(filename=self.filename,offset=self.offset + entry_offset,length=self.entry_size,index=entry_id)
            # cache entry
            self.entries[entry_id] = entry
            return entry

    def preload_entries(self, count):
        for n in range(0, count):
            self.get_entry(n)
    def __str__(self):
        result = ""
        for entry_id in self.entries:
            result += str(self.entries[entry_id]) + "\n\n"
        return result

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

class MFTEntry(RawStruct):
    def __init__(self, data=None, offset=None, length=None, filename=None, index=None):
        RawStruct.__init__(self, data=data, filename=filename, offset=offset, length=length)
        self.index=index
        self.attributes=[]
        self.fname_str=""
        self.header=MFTEntryHeader(self.get_chunk(0, HEADER_SIZE))
        self.name_str=self.get_entry_name(self.index)
        self.load_attributes()


    def get_entry_name(self, index):
        names = {
            0: "Master File Table",
            1: "Master File Table Mirror",
            2: "Log File",
            3: "Volume File",
            4: "Attribute Definition Table",
            5: "Root Directory",
            6: "Volume Bitmap",
            7: "Boot Sector",
            8: "Bad Cluster List",
            9: "Security",
            10: "Upcase Table",
            11: "Extend Table",
        }
        return names.get(index, "(unknown/unnamed)")

    def is_directory(self):
        return self.header.flags & 0x0002

    def is_file(self):
        return not self.is_directory

    def is_in_use(self):
        return self.header.flags & 0x0001

    def used_size(self):
        return self.header.used_size

    def get_attribute(self, offset):
        attr_type = self.get_uint(offset)
        length = self.get_uint(offset + 0x04)
        data = self.get_chunk(offset, length)
        return MFTAttr.factory(attr_type, data)

    def lookup_attribute(self, attr_type_id):
        for attr in self.attributes:
            if attr.header.type == attr_type_id:
                return attr
        return None

    def load_attributes(self):
        free_space = self.size() - HEADER_SIZE
        offset= self.header.first_attr_offset
        while free_space > 0:
            attr = self.get_attribute(offset)

            if (attr is not None):
                if attr.header.type == MFT_ATTR_FILENAME:
                    self.fname_str = attr.fname

                self.attributes.append(attr)
                free_space = free_space - attr.header.length
                offset = offset + attr.header.length
            else:
                break

    def __str__(self):
        result = ("File: %d\n%s (%s)" % (self.index, self.name_str, self.fname_str))

        for attr in self.attributes:
            result = result + "\n\t" + str(attr)
        return result


def NTFS():
    boots = BootSectorNTFS(None, 0, 512, r"\\.\E:")
    boots.show_infor()
    print("--------------")
    print("MBR info:  ")
    mbr = Mbr(boots.data_boot())
    mbr.showInforOfPart()

if __name__ == "__main__":
    boots = BootSectorNTFS(None, 0, 512, r"\\.\E:")
    #boots.show_infor()

    MFTable=MFT(filename=r"\\.\E:",offset=boots.mft_offset)
    MFTable.preload_entries(1)

    # print("--------------")
    # print("MBR info:  ")
    # mbr = Mbr(boots.data_boot())
    # mbr.showInforOfPart()

