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


@pytest.mark.script_launch_mode('subprocess')
def test_mkenv_create(script_runner):
    ret = script_runner.run('mkenv', 'create', ENV_TXT, ENV_BIN_TEMP)
    assert ret.success


@pytest.mark.script_launch_mode('subprocess')
def test_mkenv_info(script_runner):
    ret = script_runner.run('mkenv', 'info', ENV_BIN_TEMP)
    assert ret.success


@pytest.mark.script_launch_mode('subprocess')
def test_mkenv_extract(script_runner):
    ret = script_runner.run('mkenv', 'extract', ENV_BIN_TEMP)
    assert ret.success
