#!/usr/bin/env python

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


from setuptools import setup, find_packages

# Check python version
import sys
if sys.version_info[0] == 2:
    sys.exit('Sorry, Python 2.x is not supported')

sys.path.insert(0, './src')
from uboot import __version__, __license__, __author__, __contact__

setup(
    name='uboot',
    author=__author__,
    version=__version__,
    license=__license__,
    author_email=__contact__,
    url='https://github.com/molejar/pyUBoot',
    platforms="Mac OSX, Windows, Linux",
    install_requires=['click>=5.0', 'fdt'],
    packages=find_packages('src'),
    package_dir={'':'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Utilities'
    ],
    description='Open Source library for manipulating with U-Boot images and environment variables',
    py_modules=['envimg', 'mkenv', 'mkimg'],
    entry_points={
        'console_scripts': [
            'envimg = envimg:main',
            'mkenv = mkenv:main',
            'mkimg = mkimg:main'
        ],
    }
)
