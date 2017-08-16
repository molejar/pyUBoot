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

# Short description of U-Boot mkenv tool
DESCRIP = (
    "The U-Boot Make Environment Blob Tool"
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


# U-Boot mkenv: Base options
@click.group(context_settings=dict(help_option_names=['-?', '--help']), help=DESCRIP)
@click.version_option(VERSION, '-v', '--version')
def cli():
    click.echo()


# U-Boot mkenv: List image content
@cli.command(short_help="List image content")
@click.option('-b', '--bigendian', is_flag=True, help="The target is big endian (default is little endian)")
@click.option('-o', '--offset', type=UINT, default=0, show_default=True, help="The offset of input file")
@click.option('-s', '--size', type=UINT, default=8192, show_default=True, help="The environment blob size")
@click.argument('file', nargs=1, type=click.Path(exists=True))
def info(offset, size, file):
    """ List image content """
    try:
        env = uboot.EnvBlob()
        with open(file, "rb") as f:
            f.seek(offset)
            data = f.read(size)
            env.parse(data)
            env.size = len(data)

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)

    click.echo(str(env))


# U-Boot mkenv: Create new image from attached file
@cli.command(short_help="Create new image from attached file")
@click.argument('infile',  nargs=1, type=click.Path(exists=True))
@click.argument('outfile', nargs=1, type=click.Path(readable=False))
@click.option('-b', '--bigendian', is_flag=True, help="The target is big endian (default is little endian)")
@click.option('-r', '--redundant', is_flag=True, show_default=True, help="The environment has multiple copies in flash")
@click.option('-s', '--size', type=UINT, default=8192, show_default=True, help="The environment blob size")
def create(size, redundant, bigendian, infile, outfile):
    """ Create new image from attached file """
    try:
        env = uboot.EnvBlob(size=size, redundant=redundant, bigendian=bigendian)

        with open(infile, 'r') as f:
            env.load(f.read())

        with open(outfile, 'wb') as f:
            f.write(env.export())

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)

    click.secho(" Successfully created: %s" % outfile)


# U-Boot mkenv: Extract image content
@cli.command(short_help="Extract image content")
@click.argument('file', nargs=1, type=click.Path(exists=True))
@click.option('-o', '--offset', type=UINT, default=0, show_default=True, help="The offset of input file")
@click.option('-b', '--bigendian', is_flag=True, help="The target is big endian (default is little endian)")
@click.option('-s', '--size', type=UINT, default=8192, show_default=True, help="The environment blob size")
def extract(offset, size, file):
    """ Extract image content """
    try:
        fileName, _ = os.path.splitext(file)
        env = uboot.EnvBlob(size=size)

        with open(file, "rb") as f:
            f.seek(offset)
            env.parse(f.read())

        with open(fileName + '.txt', 'w') as f:
            f.write(env.store())

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)

    click.secho(" Successfully extracted: %s.txt" % fileName)


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
