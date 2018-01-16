#!/usr/bin/env python3

# Copyright (c) 2017 Martin Olejar, martin.olejar@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
import click
import uboot

# Application error code
ERROR_CODE = 1

# The version of u-boot tools
VERSION = uboot.__version__

# Short description of U-Boot mkimg tool
DESCRIP = (
    "The U-Boot Image Tool"
)


# User defined class
class UInt(click.ParamType):
    """ Custom argument type for UINT """
    name = 'unsigned int'

    def __repr__(self):
        return 'UINT'

    def convert(self, value, param, ctx):
        try:
            if isinstance(value, (int,)):
                return value
            else:
                return int(value, 0)
        except:
            self.fail('{} is not a valid value'.format(value), param, ctx)


# Create instances of custom argument types
UINT = UInt()

# --
ARCT = uboot.EnumArchType.all_names()
OST  = uboot.EnumOsType.all_names()
IMGT = uboot.EnumImageType.all_names()
COMT = uboot.EnumCompressionType.all_names()


# U-Boot mkimg: Base options
@click.group(context_settings=dict(help_option_names=['-?', '--help']), help=DESCRIP)
@click.version_option(VERSION, '-v', '--version')
def cli():
    click.echo()


# U-Boot mkimg: List image content
@cli.command(short_help="Show image content")
@click.argument('file', nargs=1, type=click.Path(exists=True))
def info(file):
    """ List image content """
    try:
        with open(file, 'rb') as f:
            img = uboot.parse_img(f.read())
            click.echo(img.info())

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)


# U-Boot mkimg: Create new image from attached files
@cli.command(short_help="Create U-Boot image from attached files")
@click.option('-a', '--arch', type=click.Choice(ARCT), default='arm', show_default=True, help='Architecture')
@click.option('-o', '--ostype', type=click.Choice(OST), default='linux', show_default=True, help='Operating system')
@click.option('-i', '--imgtype', type=click.Choice(IMGT), default='firmware', show_default=True, help='Image type')
@click.option('-c', '--compress', type=click.Choice(COMT), default='none', show_default=True, help='Image compression')
@click.option('-l', '--laddr',  type=UINT, default=0, show_default=True, help="Load address")
@click.option('-e', '--epaddr', type=UINT, default=0, show_default=True, help="Entry point address")
@click.option('-n', '--name', type=click.STRING, default="", help="Image name (max: 32 chars)")
@click.argument('outfile', nargs=1, type=click.Path(readable=False))
@click.argument('infiles',  nargs=-1, type=click.Path(exists=True))
def create(arch, ostype, imgtype, compress, laddr, epaddr, name, outfile, infiles):
    """ Create new image from attached files """
    try:
        img_type = uboot.EnumImageType.value(imgtype)

        if img_type == uboot.EnumImageType.MULTI:
            img = uboot.MultiImage
            for file in infiles:
                with open(file, 'rb') as f:
                    simg = uboot.parse_img(f.read())
                    img.append(simg)

        elif img_type == uboot.EnumImageType.MULTI:
            img = uboot.ScriptImage()
            with open(infiles[0], 'r') as f:
                img.load(f.read())

        else:
            img = uboot.StdImage(image=img_type)
            with open(infiles[0], 'rb') as f:
                img.data = bytearray(f.read())

        img.header.arch_type = uboot.EnumArchType.value(arch)
        img.header.os_type = uboot.EnumOsType.value(ostype)
        img.header.compression = uboot.EnumCompressionType.value(compress)
        img.header.load_address = laddr
        img.header.entry_point = epaddr
        img.header.name = name

        click.echo(img.info())
        with open(outfile, 'wb') as f:
            f.write(img.export())

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)

    click.secho("\n Created Image: %s" % outfile)


# U-Boot mkimg: Create new executable FDT image
@cli.command(short_help="Create U-Boot FDT image from *.its file")
@click.option('-a', '--align', type=UINT, default=None, help="Make the blob align to the <bytes>")
@click.option('-p', '--padding', type=UINT, default=None, help="Add padding to the blob of <bytes> long")
@click.option('-s', '--size', type=UINT, default=None, help="Make the blob at least <bytes> long")
@click.argument('outfile', nargs=1, type=click.Path(readable=False))
@click.argument('infile',  nargs=1, type=click.Path(exists=True))
def create_fdt(align, padding, size, outfile, infile):
    """ Create U-Boot FDT image from *.its file """

    try:
        raise Exception("Command not implemented yet")

        img = uboot.FdtImage()

        with open(infile, 'r') as f:
            pass

        # TODO: Finish U-Boot FDT Image creator

        with open(outfile, 'wb') as f:
            f.write(img.export())

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)

    click.secho("\n Created Image: %s" % outfile)


# U-Boot mkimg: Extract image content
@cli.command(short_help="Extract content from U-Boot image")
@click.argument('file',  nargs=1, type=click.Path(exists=True))
def extract(file):
    """ Extract image content """

    def get_file_ext(img):
        ext = ('bin', 'gz', 'bz2', 'lzma', 'lzo', 'lz4')
        return ext[img.compression]

    try:
        with open(file, 'rb') as f:
            raw_data = f.read()

        img = uboot.parse_img(raw_data)

        file_path, file_name = os.path.split(file)
        dest_dir = os.path.normpath(os.path.join(file_path, file_name + ".ex"))
        os.makedirs(dest_dir, exist_ok=True)

        if isinstance(img, uboot.FdtImage):
            pass
        elif img.image_type == uboot.EnumImageType.MULTI:
            n = 0
            for simg in img:
                with open(os.path.join(dest_dir, 'image_{0:02d}.bin'.format(n)), 'wb') as f:
                    f.write(simg.eport())
                n += 1
        elif img.image_type == uboot.EnumImageType.SCRIPT:
            with open(os.path.join(dest_dir, 'script.txt'), 'w') as f:
                f.write(img.store())

        else:
            with open(os.path.join(dest_dir, 'image.' + get_file_ext(img)), 'wb') as f:
                f.write(img.data)

        with open(os.path.join(dest_dir, 'info.txt'), 'w') as f:
            f.write(img.info())

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)

    click.secho("\n Image extracted into dir: %s" % dest_dir)


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
