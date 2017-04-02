PyUBoot
=======

PyUBoot is an Open Source python based library for manipulating with U-Boot images and environment variables.

Dependencies
------------

- Python 3.x interpreter
- [click](http://click.pocoo.org/6) - A Python "Command Line Interface Creation Kit"

Installation
------------

To install the latest development version (master branch) execute in shell the following command:

``` bash
    $ pip install --pre -U https://github.com/molejar/PyUBoot/archive/master.zip
```

NOTE: you may run into permissions issues running these commands.
You have a few options here:

1. Run with `sudo -H` to install PyUBoot and dependencies globally
2. Specify the `--user` option to install local to your user
3. Run the command in a [virtualenv](https://virtualenv.pypa.io/en/latest/) local to a specific project working set.

You can also install from source by executing in shell the following commands:

``` bash
    $ git clone https://github.com/molejar/PyUBoot.git
    $ cd PyUBoot
    $ python setup.py install
```

Usage
-----

The following example is showing how to use `uboot` module in your code.

``` python

    import uboot

    # --------------------------------------------------------------------------------
    # create env blob
    # --------------------------------------------------------------------------------
    env = uboot.EnvBlob(name="U-Boot Variables")
    env.redundant = True
    env.SetEnv("bootdelay", "3")
    env.SetEnv("stdin", "serial")
    env.SetEnv("stdout", "serial")
    ...
    # --------------------------------------------------------------------------------
    # save env blob as "TXT" and "BIN" file
    # --------------------------------------------------------------------------------
    env.Save("env.txt")
    env.Save("env.img")
    # --------------------------------------------------------------------------------
    # save env blob as "BIN" file with specified file type
    # --------------------------------------------------------------------------------
    env.Save("env", type="img")

    # --------------------------------------------------------------------------------
    # open env blob
    # --------------------------------------------------------------------------------
    env.Open("env", type="img")
    print(env)

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
    scimg.AddCmd("echo", "===== U-Boot settings =====")
    scimg.AddCmd("setenv", "stdin serial")
    scimg.AddCmd("setenv", "stdout serial")
    scimg.AddCmd("setenv", "rootdev mmcblk2p2")

    # --------------------------------------------------------------------------------
    # create multi-file image
    # --------------------------------------------------------------------------------
    mimg = uboot.MultiImage(name="Multi-File Test Image",
                            laddr=0,
                            eaddr=0,
                            arch=uboot.ARCHType.ARM,
                            os=uboot.OSType.LINUX,
                            compress=uboot.COMPRESSType.NONE)
    mimg.Append(fwimg)
    mimg.Append(scimg)
    # print created image info
    print(mimg.GetInfo())

    # --------------------------------------------------------------------------------
    # save created image into file
    # --------------------------------------------------------------------------------
    with open("uboot_mimg.img", "wb") as f:
        f.write(mimg.Export())

    # --------------------------------------------------------------------------------
    # load image from file
    # --------------------------------------------------------------------------------
    with open("uboot_mimg.img", "rb") as f:
        data = f.read()
    # parse binary blob
    img = uboot.parse(data)
    # print info
    print(img.GetInfo())
```

PyUBoot is distributed with two command-line utilities: [mkimg](doc/mkimg.md) and [mkenv](doc/mkenv.md).

TODO
----

* Add support for [FIT (Flattened Image Tree)](http://www.crashcourse.ca/wiki/index.php/U-Boot_FIT_images)