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

    @classmethod
    def parse(cls, data, offset=0, bigendian=False):
        """ Parse the u-boot environment variables from bytearray.
            :param data: The data in bytes array
            :param offset: The offset of input data
            :param bigendian: The endian type
        """
        env = cls(bigendian=bigendian)

        fmt = ">IB" if env.bigendian else "<IB"
        (read_crc, tmp) = struct.unpack_from(fmt, data, offset)

        if tmp == 0x01:
            env.redundant = True
            read_data = data[offset + 5:]
        else:
            env.redundant = False
            read_data = data[offset + 4:]

        calc_crc = binascii.crc32(read_data) & 0xffffffff

        if read_crc != calc_crc:
            raise ValueError("Wrong CRC")

        read_data = read_data.decode('utf-8')

        for s in read_data.split('\0'):
            if not s or s.startswith('\xFF') or s.startswith('\x00'):
                break
            key, value = s.split('=', 1)
            env.set(key, value)

        return env

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
        crc_blob = struct.pack(fmt + "B", crc, 0x01) if self._redundant else struct.pack(fmt, crc)
        env_blob = crc_blob + env_blob

        return env_blob
