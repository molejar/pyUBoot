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

# Short description of U-Boot envimg tool
DESCRIP = (
    "Tool for editing environment variables inside U-Boot image"
)


# U-Boot envimg: Base options
@click.group(context_settings=dict(help_option_names=['-?', '--help']), help=DESCRIP)
@click.version_option(VERSION, '-v', '--version')
def cli():
    click.echo()


# U-Boot envimg: List U-Boot environment variables
@cli.command(short_help="List U-Boot environment variables")
@click.argument('mark', nargs=1, type=click.STRING)
@click.argument('file', nargs=1, type=click.Path(exists=True))
def info(mark, file):
    """ List U-Boot environment variables """
    try:
        envimg = uboot.EnvImgOld(start_string=mark)
        envimg.open_img(file)

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)

    click.echo(str(envimg))


# U-Boot envimg: Update U-Boot environment variables
@cli.command(short_help="Update U-Boot environment variables")
@click.option('-f', '--fenv', type=click.Path(exists=True), help="The file with environment variables")
@click.option('-e', '--env', type=click.STRING, multiple=True, help="Environment variables")
@click.argument('mark', nargs=1, type=click.STRING)
@click.argument('file', nargs=1, type=click.Path(exists=True))
def update(env, mark, file, fenv=None):
    """ Update U-Boot environment variables """
    changed = False

    try:
        envimg = uboot.EnvImgOld(start_string=mark)
        envimg.open_img(file)

        if fenv is not None:
            changed = True
            with open(fenv, 'r') as f:
                envimg.load(f.read())

        if env:
            changed = True
            for var in env:
                name, value = var.split('=', 1)
                envimg.set(name.strip(), value.strip())

        if changed:
            envimg.save_img(file)

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)

    click.echo(str(envimg))


# U-Boot envimg: Replace U-Boot environment variables
@cli.command(short_help="Replace U-Boot environment variables")
@click.argument('mark', nargs=1, type=click.STRING)
@click.argument('file', nargs=1, type=click.Path(exists=True))
@click.argument('fenv', nargs=1, type=click.Path(exists=True))
def replace(mark, file, fenv):
    """ Replace U-Boot environment variables """
    try:
        envimg = uboot.EnvImgOld(start_string=mark)
        envimg.open_img(file)
        envimg.clear()

        with open(fenv, 'r') as f:
            envimg.load(f.read())

        envimg.save_img(file)

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)

    click.echo(str(envimg))


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
