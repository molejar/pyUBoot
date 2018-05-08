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


# U-Boot envimg: Export U-Boot environment variables
@cli.command(short_help="Export U-Boot environment variables")
@click.argument('mark', nargs=1, type=click.STRING)
@click.argument('file', nargs=1, type=click.Path(exists=True))
@click.argument('fenv', nargs=1, type=click.Path())
def export(mark, file, fenv):
    """ Export U-Boot environment variables """
    try:
        envimg = uboot.EnvImgOld(start_string=mark)
        envimg.open_img(file)

        with open(fenv, 'w') as f:
            f.write(envimg.store())

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")
        sys.exit(ERROR_CODE)

    click.secho("Environment variables saved into: %s" % fenv)


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
