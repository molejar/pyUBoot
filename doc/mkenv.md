U-Boot Environment Blob Tool
============================

The `mkenv` is a tool to generate a U-Boot environment binary blob from a text file or extract U-Boot environment variables from a binary blob/image.
It's implementing similar functionality as `mkenvimage` tool natively used in Linux.

Usage
-----

For printing a general info of usage this tool execute `mkenv -?`.

```sh
   $ Usage: mkenv [OPTIONS] COMMAND [ARGS]...
   $
   $ The U-Boot Make Enviroment Blob Tool
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

