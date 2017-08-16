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


from .uenv import EnvBlob, EnvImgOld
from .uimg import StdImage, FwImage, ScriptImage, MultiImage, \
                  OSType, ARCHType, IMGType, COMPRESSType, get_img_type, new_img, parse_img

__author__ = 'Martin Olejar <martin.olejar@gmail.com>'
__version__ = '0.0.7'
__status__ = 'Development'
__all__ = [
    # Classes
    'EnvBlob',
    'EnvImgOld',
    'StdImage',
    'FwImage',
    'ScriptImage',
    'MultiImage',
    # Enums
    'OSType',
    'ARCHType',
    'IMGType',
    'COMPRESSType',
    # Methods
    'get_img_type',
    'new_img',
    'parse_img'
]