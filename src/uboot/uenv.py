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

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, value):
        self._env = value

    def GetEnv(self, name):
        assert isinstance(name, str), "Error "
        if not name in self._env:
            raise Exception("ERROR: Env %s doesnt exist !" % name)
        return self._env[name]

    def SetEnv(self, name, value):
        assert isinstance(name, str), "Error "
        if not isinstance(value, str):
            value = str(value)
        self._env[name] = value

    def Load(self, data):
        self._env = collections.OrderedDict()

        for line in data.split('\n'):
            line = line.rstrip('\0')
            if not line: continue

            if line.startswith('#'):
                pass  # TODO: Parse init values
            else:
                key, value = line.split('=', 1)
                self._env[key] = value

    def Extract(self):
        """ Extract the u-boot environment variables as string.
            :return
        """
        ret = "# Name: {0:s}\n".format(self.name) if self.name else ""
        ret += "# Size: {0:d}\n".format(self.size)
        ret += "# Redundant: {0:s}\n".format("YES" if self.redundant else "NO")
        ret += "\n"

        for k in self._env:
            ret += "{0:s}={1:s}\n".format(k, self._env[k])

        return ret


    def Import(self, data, offset=0, size=None):
        """ Import the u-boot environment variables from bytearray.
            :param data:
            :param offset:
            :param size:
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

        if size: self.size = size
        read_data = read_data.decode('utf-8')

        for s in read_data.split('\0'):
            if not s or s.startswith('\xFF') or s.startswith('\x00'):
                break
            key, value = s.split('=', 1)
            self._env[key] = value


    def Export(self, size=None):
        """ Export the u-boot environment variables into bytearray.
            :param size:
            :return
        """
        env_size = self.size if not size else size

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

        if self._redundant:
            ret = struct.pack("IB", crc, 0x01)
        else:
            ret = struct.pack("I", crc)

        ret += env_blob
        return ret

    def Open(self, path, **kwargs):
        """ Reads the u-boot environment variables from TXT or BIN File.
            :param path:
            :param type:
            :param size:
            :param offset:
        """
        type = None if not 'type' in kwargs else kwargs['type']
        size = -1 if not 'size' in kwargs else kwargs['size']
        offset = 0 if not 'offset' in kwargs else kwargs['offset']

        if not os.path.exists(path):
            raise Exception("File %s doesnt exist" % path)

        if type is None:
            type = path.split('.')[-1]

        if type == 'img' or type == 'bin':
            with open(path, "rb") as f:
                f.seek(offset)
                data = f.read(size)
                self.Import(data)
                self.size = len(data)
        elif type == 'txt':
            with open(path, 'r') as f:
                data = f.read(size)
                self.Load(data)
        else:
            raise Exception("ERROR: None or unsupported file extension !")

    def Save(self, path, **kwargs):
        """ Save the u-boot environment variables into TXT or BIN File.
            :param path:
            :param type:
            :param size:
            :param offset:
        """
        type = None if not 'type' in kwargs else kwargs['type']
        size = None if not 'size' in kwargs else kwargs['size']
        offset = 0 if not 'offset' in kwargs else kwargs['offset']

        if type is None:
            type = path.split('.')[-1]

        if type == 'img' or type == 'bin':
            with open(path, 'wb') as f:
                f.seek(offset)
                f.write(self.Export(size=size))
        elif type == 'txt':
            with open(path, 'w') as f:
                f.write(self.Extract())
        else:
            raise Exception("ERROR: None or unsupported file extension !")

# Only for test purpose
if __name__ == "__main__":

    # create env blob
    env = EnvBlob(name="U-Boot Variables")
    env.redundant = True
    env.SetEnv("bootdelay", "3")
    env.SetEnv("stdin", "serial")
    env.SetEnv("stdout", "serial")
    env.SetEnv("stderr", "serial")
    env.SetEnv("baudrate", "115200")
    env.SetEnv("console", "ttymxc3")
    env.SetEnv("ethaddr", "12:34:56:78:90:AB")
    env.SetEnv("ethact", "FEC")
    env.SetEnv("mmcdev", "0")
    env.SetEnv("mmcpart", "1")
    env.SetEnv("rootdev", "mmcblk2p2")
    env.SetEnv("fdtaddr", "0x18000000")
    env.SetEnv("fdtfile", "imx6q-pop-arm2.dtb")
    env.SetEnv("loadfdt", "fatload mmc ${mmcdev}:${mmcpart} ${fdtaddr} ${fdtfile}")
    env.SetEnv("imgaddr", "0x12000000")
    env.SetEnv("imgfile", "zImage")
    env.SetEnv("loadimg", "fatload mmc ${mmcdev}:${mmcpart} ${imgaddr} ${imgfile}")
    env.SetEnv("bootargs", "console=${console},${baudrate} root=/dev/${rootdev} rootwait rw")
    env.SetEnv("bootcmd", "run loadfdt; run loadimg; bootz ${imgaddr} - ${fdtaddr};")

    # create temp dir
    os.makedirs("../temp", exist_ok=True)

    # save test file
    env.Save("../temp/env.txt")
    env.Save("../temp/env.img")
    env.Save("../temp/env", type="img")

    # open test file
    env.Open("../temp/env", type="img")
    print(env)
    env.Open("../temp/env.txt")
    print(env)
    env.Open("../temp/env.img")
    print(env)