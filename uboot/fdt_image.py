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


import fdt
import time
import struct

from .common import EnumOsType, EnumArchType, EnumImageType, EnumCompressionType


# ----------------------------------------------------------------------------------------------------------------------
# Helper methods
# ----------------------------------------------------------------------------------------------------------------------
def get_value(obj, name, default=None):
    prop = obj.get_property(name)
    return default if prop is None else prop[0]


def get_data(obj):
    prop = obj.get_property("data")
    if isinstance(prop, fdt.PropBytes):
        return prop.data
    if isinstance(prop, fdt.PropWords):
        data = bytearray()
        for val in prop.data:
            data += struct.pack(">I", val)
        return data

    raise Exception("Image data error")


# ----------------------------------------------------------------------------------------------------------------------
# FDT Image Class
# ----------------------------------------------------------------------------------------------------------------------
class FdtImage(object):

    def __init__(self):
        self.description = ""
        self.time_stamp = int(time.time())
        self.def_config = None
        self.configs = []
        self.img_info = []
        self.img_data = {}

    def __str__(self):
        return self.info()

    def __repr__(self):
        return self.info()

    def info(self):
        msg  = "FIT description: {}\n".format(self.description)
        msg += "Created:         {}\n".format(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(self.time_stamp)))
        msg += "Default config:  {}\n".format(self.def_config)
        for n, img in enumerate(self.img_info):
            msg += "\n"
            msg += " IMG[{}] {}\n".format(n, img.name)
            msg += "  size: {0:.02f} kB\n".format(len(self.img_data[img.name]) / 1024)
            for p in img.props:
                if isinstance(p, fdt.PropWords):
                    msg += "  {}: 0x{:X}\n".format(p.name, p[0])
                else:
                    msg += "  {}: {}\n".format(p.name, p[0])
        for n, cfg in enumerate(self.configs):
            msg += "\n"
            msg += " CFG[{}] {}\n".format(n, cfg.name)
            for p in cfg.props:
                msg += "  {}: {}\n".format(p.name, p[0])
        return msg

    def add_img(self, nfo, data):
        """
        :param nfo:
        :param data:
        :return:
        """
        assert isinstance(nfo, fdt.Node), "nfo type must be a fdt.Node"
        assert isinstance(data, (bytes, bytearray)), "data type must be a bytes or bytearray"

        if not nfo.exist_property("type"):
            raise Exception("Image type must be defined")

        for p in nfo.props:
            name, value = p.name, p[0]
            if name == "type" and value != "flat_dt" and not EnumImageType.validate(value):
                raise Exception("Unknown IMAGE type")
            elif name == "os" and not EnumOsType.validate(value):
                raise Exception("Unknown OS type")
            elif name == "arch" and not EnumArchType.validate(value):
                raise Exception("Unknown ARCH type")
            elif name == "compression" and not EnumCompressionType.validate(value):
                raise Exception("Unknown Compression type")

        self.img_info.append(nfo)
        self.img_data[nfo.name] = data

    def add_cfg(self, item, validate=False):
        """
        :param item:
        :param validate:
        :return:
        """
        assert isinstance(item, fdt.Node), "validate_cfg: item type must be a fdt.Node"
        for cfg in item.props:
            if cfg.name == "description":
                continue
            if validate and cfg[0] not in self.img_data:
                raise Exception("add_cfg: Config Validation Error")
        self.configs.append(item)

    def to_its(self, rpath=None, tabsize=4):
        """ Export to ITS format

        :param rpath:
        :param tabsize:
        :return:
        """
        data = {}
        images = fdt.Node("images")
        for img in self.img_info:
            img_name = img.name.replace('@', '_') + '.bin'
            img_clone = img.copy()
            img_clone.append(fdt.PropIncBin("data", None, img_name, rpath))
            images.append(img_clone)
            data[img_name] = self.img_data[img.name]

        # Check default config
        if self.def_config is None:
            raise Exception("Default config not defined")
        if self.def_config not in [cnf.name for cnf in self.configs]:
            raise Exception("Default config \"{}\" doesn't exist".format(self.def_config))

        # Add images and configs
        root_node = fdt.Node('/')
        root_node.append(fdt.PropStrings("description", self.description))
        root_node.append(images)
        configs = fdt.Node("configurations", nodes=self.configs)
        configs.append(fdt.PropStrings("default", self.def_config))
        root_node.append(configs)

        # Crete ITS
        its = "/dts-v1/;\n"
        its += '\n'
        its += root_node.to_dts(tabsize)
        return its, data

    def to_itb(self, padding=0, align=None, size=None):
        """ Export to ITB format

        :param padding:
        :param align:
        :param size:
        :return:
        """
        img_blob = bytes()
        img_offset = padding

        fdt_obj = fdt.FDT()
        fdt_obj.add_item(fdt.PropWords("timestamp", int(time.time()) if self.time_stamp is None else self.time_stamp))
        fdt_obj.add_item(fdt.PropStrings("description", self.description))

        # Add images
        node = fdt.Node("images")
        for image in self.img_info:
            if image.name not in self.img_data:
                raise Exception("export: data is None")
            cimg = image.copy()
            data = self.img_data[image.name]
            if padding:
                img_blob += data
                img_offset += len(data)
                cimg.append(fdt.PropWords("data-size", len(data)))
                cimg.append(fdt.PropWords("data-position", img_offset))
            else:
                cimg.append(fdt.PropBytes("data", data=data))
            node.append(cimg)
        fdt_obj.add_item(node)

        # Check default config
        if self.def_config is None:
            raise Exception("Default config not defined")
        if self.def_config not in [cnf.name for cnf in self.configs]:
            raise Exception("Default config \"{}\" doesn't exist".format(self.def_config))

        # Add configs
        node = fdt.Node("configurations")
        node.append(fdt.PropStrings("default", self.def_config))
        for cfg in self.configs:
            node.append(cfg)
        fdt_obj.add_item(node)

        # Generate FDT blob
        itb = fdt_obj.to_dtb(17)

        # ...
        if padding:
            itb_align = padding - len(itb)
            if itb_align < 0:
                raise Exception()
            if itb_align > 0:
                itb += bytes([0] * itb_align)
            itb += img_blob

        return itb


def parse_its(text, root_dir=''):
    """ Parse ITS file

    :param text:
    :param root_dir:
    :return:
    """
    its_obj = fdt.parse_dts(text, root_dir)
    # ...
    fim_obj = FdtImage()
    prop = its_obj.get_property("description")
    if prop is not None:
        fim_obj.description = prop[0]

    # Parse images
    node = its_obj.get_node("images")
    if node is None:
        raise Exception("parse_its: images not defined")
    for img in node.nodes:
        img_data = get_data(img)
        img.remove_property("data")
        fim_obj.add_img(img, img_data)

    # Parse configs
    node = its_obj.get_node("configurations")
    if node is None or not node.nodes:
        raise Exception("parse_its: configurations not defined")
    for cfg in node.nodes:
        fim_obj.add_cfg(cfg, True)
    fim_obj.def_config = get_value(node, "default")

    return fim_obj


def parse_itb(data, offset=0):
    """ Parse ITB data-blob

    :param data:
    :param offset:
    :return:
    """
    fdt_obj = fdt.parse_dtb(data, offset)
    # ...
    fim_obj = FdtImage()
    fim_obj.time_stamp = get_value(fdt_obj, "timestamp")
    fim_obj.description = get_value(fdt_obj, "description", "")

    # Parse images
    node = fdt_obj.get_node("images")
    if node is None or not node.nodes:
        raise Exception("parse_itb: images not defined")
    for img in node.nodes:
        if img.exist_property("data"):
            img_data = get_data(img)
            img.remove_property("data")
        elif img.exist_property("data-size") and img.exist_property("data-position"):
            data_size = get_value(img, "data-size")
            data_offset = get_value(img, "data-position")
            img_data = data[offset + data_offset : offset + data_offset + data_size]
            img.remove_property("data-size")
            img.remove_property("data-position")
        else:
            raise Exception()
        fim_obj.add_img(img, img_data)

    # Parse configs
    node = fdt_obj.get_node("configurations")
    if node is None or not node.nodes:
        raise Exception("parse_itb: configurations not defined")
    for cfg in node.nodes:
        fim_obj.add_cfg(cfg, True)
    fim_obj.def_config = get_value(node, "default")

    return fim_obj
