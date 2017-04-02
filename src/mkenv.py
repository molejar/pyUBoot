#!/usr/bin/env python

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
import click

# PyUBoot module
import uboot

# The version of u-boot tools
VERSION = uboot.__version__

# Short description of U-Boot mkenv tool
DESCRIP = (
    "The U-Boot Make Enviroment Blob Tool"
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
@click.option('-o', '--offset', type=UINT, default=0, show_default=True, help="File Offset")
@click.option('-s', '--size', type=UINT, default=8192, show_default=True, help="Env Blob Size")
@click.argument('file', nargs=1, type=click.Path(exists=True))
def info(offset, size, file):
    """ List image content """
    try:
        env = uboot.EnvBlob()
        env.Open(file, offset=offset, size=size)
        click.echo(str(env))

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")


# U-Boot mkenv: Create new image from attached file
@cli.command(short_help="Create new image from attached file")
@click.option('-n', '--name', type=str, default="", help="Image name (max: 32 chars)")
@click.option('-r', '--redundant', is_flag=True, show_default=True, help="Redundant Env.")
@click.option('-s', '--size', type=UINT, default=8192, show_default=True, help="Env. Blob Size")
@click.argument('outfile', nargs=1, type=click.Path(readable=False))
@click.argument('infile', nargs=1, type=click.Path(exists=True))
def create(size, redundant, name, outfile, infile):
    """ Create new image from attached file """
    try:
        env = uboot.EnvBlob()
        env.name = name
        env.size = size
        env.redundant = redundant
        env.Open(infile, type='txt')
        env.Save(outfile, type='bin')
        click.secho("Done Successfully")

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")


# U-Boot mkenv: Extract image content
@cli.command(short_help="Extract image content")
@click.argument('file', nargs=1, type=click.Path(exists=True))
def extract(file):
    """ Extract image content """
    try:
        fileName, _ = os.path.splitext(file)
        env = uboot.EnvBlob()
        env.Open(file, type='bin')
        env.Save(fileName + '.txt', type='txt')
        click.secho("Done Successfully")

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
