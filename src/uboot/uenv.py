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

import os
import struct
import binascii
import collections


class EnvBlob(object):

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        assert type(value) is str, "name is not a string: %r" % value
        self._name = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def redundant(self):
        return self._redundant

    @redundant.setter
    def redundant(self, value):
        self._redundant = value

    @property
    def bigendian(self):
        return self._bigendian

    @bigendian.setter
    def bigendian(self, value):
        self._bigendian = value

    def __init__(self, name=None, size=8192, redundant=False, bigendian=False, empty_value=0x00):
        self._name = name
        self._size = size
        self._redundant = redundant
        self._bigendian = bigendian
        self._empty_value = empty_value
        self._env = collections.OrderedDict()

    def __str__(self):
        return self.info()

    def __repr__(self):
        return self.info()

    def __len__(self):
        return self._size

    def info(self):
        msg = str()
        msg += "Name:       {}\n".format(self._name)
        msg += "Redundant:  {}\n".format(self._redundant)
        msg += "Endian:     {}\n".format("Big" if self._bigendian else "Little")
        msg += "Size:       {} Bytes\n".format(self._size)
        msg += "EmptyValue: 0x{:02X}\n".format(self._empty_value)
        msg += "Variables:\n"
        for key, val in self._env.items():
            msg += "- {0:s} = {1:s}\n".format(key, val)
        return msg

    def get(self, name=None):
        """ Get the value of u-boot environment variable. If name is None, get list of all variables
        :param name: The variable name
        :return The variable value
        """
        if name:
            assert isinstance(name, str), "name is not a string: %r" % name
            if not name in self._env:
                raise Exception("ERROR: Env %s doesnt exist !" % name)
            return self._env[name]
        else:
            return self._env.keys()

    def set(self, name, value):
        """ Set the u-boot environment variable.
        :param name: The variable name
        :param value: The variable value
        """
        assert isinstance(name, str), "Error "
        if not isinstance(value, str):
            value = str(value)
        self._env[name] = value

    def clear(self):
        self._env.clear()

    def load(self, txt_data):
        """ Load variables from text file
        :param txt_data:
        """
        for line in txt_data.split('\n'):
            line = line.rstrip('\0')
            if not line: continue

            if line.startswith('#'):
                pass  # TODO: Parse init values
            else:
                name, value = line.split('=', 1)
                self._env[name.strip()] = value.strip()

    def store(self, txt_data=None):
        """ Store variables into text file
        :param txt_data:
        :return: txt_data
        """
        if txt_data is None:
            txt_data = ""

        txt_data += "# Name:      {0:s}\n".format(self.name if self.name else "")
        txt_data += "# Size:      {0:d}\n".format(self.size)
        txt_data += "# Redundant: {0:s}\n".format("Yes" if self.redundant else "No")
        txt_data += "\n"

        for key, val in self._env.items():
            txt_data += "{0:s}={1:s}\n".format(key, val)

        return txt_data

    def parse(self, data, offset=0):
        """ Parse the u-boot environment variables from bytearray.
            :param data: The data in bytes array
            :param offset: The offset of input data
        """
        self._env = collections.OrderedDict()

        fmt = ">IB" if self._bigendian else "<IB"
        (read_crc, tmp) = struct.unpack_from(fmt, data, offset)

        if tmp == 0x01:
            self._redundant = True
            read_data = data[offset + 5:]
        else:
            self._redundant = False
            read_data = data[offset + 4:]

        calc_crc = binascii.crc32(read_data) & 0xffffffff

        if read_crc != calc_crc:
            raise ValueError("Wrong CRC")

        read_data = read_data.decode('utf-8')

        for s in read_data.split('\0'):
            if not s or s.startswith('\xFF') or s.startswith('\x00'):
                break
            key, value = s.split('=', 1)
            self._env[key] = value

    def export(self):
        """ Export the u-boot environment variables into bytearray.
        :return The environment variables in bytearray
        """
        env_size = self.size

        if self._redundant:
            env_size -= 5
        else:
            env_size -= 4

        data = str()
        for k in self._env:
            data += "{0:s}={1:s}".format(k, self._env[k])
            data += "\0"  # Termination of line "\0"
        data += "\0"      # End of file "\0\0"

        if len(data) > env_size:
            raise Exception("ERROR: ENV size out of range, extend required size !")

        env_blob = data + chr(self._empty_value) * (env_size - len(data))
        env_blob = env_blob.encode('utf-8')
        crc = binascii.crc32(env_blob) & 0xffffffff

        fmt = ">I" if self._bigendian else "<I"
        ret = struct.pack(fmt + "B", crc, 0x01) if self._redundant else struct.pack(fmt, crc)
        ret += env_blob

        return ret


class EnvImgOld(object):

    @property
    def start_string(self):
        return self._env_mark

    @property
    def max_size(self):
        return self._env_max_size

    @property
    def size(self):
        size = 2 * len(self._env)
        for key, value in self._env:
            size += len(key) + len(value)
        return size

    def __init__(self, start_string):
        self._env_mark = start_string
        self._env_offset = -1
        self._env_max_size = 0
        self._env = collections.OrderedDict()
        self._img = bytearray()
        self._file = ''

    def __str__(self):
        return self.info()

    def __repr__(self):
        return self.info()

    def _parse(self):
        """ Parse environment variables from image """
        self._env_offset = self._img.find(self._env_mark.encode())
        if self._env_offset == -1:
            raise Exception("Searched string \"%s\" doesnt exist in image" % self._env_mark)

        eof = 0
        index = self._env_offset
        while index < len(self._img):
            if self._img[index]:
                eof = 0
            else:
                eof += 1

            if eof == 2:
                self._env_max_size = index - self._env_offset - 1
                break

            index += 1

        data = self._img[self._env_offset : self._env_offset + self._env_max_size].decode()
        for s in data.split('\0'):
            key, value = s.split('=', 1)
            self._env[key] = value

    def _update(self):
        """ Update environment variables inside image """
        data = str()
        for key, val in self._env.items():
            data += "{0:s}={1:s}\0".format(key, val)

        if len(data) - 1 > self._env_max_size:
            raise Exception("EnVar blob size is out of range: %d instead %d bytes" % (len(data), self._env_max_size))

        if len(data) < self._env_max_size:
            data += "\0" * (self._env_max_size - len(data))

        index = self._env_offset
        for c in data:
            self._img[index] = ord(c)
            index += 1

    def info(self):
        """ Get info message
        :return string
        """
        msg = ""
        if self._file:
            msg += "Image Name:   {}\n".format(self._file)
        msg += "Image Size:   {} bytes\n".format(len(self._img))
        msg += "EnVar Size:   {} bytes\n".format(self._env_max_size)
        msg += "EnVar Offset: {} \n".format(self._env_offset)
        msg += "EnVar Mark:   {}\n".format(self._env_mark)
        msg += "EnVar Content:\n"
        for key, val in self._env.items():
            msg += "- {0:s} = {1:s}\n".format(key, val)

        return msg

    def get(self, name=None):
        """ Get the value of u-boot environment variable. If name is None, get list of all variables
        :param name: The variable name
        :return The variable value
        """
        if name:
            assert isinstance(name, str), "Env name is not a string: %r" % name
            if not name in self._env:
                raise Exception("EnVar name %s doesnt exist !" % name)
            return self._env[name]
        else:
            return self._env.keys()

    def set(self, name, value):
        """ Set the u-boot environment variable.
        :param name: The variable name
        :param value: The variable value
        """
        assert isinstance(name, str), "EnVar name is not a string: %r" % name
        if not isinstance(value, str):
            value = str(value)
        self._env[name] = value

    def clear(self):
        self._env.clear()

    def load(self, txt_data):
        """ Load the u-boot environment variables from readable string.
        :param txt_data: environment variables as string
        """
        for line in txt_data.split('\n'):
            line = line.rstrip('\0')
            if not line:
                continue
            if line.startswith('#'):
                continue
            env_name, env_value = line.split('=', 1)
            self._env[env_name.strip()] = env_value.strip()

    def store(self):
        """ Store the u-boot environment variables into readable string.
        :return environment variables as string
        """
        txt_data = ""

        for key, val in self._env.items():
            txt_data += "{0:s} = {1:s}\n".format(key, val)

        return txt_data

    def import_img(self, data):
        """ Import the u-boot image and parse environment variables from it.
        :param data: Image data in bytes
        """
        self._img = data if isinstance(data, bytearray) else bytearray(data)
        self._parse()

    def export_img(self):
        """ Export the u-boot image with updated environment variables.
        :return environment variables as string
        """
        self._update()
        return self._img

    def open_img(self, file):
        """ Open the u-boot image and parse environment variables from it.
        :param file: Path to image file
        """
        with open(file, 'rb') as f:
            self._img = bytearray(os.path.getsize(file))
            f.readinto(self._img)

        self._parse()
        self._file = file

    def save_img(self, file):
        """ Save the u-boot image with updated environment variables.
        :param file: Path to image file
        """
        self._update()
        with open(file, 'wb') as f:
            f.write(self._img)
