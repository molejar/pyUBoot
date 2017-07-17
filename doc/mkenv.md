U-Boot Environment Blob Tool
============================

The `mkenv` is a tool to generate a U-Boot environment binary blob from a text file or extract U-Boot environment variables from a binary blob.
It's implementing similar functionality as `mkenvimage` tool natively used in Linux.

Usage
-----

For printing a general info of usage this tool execute `mkenv -?`.

```sh
$ Usage: mkenv [OPTIONS] COMMAND [ARGS]...

  The U-Boot Make Enviroment Blob Tool

  Options:
    -v, --version  Show the version and exit.
    -?, --help     Show this message and exit.

  Commands:
    create   Create new image from attached file
    extract  Extract image content
    info     List image content
```

## Commands

#### $ mkenv info FILE

Print the content of U-Boot environment blob in readable format

##### options:
* **-b, --bigendian** - The target is big endian (default is little endian)
* **-o, --offset** - The offset of input file (default: 0)
* **-s, --size** - The environment blob size (default: 8192)
* **-?, --help**   - Show help message and exit

##### Example:

```sh
$ mkenv info env.bin

Name:       None
Redundant:  True
Endian:     Little
Size:       8192 Bytes
EmptyValue: 0x00
Variables:
- bootdelay = 3
- stdin = serial
- stdout = serial
- stderr = serial
- baudrate = 115200
- console = ttymxc3
...
```

<br>

#### $ mkenv extract FILE

Extract the content of U-Boot environment blob and save it in readable text format

##### options:
* **-b, --bigendian** - The target is big endian (default is little endian)
* **-o, --offset** - The offset of input file (default: 0)
* **-s, --size** - The environment blob size (default: 8192)
* **-?, --help**   - Show help message and exit

##### Example:

```sh
$ mkenv extract env.bin

 Successfully extracted: env.txt

```

<br>

#### $ mkenv create [OPTIONS] INFILE OUTFILE

Create U-Boot environment blob from input text file

##### options:
* **-r, --redundant** - The environment has multiple copies in flash (default: False)
* **-b, --bigendian** - The target is big endian (default is little endian)
* **-s, --size** - The environment blob size (default: 8192)
* **-?, --help**   - Show help message and exit

##### Example:

```sh
$ mkenv create env.txt env.bin

 Successfully created: env.bin

```