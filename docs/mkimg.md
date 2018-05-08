U-Boot Image Tool
=================

The `mkimg` is a tool to create images for use with the U-Boot boot loader. These images can contain the linux kernel, device tree blob, root file system image, firmware images etc., either separate or combined.It's implementing similar functionality as `mkimage` tool used in Linux.

Usage
-----

For printing a general info of usage this tool execute `mkimg -?`.

```sh
$ Usage: mkimg [OPTIONS] COMMAND [ARGS]...

  The U-Boot Image Tool

  Options:
    -v, --version  Show the version and exit.
    -?, --help     Show this message and exit.

  Commands:
    create   Create new image from attached file
    extract  Extract image content
    info     List image content
```

## Commands

#### $ mkimg info FILE

Print the U-Boot executable image content in readable format

##### Example:

```sh
$ mkimg info script.bin

Image Name:    iMX7D NetBoot Script
Created:       Tue Apr 04 17:15:01 2017
Image Type:    ARM Linux Script (uncompressed)
Data Size:     0.62 kB
Load Address:  0x00000000
Entry Address: 0x00000000
Content:       16 Commands
  0) echo '>> Run Script ...'
  1) setenv autoload 'no'
  2) dhcp
  3) setenv serverip 192.168.1.162
  4) setenv hostname 'imx7dsb'
  5) setenv netdev  'eth0'
  6) setenv nfsroot '/srv/nfs/imx7d'
  7) setenv imgfile '/imx7d/zImage'
  8) setenv fdtfile '/imx7d/imx7d-sdb.dtb'
  9) setenv fdtaddr 0x83000000
 10) setenv imgaddr 0x80800000
 11) setenv imgload 'tftp ${imgaddr} ${imgfile}'
 12) setenv fdtload 'tftp ${fdtaddr} ${fdtfile}'
 13) setenv netargs 'setenv bootargs console=${console},${baudrate} root=/dev/nfs rw nfsroot=${serverip}:${nfsroot},v3,tcp ip=dhcp'
 14) setenv netboot 'echo Booting from net ...; run netargs; run imgload; run fdtload; bootz ${imgaddr} - ${fdtaddr};'
 15) run netboot
```

<br>

#### $ mkimg extract FILE

Extract U-Boot executable image

##### Example:

```sh
$ mkimg extract script.bin

 Image extracted into dir: script.bin.ex

```

<br>

#### $ mkimg create [OPTIONS] OUTFILE [INFILES]

Create U-Boot executable image (uImage, Script, ...)

##### options:
* **-a, --arch** - Architecture (default: arm)
* **-o, --ostype** - Operating system (default: linux)
* **-i, --imgtype** - Image type (default: firmware)
* **-c, --compress** - Image compression (default: none)
* **-l, --laddr** - Load address (default: 0)
* **-e, --epaddr** - Entry point address (default: 0)
* **-n, --name** - Image name (max: 32 chars)
* **-?, --help**   - Show help message and exit

##### Example:

```sh
$ mkimg create -a arm -o linux -i script -c none script.bin script.txt

 Created Image: script.bin

```