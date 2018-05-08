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
from uboot import EnvBlob

# Used Directories
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')

# Test Files
ENV_TXT = os.path.join(DATA_DIR, 'env.txt')
ENV_TXT_TEMP = os.path.join(TEMP_DIR, 'env.txt')
ENV_BIN_TEMP = os.path.join(TEMP_DIR, 'env.bin')


def setup_module(module):
    # Create temp directory
    os.makedirs(TEMP_DIR, exist_ok=True)


def teardown_module(module):
    # Delete created files
    os.remove(ENV_TXT_TEMP)
    os.remove(ENV_BIN_TEMP)


def test_01():
    env = EnvBlob("Test")
    env.set("int_variable", 100)
    env.set("str_variable", "value")

    tmp = env.get("str_variable")
    assert tmp == "value"

    with pytest.raises(Exception):
        tmp = env.get("test")


def test_02():
    env = EnvBlob("Test")

    with open(ENV_TXT, 'r') as f:
        env.load(f.read())

    with open(ENV_TXT_TEMP, 'w') as f:
        f.write(env.store())

    with open(ENV_BIN_TEMP, 'wb') as f:
        f.write(env.export())
