pyUBoot
=======

pyUBoot is an Open Source python based library for manipulating with U-Boot images and environment variables.

Dependencies
------------

- [Python 3](https://www.python.org) - The interpreter
- [Click](http://click.pocoo.org/6) - Python package for creating beautiful command line interface.

Installation
------------

To install the latest development version (master branch) execute in shell the following command:

``` bash
    $ pip3 install --pre -U https://github.com/molejar/pyUBoot/archive/master.zip
```

NOTE: you may run into permissions issues running these commands.
You have a few options here:

1. Run with `sudo -H` to install pyUBoot and dependencies globally
2. Specify the `--user` option to install local to your user
3. Run the command in a [virtualenv](https://virtualenv.pypa.io/en/latest/) local to a specific project working set.

You can also install from source by executing in shell the following commands:

``` bash
    $ git clone https://github.com/molejar/pyUBoot.git
    $ cd pyUBoot
    $ pip3 install .
```

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
                           arch=uboot.ARCHType.ARM,
                           os=uboot.OSType.LINUX,
                           image=uboot.IMGType.FIRMWARE,
                           compress=uboot.COMPRESSType.NONE)

    # --------------------------------------------------------------------------------
    # create script image (u-boot executable image)
    # --------------------------------------------------------------------------------
    scimg = uboot.ScriptImage()
    scimg.Name = "Test Script Image"
    scimg.OsType = uboot.OSType.LINUX
    scimg.ArchType = uboot.ARCHType.ARM
    scimg.Compression = uboot.COMPRESSType.NONE
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
                            arch=uboot.ARCHType.ARM,
                            os=uboot.OSType.LINUX,
                            compress=uboot.COMPRESSType.NONE)
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

The `pyUBoot` module is distributed with two command-line utilities (tools):
* [envimg](doc/envimg.md) - a tool for editing environment variables inside U-Boot image
* [mkenv](doc/mkenv.md) - a tool to generate/extract U-Boot environment variables into/from a binary blob
* [mkimg](doc/mkimg.md) - a tool for manipulation with U-Boot executable images (zImage, Scripts, ...)

TODO
----

* Add support for [FIT (Flattened Image Tree)](http://www.crashcourse.ca/wiki/index.php/U-Boot_FIT_images)
