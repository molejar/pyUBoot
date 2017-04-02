#!/usr/bin/env python

# Copyright 2016 Martin Olejar
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

import sys
from setuptools import setup, find_packages

sys.path.insert(0, './src')
import uboot

setup(
    name='PyUBoot',
    version=uboot.__version__,
    license='Apache 2.0',
    author='Martin Olejar',
    author_email='martin.olejar@gmail.com',
    url='https://github.com/molejar/PyUBoot',
    platforms="Mac OSX, Windows, Linux",
    install_requires=['click>=5.0'],
    packages=find_packages('src'),
    package_dir={'':'src'},
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Utilities'
    ],
    description='U-Boot Image Tools',
    py_modules=['mkenv', 'mkimg'],
    entry_points={
        'console_scripts': [
            'mkenv = mkenv:main',
            'mkimg = mkimg:main'
        ],
    }
)
