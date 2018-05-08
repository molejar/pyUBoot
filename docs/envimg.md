Tool for editing environment variables inside U-Boot image
==========================================================

The `envimg` is a tool for editing environment variables inside U-Boot image.

Usage
-----

For printing a general info of usage this tool execute `envimg -?`.

```sh
Usage: envimg.py [OPTIONS] COMMAND [ARGS]...

  Tool for editing environment variables inside U-Boot image

Options:
  -v, --version  Show the version and exit.
  -?, --help     Show this message and exit.

Commands:
  info     List U-Boot environment variables
  export   Export U-Boot environment variables
  replace  Replace U-Boot environment variables
  update   Update U-Boot environment variables
```

## Commands

#### $ envimg info [OPTIONS] MARK FILE

Print the content of U-Boot environment variables located inside image.

##### options:
* **-?, --help** - Show help message and exit

##### Example:

```sh
$ envimg info bootcmd= u-boot.imx

Image Name:   u-boot.imx
Image Size:   478208 bytes
EnVar Size:   2470 bytes
EnVar Offset: 312273
EnVar Mark:   bootcmd=
EnVar Content:
- bootcmd = mmc dev ${mmcdev}; mmc dev ${mmcdev}; if mmc rescan; then run mmcboot; else run netboot; fi;
- bootdelay = 3
- ...
```

<br>

#### $ envimg export [OPTIONS] MARK FILE FENV

Export environment variables from U-Boot image.

##### options:
* **-?, --help** - Show help message and exit

##### Example:

```sh
$ envimg export bootcmd= u-boot.imx env.txt

Environment variables saved into: env.txt
```

<br>

#### $ envimg update [OPTIONS] MARK FILE

Update environment variables inside U-Boot image.

##### options:
* **-f, --fenv** - The file with environment variables
* **-e, --env**  - Environment variables
* **-?, --help** - Show help message and exit

##### Example:

```sh
$ envimg update bootcmd= u-boot.imx -e "bootdelay = 6"

Image Name:   u-boot.imx
Image Size:   478208 bytes
EnVar Size:   2470 bytes
EnVar Offset: 312273
EnVar Mark:   bootcmd=
EnVar Content:
- bootcmd = mmc dev ${mmcdev}; mmc dev ${mmcdev}; if mmc rescan; then run mmcboot; else run netboot; fi;
- bootdelay = 6
- ...
```

<br>

#### $ envimg replace [OPTIONS] MARK FILE FENV

Replace environment variables inside U-Boot image.

##### options:
* **-?, --help** - Show help message and exit

##### Example:

```sh
$ envimg update bootcmd= u-boot.imx env.txt

...
```