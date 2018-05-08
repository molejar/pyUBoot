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
import uboot
import pytest

# Used Directories
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')

# Test Files
UBOOT_IMG_TEMP = os.path.join(TEMP_DIR, 'u-boot.img')



def setup_module(module):
    # Create temp directory
    os.makedirs(TEMP_DIR, exist_ok=True)


def teardown_module(module):
    # Delete created files
    os.remove(UBOOT_IMG_TEMP)


def test_01():
    # --------------------------------------------------------------------------------
    # create dummy firmware image (u-boot executable image)
    # --------------------------------------------------------------------------------
    fwimg = uboot.StdImage(bytes([1] * 512),
                           name="Firmware Test Image",
                           laddr=0,
                           eaddr=0,
                           arch=uboot.EnumArchType.ARM,
                           os=uboot.EnumOsType.LINUX,
                           image=uboot.EnumImageType.FIRMWARE,
                           compress=uboot.EnumCompressionType.NONE)

    # --------------------------------------------------------------------------------
    # create script image (u-boot executable image)
    # --------------------------------------------------------------------------------
    scimg = uboot.ScriptImage()
    scimg.Name = "Test Script Image"
    scimg.OsType = uboot.EnumOsType.LINUX
    scimg.ArchType = uboot.EnumArchType.ARM
    scimg.Compression = uboot.EnumCompressionType.NONE
    scimg.EntryAddress = 0
    scimg.LoadAddress = 0
    scimg.append("echo", "'===== U-Boot settings ====='")
    scimg.append("setenv", "stdin serial")
    scimg.append("setenv", "stdout serial")
    scimg.append("setenv", "rootdev mmcblk2p2")

    # --------------------------------------------------------------------------------
    # create multi-file image
    # --------------------------------------------------------------------------------
    mimg = uboot.MultiImage(name="Multi-File Test Image",
                            laddr=0,
                            eaddr=0,
                            arch=uboot.EnumArchType.ARM,
                            os=uboot.EnumOsType.LINUX,
                            compress=uboot.EnumCompressionType.NONE)
    mimg.append(fwimg)
    mimg.append(scimg)

    # --------------------------------------------------------------------------------
    # save created image into file: uboot_mimg.img
    # --------------------------------------------------------------------------------
    with open(UBOOT_IMG_TEMP, "wb") as f:
        f.write(mimg.export())

    # --------------------------------------------------------------------------------
    # open and read image file: uboot_mimg.img
    # --------------------------------------------------------------------------------
    with open(UBOOT_IMG_TEMP, "rb") as f:
        data = f.read()

    # --------------------------------------------------------------------------------
    # parse binary data into new img object of specific image type
    # --------------------------------------------------------------------------------
    img = uboot.parse_img(data)

    # check if are identical
    assert mimg == img
