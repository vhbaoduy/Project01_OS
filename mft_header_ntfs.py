from mbr import *

class MFTAttrHeader(RawStruct):
    def __init__(self, data):
        RawStruct.__init__(self, data)
        self.type = self.get_uint(0)
        self.length = self.get_uint(0x4)
        self.non_resident_flag = self.get_uchar(0x08)   # 0 - resident, 1 - not
        self.length_of_name = self.get_uchar(0x09)      # Used only for ADS
        self.offset_to_name = self.get_ushort(0x0A)     # Used only for ADS

        # (Compressed, Encrypted, Sparse)
        self.flags = self.get_ushort(0x0C)
        self.identifier = self.get_ushort(0x0E)

        if (self.non_resident_flag):
            # Attribute is Non-Resident
            self.lowest_vcn = self.get_ulonglong(0x10)
            self.highest_vcn = self.get_ulonglong(0x18)
            self.data_run_offset = self.get_ushort(0x20)
            self.comp_unit_size = self.get_ushort(0x22)
            # 4 byte 0x00 padding @ 0x24
            self.alloc_size = self.get_ulonglong(0x28)
            self.real_size = self.get_ulonglong(0x30)
            self.data_size = self.get_ulonglong(0x38)

            if (self.length_of_name > 0):
                self.attr_name = self.get_chunk(
                    0x40, 2 * self.length_of_name).decode('utf-16')
                # print self.attr_name.decode('utf-16')
        else:
            # Attribute is Resident
            self.attrngth = self.get_uint(0x10)
            self.attr_offset = self.get_ushort(0x14)
            self.indexed = self.get_uchar(0x16)
            if (self.length_of_name > 0):
                self.attr_name = self.get_chunk(
                    0x18, 2 * self.length_of_name).decode('utf-16')
                # print self.attr_name.decode('utf-16')
            # The rest byte is 0x00 padding
            # print "Attr Offset: 0x%x" % (self.attr_offset)
