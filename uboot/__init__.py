# Copyright 2018 Martin Olejar
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

from .common import EnumArchType, EnumOsType, EnumImageType, EnumCompressionType
from .old_image import StdImage, FwImage, ScriptImage, MultiImage, get_img_type, new_img, parse_img
from .fdt_image import FdtImage, parse_its, parse_itb
from .env_image import EnvImgOld
from .env_blob import EnvBlob


__author__  = "Martin Olejar"
__contact__ = "martin.olejar@gmail.com"
__version__ = "0.1.0"
__license__ = "Apache 2.0"
__status__  = "Development"
__all__ = [
    # Classes
    'EnvBlob',
    'EnvImgOld',
    'FdtImage',
    'StdImage',
    'FwImage',
    'ScriptImage',
    'MultiImage',
    # Enums
    'EnumOsType',
    'EnumArchType',
    'EnumImageType',
    'EnumCompressionType',
    # Methods
    'get_img_type',
    'new_img',
    'parse_img',
    'parse_its',
    'parse_itb'
]


def parse_blob(data, offset=0):
    """ Universal parser for binary blob

    :param data:
    :param offset:
    :return:
    """
    raise NotImplementedError()
