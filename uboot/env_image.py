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

import os
import collections


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