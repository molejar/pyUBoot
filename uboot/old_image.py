# Copyright 2017 Martin Olejar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import zlib
from struct import pack, unpack_from, calcsize

from .common import EnumArchType, EnumOsType, EnumImageType, EnumCompressionType

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
# UBoot Image Header Class
# ----------------------------------------------------------------------------------------------------------------------
class Header(object):
    MAGIC_NUMBER = 0x27051956
    FORMAT = '!7L4B32s'      # (Big-endian, 7 ULONGS, 4 UCHARs, 32-byte string)
    SIZE = calcsize(FORMAT)  # Should be 64-bytes

    @property
    def header_crc(self):
        return  CRC32(pack(self.FORMAT,
                           self.magic_number,
                           0,
                           self.time_stamp,
                           self.data_size,
                           self.load_address,
                           self.entry_address,
                           self.data_crc,
                           self.os_type,
                           self.arch_type,
                           self.image_type,
                           self.compression,
                           self.name.encode('utf-8')))

    @property
    def os_type(self):
        return self._os_type

    @os_type.setter
    def os_type(self, value):
        assert EnumOsType.validate(value), "HEADER: Unknown Value of OS Type: %d" % value
        self._os_type = int(value)

    @property
    def arch_type(self):
        return self._arch_type

    @arch_type.setter
    def arch_type(self, value):
        assert EnumArchType.validate(value), "HEADER: Unknown Value of Arch Type: %d" % value
        self._arch_type = int(value)

    @property
    def image_type(self):
        return self._image_type

    @image_type.setter
    def image_type(self, value):
        assert EnumImageType.validate(value), "HEADER: Unknown Value of Image Type: %d" % value
        self._image_type = int(value)

    @property
    def compression(self):
        return self._compression

    @compression.setter
    def compression(self, value):
        assert EnumCompressionType.validate(value), "HEADER: Unknown Value of Compression Type: %d" % value
        self._compression = int(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
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
        self.magic_number = self.MAGIC_NUMBER  # U-Boot Default Value is 0x27051956
        self.time_stamp = int(time.time())
        self.data_size = 0
        self.data_crc = 0
        self.load_address = 0
        self.entry_address = 0
        self._os_type = EnumOsType.LINUX
        self._arch_type = EnumArchType.ARM
        self._image_type = EnumImageType.STANDALONE
        self._compression = EnumCompressionType.NONE
        self._name = ''

        if 'laddr' in kwargs:
            try:
                self.load_address = int(kwargs['laddr'], 0) if isinstance(kwargs['laddr'], str) else int(kwargs['laddr'])
            except ValueError:
                raise Exception("The value of \"laddr\" is not correct !")
        if 'eaddr' in kwargs:
            try:
                self.entry_address = int(kwargs['eaddr'], 0) if isinstance(kwargs['eaddr'], str) else int(kwargs['eaddr'])
            except ValueError:
                raise Exception("The value of \"eaddr\" is not correct !")
        if 'os' in kwargs and kwargs['os'] is not None:
            val = kwargs['os']
            self.os_type = val if isinstance(val, int) else EnumOsType.value(val)
        if 'arch' in kwargs and kwargs['arch'] is not None:
            val = kwargs['arch']
            self.arch_type = val if isinstance(val, int) else EnumArchType.value(val)
        if 'image' in kwargs and kwargs['image'] is not None:
            val = kwargs['image']
            self.image_type = val if isinstance(val, int) else EnumImageType.value(val)
        if 'compress' in kwargs and kwargs['compress'] is not None:
            val = kwargs['compress']
            self.compression = val if isinstance(val, int) else EnumCompressionType.value(val)
        if 'name' in kwargs and kwargs['name'] is not None:
            self.name = kwargs['name']

    def __len__(self):
        return self.size

    def __str__(self):
        return self.info()

    def __repr__(self):
        return self.info()

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __eq__(self, obj):
        if not isinstance(obj, Header):
            return False
        if self.header_crc != obj.header_crc:
            return False
        return True

    def info(self):
        msg  = "Image Name:    {0:s}\n".format(self.name)
        msg += "Created:       {0:s}\n".format(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(self.time_stamp)))
        msg += "Image Type:    {0:s} {1:s} {2:s} ({3:s})\n".format(EnumArchType.name(self.arch_type),
                                                                   EnumOsType.name(self.os_type),
                                                                   EnumImageType.name(self.image_type),
                                                                   EnumCompressionType.name(self.compression))
        msg += "Data Size:     {0:.02f} kB\n".format(self.data_size / 1024)
        msg += "Load Address:  0x{0:08X}\n".format(self.load_address)
        msg += "Entry Address: 0x{0:08X}\n".format(self.entry_address)
        return msg

    def export(self):
        return pack(self.FORMAT,
                    self.magic_number,
                    self.header_crc,
                    self.time_stamp,
                    self.data_size,
                    self.load_address,
                    self.entry_address,
                    self.data_crc,
                    self.os_type,
                    self.arch_type,
                    self.image_type,
                    self.compression,
                    self.name.encode('utf-8'))

    @classmethod
    def parse(cls, data, offset=0):
        if len(data) < cls.SIZE:
            raise Exception("Header: Too small size of input data !")

        val = unpack_from(cls.FORMAT, data, offset)
        header = cls()

        header.magic_number = val[0]
        header_crc = val[1]
        header.time_stamp = val[2]
        header.data_size = val[3]
        header.load_address = val[4]
        header.entry_address = val[5]
        header.data_crc = val[6]
        header.os_type = val[7]
        header.arch_type = val[8]
        header.image_type = val[9]
        header.compression = val[10]
        header.name = val[11].decode('utf-8').strip('\0')

        if header.magic_number != header.MAGIC_NUMBER:
            raise Exception("Header: Magic number not valid !")

        if header_crc != header.header_crc:
            raise Exception("Header: Uncorrect CRC of input data !")

        return header
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# UBoot Image Classes
# ----------------------------------------------------------------------------------------------------------------------
class BaseImage(object):
    def __init__(self, **kwargs):
        self.header = Header(**kwargs)

    def __str__(self):
        return self.info()

    def __repr__(self):
        return self.info()

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def info(self):
        self.export()
        return self.header.info()

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
        self.data = data if data else bytearray()

    def __eq__(self, obj):
        if not isinstance(obj, StdImage):
            return False
        if self.__len__() != len(obj):
            return False
        if self.data != obj.data:
            return False
        return True

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def info(self):
        msg  = super().info()
        msg += "Content:       Binary Blob ({0:d} Bytes)\n".format(len(self.data))
        return msg

    def export(self):
        """ Export the image into byte array. """
        if len(self.data) == 0:
            raise Exception("Image: No data to export !")

        self.header.data_size = len(self.data)
        self.header.data_crc = CRC32(self.data)

        return self.header.export() + self.data

    @classmethod
    def parse(cls, data, offset=0):
        """ Load the image from byte array.
            :param data:   The raw image as byte array
            :param offset: The offset of input data
        """
        img = cls()
        img.header = Header.parse(data, offset)
        offset += img.header.size
        if len(data[offset:]) < img.header.data_size:
            raise Exception("Image: Too small size of input data !")

        img.data = data[offset:offset + img.header.data_size]
        if CRC32(img.data) != img.header.data_crc:
            raise Exception("Image: Uncorrect CRC of input data ")

        return img


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
        self.header.image_type = EnumImageType.FIRMWARE

        def __eq__(self, obj):
            if not isinstance(obj, FwImage):
                return False
            if self.__len__() != len(obj):
                return False
            if self.data != obj.data:
                return False
            return True


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
        self.header.image_type = EnumImageType.SCRIPT
        self._cmds = cmds if cmds else []

    def __eq__(self, obj):
        if not isinstance(obj, ScriptImage):
            return False
        if self.__len__() != len(obj):
            return False
        if self.cmds != obj.cmds:
            return False
        return True

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

    def export(self):
        """ Export the image into byte array. """
        if len(self._cmds) == 0:
            raise Exception("Image: No data to export !")

        data = b''
        for cmd in self._cmds:
            data += "{0:s} {1:s}\n".format(cmd[0], cmd[1]).encode('utf-8')
        data = pack('!2L', len(data), 0) + data

        self.header.data_size = len(data)
        self.header.data_crc = CRC32(data)

        return self.header.export() + data

    @classmethod
    def parse(cls, data, offset=0):
        """ Load the image from byte array.
            :param data:   The raw image as byte array
            :param offset: The offset of input data
        """
        img = cls()
        img.header = Header.parse(data, offset)
        offset += img.header.size
        if len(data[offset:]) < img.header.data_size:
            raise Exception("Image: Too small size of input data !")

        data = data[offset:offset + img.header.data_size]
        if CRC32(data) != img.header.data_crc:
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
            img.append(cmd[0], cmd[1])

        return img


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
        self.header.image_type = EnumImageType.MULTI
        self._imgs = imgs if imgs else []

    def __eq__(self, obj):
        if not isinstance(obj, MultiImage):
            return False
        if self.__len__() != len(obj):
            return False
        for img in self._imgs:
            if img not in obj:
                return False
        return True

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
            # images must be aligned
            if len(dimg) % 4:
                dimg += b'\0' * (len(dimg) % 4)
            dlen.append(len(dimg))
            data += dimg

        dlen.append(0)
        fmt = "!{0:d}L".format(len(dlen))
        data = pack(fmt, *dlen) + data

        self.header.data_size = len(data)
        self.header.data_crc = CRC32(data)

        return self.header.export() + data

    @classmethod
    def parse(cls, data, offset=0):
        """ Load the image from byte array.
            :param data:   The raw image as byte array
            :param offset: The offset of input data
        """
        img = cls()
        img.header = Header.parse(data, offset)
        offset += img.header.size

        if len(data[offset:]) < img.header.data_size:
            raise Exception("MultiImage: Too small size of input data !")

        if CRC32(data[offset:offset + img.header.data_size]) != img.header.data_crc:
            raise Exception("MultiImage: Uncorrect CRC of input data !")

        if img.header.image_type != EnumImageType.MULTI:
            raise Exception("MultiImage: Not a Multi Image Type !")

        # Parse images lengths
        sList = []
        while True:
            (length,) = unpack_from('!L', data, offset)
            offset += 4
            if length == 0: break
            sList.append(length)

        # Parse images itself
        for size in sList:
            img.append(parse_img(data, offset))
            offset += size

        return img
# ----------------------------------------------------------------------------------------------------------------------


def get_img_type(data, offset=0):
    """ Help function for extracting image fom raw data
    :param data: The raw data as byte array
    :param offset: The offset
    :return: Image type and offset where image start
    """
    while True:
        if (offset + Header.SIZE) > len(data):
            raise Exception("Not an U-Boot image !")

        (header_mn, header_crc,) = unpack_from('!2L', data, offset)
        # Check the magic number if is U-Boot image
        if header_mn == Header.MAGIC_NUMBER:
            header = bytearray(data[offset:offset+Header.SIZE])
            header[4:8] = [0]*4
            if header_crc == CRC32(header):
                break
        offset += 4

    (image_type,) = unpack_from('B', data, offset + 30)

    return image_type, offset


def new_img(**kwargs):
    """ Help function for creating image
    :param img_type:
    :return: Image object
    """
    if not 'image' in kwargs:
        kwargs['image'] = EnumImageType.FIRMWARE

    if isinstance(kwargs['image'], str):
        img_type = EnumImageType.value(kwargs['image'])
    else:
        img_type = kwargs['image']

    if not EnumImageType.validate(img_type):
        raise Exception()

    if img_type == EnumImageType.MULTI:
        img_obj = MultiImage(**kwargs)
    elif img_type == EnumImageType.FIRMWARE:
        img_obj = FwImage(**kwargs)
    elif img_type == EnumImageType.SCRIPT:
        img_obj = ScriptImage(**kwargs)
    else:
        img_obj = StdImage(**kwargs)

    return img_obj


def parse_img(data, offset=0):
    """ Help function for extracting image fom raw data
    :param data: The raw data as byte array
    :param offset: The offset
    :return: Image object
    """
    (img_type, offset) = get_img_type(bytearray(data), offset)

    if not EnumImageType.validate(img_type):
        raise Exception("Not a valid image type")

    if img_type == EnumImageType.MULTI:
        img = MultiImage.parse(data, offset)
    elif img_type == EnumImageType.FIRMWARE:
        img = FwImage.parse(data, offset)
    elif img_type == EnumImageType.SCRIPT:
        img = ScriptImage.parse(data, offset)
    else:
        img = StdImage.parse(data, offset)
        img.header.image_type = img_type

    return img
