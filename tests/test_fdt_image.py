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
import pytest
from uboot import parse_itb, parse_its, FdtImage


# Used Directories
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')

# Test Files
UBOOT_ITS = os.path.join(DATA_DIR, 'u-boot.its')
UBOOT_ITB_TEMP = os.path.join(TEMP_DIR, 'u-boot.itb')


def setup_module(module):
    # Create temp directory
    os.makedirs(TEMP_DIR, exist_ok=True)


def teardown_module(module):
    # Delete created files
    #os.remove(UBOOT_ITB_TEMP)
    pass


def test_01():
    pass