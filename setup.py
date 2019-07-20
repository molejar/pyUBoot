#!/usr/bin/env python

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


from os import path
from setuptools import setup
from uboot import __version__, __license__, __author__, __contact__


def long_description():
    try:
        import pypandoc

        readme_path = path.join(path.dirname(__file__), 'README.md')
        return pypandoc.convert(readme_path, 'rst')
    except (IOError, ImportError):
        return (
            "More on: https://github.com/molejar/pyUBoot"
        )

setup(
    name='uboot',
    author=__author__,
    version=__version__,
    license=__license__,
    author_email=__contact__,
    url='https://github.com/molejar/pyUBoot',
    description='Open Source library for manipulating with U-Boot images and environment variables',
    long_description=long_description(),
    python_requires='>=3.6',
    install_requires=[
        'fdt==0.1.2',
        'click==7.0',
        'easy_enum==0.2.0'
    ],
    packages=['uboot'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Utilities'
    ],
    entry_points={
        'console_scripts': [
            'envimg = uboot.cli_envimg:main',
            'mkenv  = uboot.cli_mkenv:main',
            'mkimg  = uboot.cli_mkimg:main'
        ],
    }
)
