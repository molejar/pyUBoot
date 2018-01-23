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


import fdt

from .common import EnumArchType, EnumOsType, EnumImageType, EnumCompressionType


class ImgItem(object):

    def __init__(self):
        pass


class FdtImage(object):

    def __init__(self):
        self.its = None
        self.images = None
        self.padding = 0
        self.align = 0

    def load(self, text, root_dir=''):
        dt = fdt.parse_dts(text, root_dir)
        images = dt.rootnode.get_item_by_name("images", fdt.Node)
        config = dt.rootnode.get_item_by_name("configurations", fdt.Node)
        if images is None or config is None:
            raise Exception(" ")

    def export(self, size=None):
        if self.its is None:
            raise Exception(" ")
        data = self.its.export()

    @classmethod
    def parse(cls, data, offset=0):
        itb = fdt.parse_dtb(data[offset:])

