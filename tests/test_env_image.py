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
import shutil
import pytest
from uboot import EnvImgOld

# Used Directories
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')

# Test Files
UBOOT_BIN = os.path.join(DATA_DIR, 'u-boot.bin')
ENV_TXT_TEMP = os.path.join(TEMP_DIR, 'u-boot_env.txt')
UBOOT_BIN_TEMP = os.path.join(TEMP_DIR, 'u-boot.bin')


def setup_module(module):
    # Create temp directory
    os.makedirs(TEMP_DIR, exist_ok=True)
    shutil.copyfile(UBOOT_BIN, UBOOT_BIN_TEMP)


def teardown_module(module):
    # Delete created files
    #os.remove(ENV_TXT_TEMP)
    #os.remove(UBOOT_BIN_TEMP)
    pass


def test_01():
    pass


def test_02():
    pass


def test_03():
    pass