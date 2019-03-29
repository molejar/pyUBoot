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
   create       Create old U-Boot image from attached files
   createitb    Create new U-Boot image from *.its file
   extract      Extract content from old U-Boot image
   extractitb   Extract content from new U-Boot image
   info         Show old image content
   infoitb      Show new image content
```

## Commands for old U-Boot images

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

## Commands for new FDT U-Boot images

#### $ mkimg infoitb FILE

List new U-Boot image content in readable format

##### Example:

```sh
$ mkimg infoitb image.itb

FIT description: i.MX7D U-Boot Image
Created:         Fri May 11 21:51:14 2018
Default config:  config@1

 IMG[0] uboot@1
  size: 472.00 kB
  description: U-Boot (32-bit)
  type: standalone
  arch: arm
  compression: none
  load: 0x40200000

 IMG[1] fdt@1
  size: 46.00 kB
  description: FDT i.MX7D-SDB
  type: flat_dt
  compression: none

 CFG[0] config@1
  description: fsl-imx7d-sdb
  firmware: uboot@1
  fdt: fdt@1
```

<br>

#### $ mkimg createitb [OPTIONS] FILE

Create new U-Boot image from *.its file 

##### options:
* **-o, --outfile** - Output path/file name
* **-p, --padding** - Add padding to the blob of <bytes> long (default: 0)
* **-a, --align** - Make the blob align to the <bytes> (default: 0)
* **-s, --size** - Make the blob at least <bytes> long (default: none)
* **-?, --help**   - Show help message and exit

##### Example:

```sh
$ mkimg createitb image.its

 Created Image: image.itb
```

<br>

#### $ mkimg extractitb FILE

Extract content from new U-Boot image (*.itb)

##### Example:

```sh
$ mkimg extractitb image.itb

 Image extracted into dir: image.itb.ex
```

<br>
