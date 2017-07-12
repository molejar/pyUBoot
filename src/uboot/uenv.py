# Copyright 2016 Martin Olejar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import struct
import binascii
import collections

if sys.version_info[0] < 3:
    raise "Must be using Python 3"


class EnvBlob(object):
    def __init__(self, name=None, size=8192, redundant=False, empty_value=0x00):
        self._name = name
        self._size = size
        self._redundant = redundant
        self._empty_value = empty_value
        self._env = collections.OrderedDict()

    def __repr__(self):
        msg = str()
        msg += "Name:       " + str(self._name) + "\n"
        msg += "Size:       " + str(self._size) + " Bytes\n"
        msg += "Redundant:  " + str(self._redundant) + "\n"
        msg += "EmptyValue: " + str(self._empty_value) + "\n"
        msg += "Variables:\n"

        for key, val in self._env.items():
            msg += "- {0:s} = {1:s}\n".format(key, val)

        return msg

    def __len__(self):
        return self._size

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

    def get(self, name=None):
        """ Get the value of u-boot environment variable. If name is None, get list of all variables
            :param name: The variable name
            :return The variable value
        """
        if name:
            assert isinstance(name, str), "Error "
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

    def parse(self, data, offset=0):
        """ Parse the u-boot environment variables from bytearray.
            :param data: The data in bytes array
            :param offset: The offset of input data
        """
        self._env = collections.OrderedDict()

        (read_crc, tmp) = struct.unpack_from("IB", data, offset)
        if tmp == 0x01:
            self._redundant = True
            read_data = data[offset + 5:]
        else:
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

        ret = struct.pack("IB", crc, 0x01) if self._redundant else struct.pack("I", crc)
        ret += env_blob

        return ret


# Only for test purpose
if __name__ == "__main__":

    # create env blob
    env = EnvBlob(name="U-Boot Variables")
    env.redundant = True
    env.set("bootdelay", "3")
    env.set("stdin", "serial")
    env.set("stdout", "serial")
    env.set("stderr", "serial")
    env.set("baudrate", "115200")
    env.set("console", "ttymxc3")
    env.set("ethaddr", "12:34:56:78:90:AB")
    env.set("ethact", "FEC")
    env.set("mmcdev", "0")
    env.set("mmcpart", "1")
    env.set("rootdev", "mmcblk2p2")
    env.set("fdtaddr", "0x18000000")
    env.set("fdtfile", "imx6q-pop-arm2.dtb")
    env.set("loadfdt", "fatload mmc ${mmcdev}:${mmcpart} ${fdtaddr} ${fdtfile}")
    env.set("imgaddr", "0x12000000")
    env.set("imgfile", "zImage")
    env.set("loadimg", "fatload mmc ${mmcdev}:${mmcpart} ${imgaddr} ${imgfile}")
    env.set("bootargs", "console=${console},${baudrate} root=/dev/${rootdev} rootwait rw")
    env.set("bootcmd", "run loadfdt; run loadimg; bootz ${imgaddr} - ${fdtaddr};")

    # create temp dir
    os.makedirs("../../temp", exist_ok=True)

    # save test file
    with open("../../temp/env.txt", 'w') as f:
        f.write(env.export(raw=False))

    with open("../../temp/env.img", 'wb') as f:
        f.write(env.export())

    # open test file
    with open("../../temp/env.img", 'rb') as f:
        env.parse(data = f.read())

    print(env)

    with open("../../temp/env.txt", 'r') as f:
        env.parse(data = f.read(), raw = False)

    print(env)