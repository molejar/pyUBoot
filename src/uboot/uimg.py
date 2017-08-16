# Copyright (c) 2017 Martin Olejar, martin.olejar@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time
import zlib
from struct import pack, unpack_from, calcsize
from enum import Enum, unique


# ----------------------------------------------------------------------------------------------------------------------
# Helper methods
# ----------------------------------------------------------------------------------------------------------------------
def CRC32(data):
    """ Help function for 32bit CRC calculation
    :param data: Tha data blob as byte array
    :return: CRC Value
    """
    return zlib.crc32(data) & 0xFFFFFFFF
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Customized Enum Class
# ----------------------------------------------------------------------------------------------------------------------
class IntEnum(int, Enum):
    @classmethod
    def check_value(cls, value):
        for n, v in cls.__members__.items():
            if int(value) == int(v):
                return True
        return False

    @classmethod
    def str_to_value(cls, name):
        for n, v in cls.__members__.items():
            if name.upper() == n:
                return int(v)
        raise ValueError("Unsupported name: %s" % name)

    @classmethod
    def value_to_str(cls, value):
        for n, v in cls.__members__.items():
            if int(value) == int(v):
                return n
        return "0x{0:08X}".format(value)

    @classmethod
    def get_names(cls, lower=False):
        if lower:
            return [x.lower() for x in cls.__members__.keys()]
        else:
            return cls.__members__.keys()

    @classmethod
    def get_items(cls):
        items = {}
        for n, v in cls.__members__.items():
            items[n] = int(v)
        return items
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# UBoot Header Class and Enums
# ----------------------------------------------------------------------------------------------------------------------
@unique
class IMGType(IntEnum):
    """ Header: Options of UBoot Image Types """
    STD = 1         # Standalone Image
    KERNEL = 2      # Kernel Image
    RAMDISK = 3     # RamDisk Image
    MULTI = 4       # Multi-File Image
    FIRMWARE = 5    # Firmware Image
    SCRIPT = 6      # U-Boot Script Image
    FILESYSTEM = 7  # Filesystem Image
    FLATDT = 8      # Flat Device Tree Image
    KWB = 9         # -
    IMX = 10        # i.MX Image
    UBL = 11        # -
    OMAP = 12       # TX Omap Image
    AIS = 13        # -
    KNOLOAD = 14    # Kernel No Load Image
    PBL = 15        # -
    MXS = 16        # -
    GP = 17         # -
    ATMEL = 18      # -
    SOCFPGA = 19    # -
    X86SETUP = 20   # -
    LPC32XX = 21    # -
    LOADABLE = 22   # -
    RK = 23         # -
    RKSD = 24       # -
    RKSPI = 25      # -
    ZYNQ = 26       # -


@unique
class OSType(IntEnum):
    """ Header: Options of Operating System """
    OPENBSD = 1
    NETBSD = 2
    FREEBSD = 3
    BSD4 = 4
    LINUX = 5
    SVR4 = 6
    ESIX = 7
    SOLARIS = 8
    IRIX = 9
    SCO = 10
    DELL = 11
    NCR = 12
    LYNXOS = 13
    VXWORKS = 14
    PSOS = 15
    QNX = 16
    UBOOT = 17
    RTEMS = 18
    UNITY = 19
    INTEGRITY = 20
    OSE = 21
    PLAN9 = 22
    OPENRTOS = 23


@unique
class ARCHType(IntEnum):
    """ Header: Options of CPU Architecture """
    ALPHA = 1
    ARM = 2
    X86 = 3
    IA64 = 4
    MIPS = 5
    MIPS64 = 6
    PPC = 7
    S390 = 8
    SH = 9
    SPARC = 10
    SPARC64 = 11
    M68K = 12
    MICROBLAZE = 13
    NIOS2 = 14
    BLACKFIN = 15
    AVR32 = 16
    ST200 = 17
    NDS32 = 18
    OR1K = 19


@unique
class COMPRESSType(IntEnum):
    """ Header: Options of Data Compression """
    NONE = 0
    GZIP = 1
    BZIP2 = 2
    LZMA = 3
    LZO = 4
    LZ4 = 5


class Header(object):
    FORMAT = '!7L4B32s'        ### (Big-endian, 7 ULONGS, 4 UCHARs, 32-byte string)
    SIZE   = calcsize(FORMAT)  ### Should be 64-bytes

    OS_NAMES = (
        "NA", "OpenBSD", "NetBSD", "FreeBSD", "4-BSD", "Linux", "SVR4", "ESIX", "Solaris", "IRIX", "SCO", "Dell", "NCR",
        "LynxOS", "VXWorks", "PSOS", "QNX", "UBoot", "RTEMS", "Unity", "Integrity", "OSE", "PLAN9", "OpenRTOS"
    )

    ARCH_NAMES = (
        "NA", "Alpha", "ARM", "X86", "IA64", "MIPS", "MIPS64", "PPC", "S390", "SH", "SPARC", "SPARC64", "M68K",
        "MicroBlaze", "NIOS2", "Blackfin", "AVR32", "ST200", "NDS32", "OR1K"
    )

    IMAGE_NAMES = (
        "NA", "Standalone", "Kernel", "RAMDisk", "Multi-File", "Firmware", "Script", "FileSystem", "Flat-DT", "KWB",
        "IMX", "UBL", "OMAP", "AIS", "KernelNoLoad", "PBL", "MXS", "GP", "Atmel", "SoC-FPGA", "X86-Setup", "LPC32xx",
        "Loadable", "RK", "RKSD", "RKSPI", "ZYNQ"
    )

    COMPRESS_NAMES = ("uncompressed", "gzip", "bzip2", "lzma", "lzo", "lz4")

    @property
    def MagicNumber(self):
        return self._magicNumber

    @MagicNumber.setter
    def MagicNumber(self, value):
        self._magicNumber = value

    @property
    def HeaderCRC(self):
        return self._crc()

    @property
    def TimeStamp(self):
        return self._timeStamp

    @TimeStamp.setter
    def TimeStamp(self, value):
        self._timeStamp = value

    @property
    def DataSize(self):
        return self._dataSize

    @DataSize.setter
    def DataSize(self, value):
        self._dataSize = value

    @property
    def LoadAddress(self):
        return self._loadAddress

    @LoadAddress.setter
    def LoadAddress(self, value):
        self._loadAddress = value

    @property
    def EntryAddress(self):
        return self._entryAddress

    @EntryAddress.setter
    def EntryAddress(self, value):
        self._entryAddress = value

    @property
    def DataCRC(self):
        return self._dataCrc

    @DataCRC.setter
    def DataCRC(self, value):
        self._dataCrc = value

    @property
    def OsType(self):
        return self._osType

    @OsType.setter
    def OsType(self, value):
        assert OSType.check_value(value), "HEADER: Unknown Value of OS Type: %d" % value
        self._osType = int(value)

    @property
    def ArchType(self):
        return self._archType

    @ArchType.setter
    def ArchType(self, value):
        assert ARCHType.check_value(value), "HEADER: Unknown Value of Arch Type: %d" % value
        self._archType = int(value)

    @property
    def ImageType(self):
        return self._imageType

    @ImageType.setter
    def ImageType(self, value):
        assert IMGType.check_value(value), "HEADER: Unknown Value of Image Type: %d" % value
        self._imageType = int(value)

    @property
    def Compression(self):
        return self._compression

    @Compression.setter
    def Compression(self, value):
        assert COMPRESSType.check_value(value), "HEADER: Unknown Value of Compression Type: %d" % value
        self._compression = int(value)

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, value):
        assert type(value) is str, "HEADER: Name must be a string"
        assert len(value) <= 32, "HEADER: Name to long: %d char instead 32" % len(value)
        self._name = value

    @property
    def size(self):
        return self.SIZE

    def __init__(self, **kwargs):
        """ U-Boot Image Header Constructor
        :param laddr:    Load address
        :param eaddr:    Entry point address
        :param arch:     Architecture (ARCHType Enum)
        :param os:       Operating system (OSType Enum)
        :param image:    Image type (IMGType Enum)
        :param compress: Image compression (COMPRESSType Enum)
        :param name:     Image name (max: 32 chars)
        """
        self.MagicNumber  = 0x27051956  # U-Boot Default Value is 0x27051956
        self.TimeStamp    = int(time.time())
        self.DataSize     = 0
        self.DataCRC      = 0
        self.LoadAddress  = 0 if 'laddr' not in kwargs else kwargs['laddr']
        self.EntryAddress = 0 if 'eaddr' not in kwargs else kwargs['eaddr']
        self.OsType       = OSType.LINUX if 'os' not in kwargs else kwargs['os']
        self.ArchType     = ARCHType.ARM if 'arch' not in kwargs else kwargs['arch']
        self.ImageType    = IMGType.STD if 'image' not in kwargs else kwargs['image']
        self.Compression  = COMPRESSType.NONE if 'compress' not in kwargs else kwargs['compress']
        self.Name         = '' if 'name' not in kwargs else kwargs['name']

    def __len__(self):
        return self.size

    def __repr__(self):
        msg = str()
        msg += "Magic Number:  0x{0:08X}\n".format(self.MagicNumber)
        msg += "Header CRC:    0x{0:08X}\n".format(self.HeaderCRC)
        msg += "Created:       {0:s}\n".format(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(self.TimeStamp)))
        msg += "Data Size:     {0:.02f} kB\n".format(self.DataSize / 1024)
        msg += "Load Address:  0x{0:08X}\n".format(self.LoadAddress)
        msg += "Entry Address: 0x{0:08X}\n".format(self.EntryAddress)
        msg += "Data CRC:      0x{0:08X}\n".format(self.DataCRC)
        msg += "OS Type:       {0:s}\n".format(OSType.value_to_str(self.OsType))
        msg += "Arch Type:     {0:s}\n".format(ARCHType.value_to_str(self.ArchType))
        msg += "Image Type:    {0:s}\n".format(IMGType.value_to_str(self.ImageType))
        msg += "Compression:   {0:s}\n".format(COMPRESSType.value_to_str(self.Compression))
        msg += "Image Name:    {0:s}\n".format(self.Name)
        return msg

    def _crc(self):
        header = pack(self.FORMAT,
                      self.MagicNumber,
                      0,
                      self.TimeStamp,
                      self.DataSize,
                      self.LoadAddress,
                      self.EntryAddress,
                      self.DataCRC,
                      self.OsType,
                      self.ArchType,
                      self.ImageType,
                      self.Compression,
                      self.Name.encode('utf-8'))
        return CRC32(header)

    def info(self):
        msg  = "Image Name:    {0:s}\n".format(self.Name)
        msg += "Created:       {0:s}\n".format(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(self.TimeStamp)))
        msg += "Image Type:    {0:s} {1:s} {2:s} ({3:s})\n".format(self.ARCH_NAMES[self.ArchType],
                                                                   self.OS_NAMES[self.OsType],
                                                                   self.IMAGE_NAMES[self.ImageType],
                                                                   self.COMPRESS_NAMES[self.Compression])
        msg += "Data Size:     {0:.02f} kB\n".format(self.DataSize / 1024)
        msg += "Load Address:  0x{0:08X}\n".format(self.LoadAddress)
        msg += "Entry Address: 0x{0:08X}\n".format(self.EntryAddress)
        return msg

    def parse(self, data, offset=0):
        if len(data) < self.size:
            raise Exception("Header: Too small size of input data !")

        val = unpack_from(self.FORMAT, data, offset)
        self.MagicNumber  = val[0]
        header_crc        = val[1]
        self.TimeStamp    = val[2]
        self.DataSize     = val[3]
        self.LoadAddress  = val[4]
        self.EntryAddress = val[5]
        self.DataCRC      = val[6]
        self.OsType       = val[7]
        self.ArchType     = val[8]
        self.ImageType    = val[9]
        self.Compression  = val[10]
        self.Name         = val[11].decode('utf-8').strip('\0')

        if header_crc != self._crc():
            raise Exception("Header: Uncorrect CRC of input data !")

        return self.size

    def export(self):
        header = pack(self.FORMAT,
                      self.MagicNumber,
                      self.HeaderCRC,
                      self.TimeStamp,
                      self.DataSize,
                      self.LoadAddress,
                      self.EntryAddress,
                      self.DataCRC,
                      self.OsType,
                      self.ArchType,
                      self.ImageType,
                      self.Compression,
                      self.Name.encode('utf-8'))
        return header
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# UBoot Image Classes
# ----------------------------------------------------------------------------------------------------------------------
class BaseImage(object):
    def __init__(self, **kwargs):
        self._header = Header(**kwargs)

    @property
    def LoadAddress(self):
        return self._header.LoadAddress

    @LoadAddress.setter
    def LoadAddress(self, value):
        self._header.LoadAddress = value

    @property
    def EntryAddress(self):
        return self._header.EntryAddress

    @EntryAddress.setter
    def EntryAddress(self, value):
        self._header.EntryAddress = value

    @property
    def OsType(self):
        return self._header.OsType

    @OsType.setter
    def OsType(self, value):
        self._header.OsType = value

    @property
    def ArchType(self):
        return self._header.ArchType

    @ArchType.setter
    def ArchType(self, value):
        self._header.ArchType = value

    @property
    def ImageType(self):
        return self._header.ImageType

    @property
    def Compression(self):
        return self._header.Compression

    @Compression.setter
    def Compression(self, value):
        self._header.Compression = value

    @property
    def Name(self):
        return self._header.Name

    @Name.setter
    def Name(self, value):
        self._header.Name = value

    def __str__(self):
        return self.info()

    def __repr__(self):
        return self.info()

    def info(self):
        self.export()
        return self._header.info()

    def parse(self, data, offset=0):
        raise NotImplementedError()

    def export(self):
        raise NotImplementedError()


class StdImage(BaseImage):
    def __init__(self, data=None, **kwargs):
        """ Image Constructor
        :param data:     Image content as byte array
        :param laddr:    Load address
        :param eaddr:    Entry point address
        :param arch:     Architecture (ARCHType Enum)
        :param os:       Operating system (OSType Enum)
        :param image:    Image type (IMGType Enum)
        :param compress: Image compression (COMPRESSType Enum)
        :param name:     Image name (max: 32 chars)
        """
        super().__init__(**kwargs)
        self._data = data if data else bytearray()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def info(self):
        msg  = super().info()
        msg += "Content:       Binary Blob ({0:d} Bytes)\n".format(len(self._data))
        return msg

    def parse(self, data, offset=0):
        """ Load the image from byte array.
            :param data:   The raw image as byte array
            :param offset: The offset of input data
        """
        offset += self._header.parse(data, offset)
        if len(data[offset:]) < self._header.DataSize:
            raise Exception("Image: Too small size of input data !")

        self._data = data[offset:offset + self._header.DataSize]
        if CRC32(self._data) != self._header.DataCRC:
            raise Exception("Image: Uncorrect CRC of input data ")

    def export(self):
        """ Export the image into byte array. """
        if len(self._data) == 0:
            raise Exception("Image: No data to export !")

        self._header.DataSize = len(self._data)
        self._header.DataCRC = CRC32(self._data)

        return self._header.export() + self._data


class FwImage(StdImage):
    def __init__(self, data=None, **kwargs):
        """ Image Constructor
        :param data:     Image content as byte array
        :param laddr:    Load address
        :param eaddr:    Entry point address
        :param arch:     Architecture (ARCHType Enum)
        :param os:       Operating system (OSType Enum)
        :param compress: Image compression (COMPRESSType Enum)
        :param name:     Image name (max: 32 chars)
        """
        super().__init__(data, **kwargs)
        # Set The Image Type to Firmware
        self._header.ImageType = IMGType.FIRMWARE


class ScriptImage(BaseImage):

    @property
    def cmds(self):
        return self._cmds

    @cmds.setter
    def cmds(self, value):
        self._cmds = value

    def __init__(self, cmds=None, **kwargs):
        """ Script Image Constructor
        :param cmds:     List of commands, the item is in format [<cmd_name>, <cmd_value>]
        :param laddr:    Load address
        :param eaddr:    Entry point address
        :param arch:     Architecture (ARCHType Enum)
        :param os:       Operating system (OSType Enum)
        :param compress: Image compression (COMPRESSType Enum)
        :param name:     Image name (max: 32 chars)
        """
        super().__init__(**kwargs)
        # Set The Image Type to Script
        self._header.ImageType = IMGType.SCRIPT
        self._cmds = cmds if cmds else []

    def __len__(self):
        return len(self._cmds)

    def __iter__(self):
        return iter(self._cmds)

    def __getitem__(self, key):
        return self._cmds[key]

    def __setitem__(self, key, value):
        self._cmds[key] = value

    def info(self):
        i = 0
        msg  = super().info()
        msg += 'Content:       {0:d} Commands\n'.format(len(self._cmds))
        for cmd in self._cmds:
            msg += "{0:3d}) {1:s} {2:s}\n".format(i, cmd[0], cmd[1])
            i += 1
        return msg

    def append(self, cmd_name, cmd_value):
        assert type(cmd_name) is str, "ScriptImage: Command name must be a string"
        assert type(cmd_value) is str, "ScriptImage: Command value must be a string"
        self._cmds.append([cmd_name, cmd_value])

    def pop(self, index):
        assert 0 <= index < len(self._cmds)
        return self._cmds.pop(index)

    def clear(self):
        self._cmds.clear()

    def load(self, txt_data):

        for line in txt_data.split('\n'):
            line = line.rstrip('\0')
            if not line:
                continue
            if line.startswith('#'):
                continue
            cmd = line.split(' ', 1)
            if len(cmd) == 1:
                cmd.append('')
            self._cmds.append([cmd[0], cmd[1]])

    def store(self, txt_data=None):
        """ Store variables into text file
        :param txt_data:
        :return: txt_data
        """
        if txt_data is None:
            txt_data = ""

        txt_data += '# U-Boot Script\n\n'
        for cmd in self._cmds:
            txt_data += "{0:s} {1:s}\n".format(cmd[0], cmd[1])

        return txt_data

    def parse(self, data, offset=0):
        """ Load the image from byte array.
            :param data:   The raw image as byte array
            :param offset: The offset of input data
        """
        offset += self._header.parse(data, offset)
        if len(data[offset:]) < self._header.DataSize:
            raise Exception("Image: Too small size of input data !")

        data = data[offset:offset + self._header.DataSize]
        if CRC32(data) != self._header.DataCRC:
            raise Exception("Image: Uncorrect CRC of input data ")

        # TODO: Check image format for script type
        size = unpack_from('!2L', data)[0]
        offset = 8

        data = data[offset:offset+size].decode('utf-8')
        for line in data.split('\n'):
            line = line.rstrip('\0')
            if not line:
                continue
            if line.startswith('#'):
                continue
            cmd = line.split(' ', 1)
            if len(cmd) == 1:
                cmd.append('')
            self._cmds.append(cmd)

    def export(self):
        """ Export the image into byte array. """
        if len(self._cmds) == 0:
            raise Exception("Image: No data to export !")

        data = b''
        for cmd in self._cmds:
            data += "{0:s} {1:s}\n".format(cmd[0], cmd[1]).encode('utf-8')
        data = pack('!2L', len(data), 0) + data

        self._header.DataSize = len(data)
        self._header.DataCRC = CRC32(data)

        return self._header.export() + data


class MultiImage(BaseImage):
    def __init__(self, imgs=None, **kwargs):
        """ Multi Image Constructor
        :param imgs:     The list of all images
        :param laddr:    Load address
        :param eaddr:    Entry point address
        :param arch:     Architecture (ARCHType Enum)
        :param os:       Operating system (OSType Enum)
        :param compress: Image compression (COMPRESSType Enum)
        :param name:     Image name (max: 32 chars)
        """
        super().__init__(**kwargs)
        # Set Image Type as Multi in default
        self._header.ImageType = IMGType.MULTI
        self._imgs = imgs if imgs else []

    def __len__(self):
        return len(self._imgs)

    def __iadd__(self, value):
        self._imgs += value

    def __iter__(self):
        return iter(self._imgs)

    def __getitem__(self, key):
        return self._imgs[key]

    def __setitem__(self, key, value):
        self._imgs[key] = value

    def __delitem__(self, key):
        self._imgs.remove(key)

    def info(self):
        msg  = super().info()
        msg += 'Content:       {0:d} Images\n'.format(len(self._imgs))
        n = 0
        for img in self._imgs:
            msg += '#IMAGE[' + str(n) + ']\n'
            msg += img.info()
            n += 1
        return msg

    def append(self, image):
        assert isinstance(image, BaseImage), "MultiImage: Unsupported value"
        self._imgs.append(image)

    def pop(self, index):
        assert 0 <= index < len(self._imgs)
        return self._imgs.pop(index)

    def cear(self):
        self._imgs.clear()

    def parse(self, data, offset=0):
        """ Load the image from byte array.
            :param data:   The raw image as byte array
            :param offset: The offset of input data
        """
        offset += self._header.parse(data, offset)

        if len(data[offset:]) < self._header.DataSize:
            raise Exception("MultiImage: Too small size of input data !")

        if CRC32(data[offset:offset + self._header.DataSize]) != self._header.DataCRC:
            raise Exception("MultiImage: Uncorrect CRC of input data !")

        if self._header.ImageType != int(IMGType.MULTI):
            raise Exception("MultiImage: Not a Multi Image Type !")

        # Clear Images list
        self._imgs.clear()

        # Parse images lengths
        sList = []
        while True:
            (length,) = unpack_from('!L', data, offset)
            offset += 4
            if length == 0: break
            sList.append(length)

        # Parse images itself
        for size in sList:
            self._imgs.append(parse_img(data, offset))
            offset += size

    def export(self):
        """ Export the image into byte array.
            :return
        """
        data = bytes()
        dlen = []

        if len(self._imgs) == 0:
            raise Exception("MultiImage: No data to export !")

        for img in self._imgs:
            dimg = img.export()
            dlen.append(len(dimg))
            data += dimg

        dlen.append(0)
        fmt = "!{0:d}L".format(len(dlen))
        data = pack(fmt, *dlen) + data

        self._header.DataSize = len(data)
        self._header.DataCRC = CRC32(data)

        return self._header.export() + data
# ----------------------------------------------------------------------------------------------------------------------


def get_img_type(data, offset=0):
    """ Help function for extracting image fom raw data
    :param data: The raw data as byte array
    :param offset: The offset
    :return: Image type and offset where image start
    """
    while True:
        if (offset + Header.SIZE) > len(data):
            raise Exception("Error: Not an U-Boot image !")

        (header_mn, header_crc,) = unpack_from('!2L', data, offset)
        # Check the magic number if is U-Boot image
        if header_mn == 0x27051956:
            header = bytearray(data[offset:offset+Header.SIZE])
            header[4:8] = [0]*4
            if header_crc == CRC32(header):
                break
        offset += 4

    (image_type,) = unpack_from('B', data, offset + 30)

    return image_type, offset


def new_img(img_type):
    """ Help function for creating image
    :param img_type:
    :return: Image object
    """
    if img_type == int(IMGType.MULTI):
        img_obj = MultiImage()
    elif img_type == int(IMGType.FIRMWARE):
        img_obj = FwImage()
    elif img_type == int(IMGType.SCRIPT):
        img_obj = ScriptImage()
    else:
        img_obj = StdImage(image=img_type)

    return img_obj


def parse_img(data, offset=0):
    """ Help function for extracting image fom raw data
    :param data: The raw data as byte array
    :param offset: The offset
    :param magic_number:
    :return: Image object
    """
    (imgType, offset) = get_img_type(bytearray(data), offset)
    imgObj = new_img(imgType)
    imgObj.parse(data, offset)

    return imgObj
