pyUBoot
=======

[![Build Status](https://travis-ci.org/molejar/pyUBoot.svg?branch=master)](https://travis-ci.org/molejar/pyUBoot)
[![Coverage Status](https://coveralls.io/repos/github/molejar/pyUBoot/badge.svg?branch=master)](https://coveralls.io/github/molejar/pyUBoot?branch=master)
[![PyPI Status](https://img.shields.io/pypi/v/uboot.svg)](https://pypi.python.org/pypi/uboot)
[![Python Version](https://img.shields.io/pypi/pyversions/uboot.svg)](https://www.python.org)

pyUBoot is an Open Source python based library for manipulating with U-Boot images and environment variables. Is 
distributed with following command-line utilities (tools):

* [envimg](docs/envimg.md) - a tool for editing environment variables inside U-Boot image
* [mkenv](docs/mkenv.md) - a tool to generate/extract U-Boot environment variables into/from a binary blob
* [mkimg](docs/mkimg.md) - a tool for manipulation with U-Boot executable images (zImage, Scripts, ...)

Dependencies
------------

- [Python](https://www.python.org) - Python 3.x interpreter
- [Click](http://click.pocoo.org/6) - Python package for creating beautiful command line interface.
- [pyFDT](https://github.com/molejar/pyFDT) - Python package for manipulation with Device Tree images.

Installation
------------

``` bash
    $ pip install uboot
```

To install the latest version from master branch execute in shell following commands:

``` bash
    $ pip install -r https://raw.githubusercontent.com/molejar/pyUBoot/master/requirements.txt
    $ pip install -U https://github.com/molejar/pyUBoot/archive/master.zip
```

In case of development, install it from cloned sources:

``` bash
    $ git clone https://github.com/molejar/pyUBoot.git
    $ cd pyUBoot
    $ pip install -r requirements.txt
    $ pip install -U -e .
```

**NOTE:** You may run into a permissions issues running these commands. Here are a few options how to fix it:

1. Run with `sudo` to install pyUBoot and dependencies globally
2. Specify the `--user` option to install locally into your home directory (export "~/.local/bin" into PATH variable if haven't).
3. Run the command in a [virtualenv](https://virtualenv.pypa.io/en/latest/) local to a specific project working set.

Usage
-----

The first example is showing how to use `EnvBlob` class from `uboot` module in your code.

``` python

    import uboot

    # --------------------------------------------------------------------------------
    # create env blob
    # --------------------------------------------------------------------------------
    env = uboot.EnvBlob(name="U-Boot Variables")
    env.redundant = True
    env.set("bootdelay", "3")
    env.set("stdin", "serial")
    env.set("stdout", "serial")

    # --------------------------------------------------------------------------------
    # save env blob as binary file
    # --------------------------------------------------------------------------------
    with open("env.img", 'wb') as f:
        f.write(env.export())

    # --------------------------------------------------------------------------------
    # save env blob in readable format as text file
    # --------------------------------------------------------------------------------
    with open("env.txt", 'w') as f:
        f.write(env.store())

    # --------------------------------------------------------------------------------
    # parse env blob from binary file
    # --------------------------------------------------------------------------------
    with open("env.img", 'rb') as f:
        env.parse(f.read())

    # print env blob info
    print("U-Boot enviroment blob loaded from env.img file:")
    print(env)
    print()

    # --------------------------------------------------------------------------------
    # load env blob from text file
    # --------------------------------------------------------------------------------
    with open("env.txt", 'r') as f:
        env.load(f.read())

    # print env blob info
    print("U-Boot enviroment blob loaded from env.txt file:")
    print(env)
```

The second example is showing how to create Multi-File U-Boot image with `uboot` module.

``` python

    import uboot

    # --------------------------------------------------------------------------------
    # create dummy firmware image (u-boot executable image)
    # --------------------------------------------------------------------------------
    fwimg = uboot.StdImage(bytes([1]*512),
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
    # print created image info
    print(mimg)

    # --------------------------------------------------------------------------------
    # save created image into file: uboot_mimg.img
    # --------------------------------------------------------------------------------
    with open("uboot_mimg.img", "wb") as f:
        f.write(mimg.export())

    # --------------------------------------------------------------------------------
    # open and read image file: uboot_mimg.img
    # --------------------------------------------------------------------------------
    with open("uboot_mimg.img", "rb") as f:
        data = f.read()

    # --------------------------------------------------------------------------------
    # parse binary data into new img object of specific image type
    # --------------------------------------------------------------------------------
    img = uboot.parse_img(data)

    # print parsed image info
    print(img)
```
