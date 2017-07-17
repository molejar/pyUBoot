#!/usr/bin/env python3

# Copyright 2016 Martin Olejar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import click

# PyUBoot module
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
            self.fail('%s is not a valid value' % value, param, ctx)


# Create instances of custom argument types
UINT = UInt()

# --
ARCT = uboot.ARCHType.GetNames(lower=True)
OST  = uboot.OSType.GetNames(lower=True)
IMGT = uboot.IMGType.GetNames(lower=True)
COMT = uboot.COMPRESSType.GetNames(lower=True)


# U-Boot mkimg: Base options
@click.group(context_settings=dict(help_option_names=['-?', '--help']), help=DESCRIP)
@click.version_option(VERSION, '-v', '--version')
def cli():
    click.echo()


# U-Boot mkimg: List image content
@cli.command(short_help="List image content")
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
@cli.command(short_help="Create new image from attached files")
@click.option('-a', '--arch', type=click.Choice(ARCT), default='arm', show_default=True, help='Architecture')
@click.option('-o', '--ostype', type=click.Choice(OST), default='linux', show_default=True, help='Operating system')
@click.option('-i', '--imgtype', type=click.Choice(IMGT), default='firmware', show_default=True, help='Image type')
@click.option('-c', '--compress', type=click.Choice(COMT), default='none', show_default=True, help='Image compression')
@click.option('-l', '--laddr',  type=UINT, default=0, show_default=True, help="Load address")
@click.option('-e', '--epaddr', type=UINT, default=0, show_default=True, help="Entry point address")
@click.option('-n', '--name', type=str, default="", help="Image name (max: 32 chars)")
@click.argument('outfile', nargs=1, type=click.Path(readable=False))
@click.argument('infiles',  nargs=-1, type=click.Path(exists=True))
def create(arch, ostype, imgtype, compress, laddr, epaddr, name, outfile, infiles):
    """ Create new image from attached files """
    try:
        img_type = uboot.IMGType.StrToValue(imgtype)

        if img_type == int(uboot.IMGType.MULTI):
            img = uboot.MultiImage
            for file in infiles:
                with open(file, 'rb') as f:
                    simg = uboot.parse_img(f.read())
                    img.append(simg)

        elif img_type == int(uboot.IMGType.SCRIPT):
            img = uboot.ScriptImage()
            with open(infiles[0], 'r') as f:
                data = f.read()
            for line in data.split('\n'):
                line = line.rstrip('\0')
                if not line:
                    continue
                if line.startswith('#'):
                    continue
                cmd = line.split(' ', 1)
                if len(cmd) == 1:
                    cmd.append('')
                img.append(cmd[0], cmd[1])

        else:
            img = uboot.StdImage(image=img_type)
            with open(infiles[0], 'rb') as f:
                img.data = f.read()

        img.ArchType = uboot.ARCHType.StrToValue(arch)
        img.OsType = uboot.OSType.StrToValue(ostype)
        img.Compression = uboot.COMPRESSType.StrToValue(compress)
        img.LoadAddress = laddr
        img.EntryPoint = epaddr
        img.Name = name

        click.echo(img.info())
        with open(outfile, 'wb') as f:
            f.write(img.export())

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)

    click.secho("\n Created Image: %s" % outfile)


# U-Boot mkimg: Extract image content
@cli.command(short_help="Extract image content")
@click.argument('file',  nargs=1, type=click.Path(exists=True))
def extract(file):
    """ Extract image content """

    def get_file_ext(img):
        ext = ('bin', 'gz', 'bz2', 'lzma', 'lzo', 'lz4')
        return ext[img.Compression]

    try:
        with open(file, 'rb') as f:
            raw_data = f.read()

        img = uboot.parse_img(raw_data)

        file_path, file_name = os.path.split(file)
        dest_dir = os.path.normpath(os.path.join(file_path, file_name + ".ex"))
        os.makedirs(dest_dir, exist_ok=True)

        if img.ImageType == int(uboot.IMGType.MULTI):
            n = 0
            for simg in img:
                with open(os.path.join(dest_dir, 'image_{0:02d}.bin'.format(n)), 'wb') as f:
                    f.write(simg.eport())
                n += 1
        elif img.ImageType == int(uboot.IMGType.SCRIPT):
            script = '# U-Boot Script\n\n'
            for cmd in img.cmds:
                script += "{0:s} {1:s}\n".format(cmd[0], cmd[1])
            with open(os.path.join(dest_dir, 'script.txt'), 'w') as f:
                f.write(script)

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
