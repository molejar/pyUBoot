U-Boot Image Tool
=================

The `mkimg` is a tool to create images for use with the U-Boot boot loader. These images can contain the linux kernel, device tree blob, root file system image, firmware images etc., either separate or combined.It's implementing similar functionality as `mkimage` tool used in Linux.

Usage
-----

For printing a general info of usage this tool execute `mkimg -?`.

```sh
   $ Usage: mkimg [OPTIONS] COMMAND [ARGS]...
   $
   $ The U-Boot Image Tool
   $
   $ Options:
   $  -v, --version  Show the version and exit.
   $  -?, --help     Show this message and exit.
   $
   $ Commands:
   $  create   Create new image from attached file
   $  extract  Extract image content
   $  info     List image content
```

