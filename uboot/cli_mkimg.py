# Copyright 2017 Martin Olejar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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


@cli.command(short_help="Show old image content")
@click.argument('file', nargs=1, type=click.Path(exists=True))
def info(file):
    """ List old image content """
    try:
        with open(file, 'rb') as f:
            img = uboot.parse_img(f.read())
            click.echo(img.info())

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)


@cli.command(short_help="Show new image content")
@click.argument('file', nargs=1, type=click.Path(exists=True))
def info_itb(file):
    """ List new image content """
    try:
        with open(file, 'rb') as f:
            img = uboot.parse_itb(f.read())
            click.echo(img.info())

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)


@cli.command(short_help="Create old U-Boot image from attached files")
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
    """ Create old U-Boot image from attached files """
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


@cli.command(short_help="Create new U-Boot image from *.its file")
@click.option('-o', '--outfile', type=click.Path(readable=False), default=None, help="Output file")
@click.option('-p', '--padding', type=UINT, default=0, help="Add padding to the blob of <bytes> long")
@click.option('-a', '--align', type=UINT, default=None, help="Make the blob align to the <bytes>")
@click.option('-s', '--size', type=UINT, default=None, help="Make the blob at least <bytes> long")
@click.argument('itsfile',  nargs=1, type=click.Path(exists=True))
def create_itb(outfile, padding, align, size, itsfile):
    """ Create new U-Boot image from *.its file """

    try:
        if outfile is None:
            outfile = os.path.splitext(itsfile)[0] + ".itb"

        with open(itsfile, 'r') as f:
            img = uboot.parse_its(f.read(), os.path.dirname(itsfile))

        with open(outfile, 'wb') as f:
            f.write(img.to_itb(padding, align, size))

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)

    click.secho("\n Created Image: %s" % outfile)


@cli.command(short_help="Extract content from old U-Boot image")
@click.argument('file',  nargs=1, type=click.Path(exists=True))
def extract(file):
    """ Extract content from old U-Boot image """

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

        if img.header.image_type == uboot.EnumImageType.MULTI:
            n = 0
            for simg in img:
                with open(os.path.join(dest_dir, 'image_{0:02d}.bin'.format(n)), 'wb') as f:
                    f.write(simg.eport())
                n += 1
        elif img.header.image_type == uboot.EnumImageType.SCRIPT:
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


@cli.command(short_help="Extract content from new U-Boot image")
@click.argument('file',  nargs=1, type=click.Path(exists=True))
def extract_itb(file):
    """ Extract content from new U-Boot image """

    try:
        with open(file, 'rb') as f:
            img = uboot.parse_itb(f.read())

        file_path, file_name = os.path.split(file)
        dest_dir = os.path.normpath(os.path.join(file_path, file_name + ".ex"))
        os.makedirs(dest_dir, exist_ok=True)

        its, images = img.to_its()

        with open(os.path.join(dest_dir, file_name.split('.')[0] + '.its'), 'w') as f:
            f.write(its)

        for name, data in images.items():
            with open(os.path.join(dest_dir, name + '.bin'), 'wb') as f:
                f.write(data)

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)

    click.secho("\n Image extracted into dir: %s" % dest_dir)


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
