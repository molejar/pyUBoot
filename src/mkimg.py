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
            img = uboot.parse(f.read())
            click.echo(img.GetInfo())

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")


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
        imgtype = uboot.IMGType.StrToValue(imgtype)

        if len(infiles) > 1:
            data = []
            for file in infiles:
                with open(file, 'rb') as f:
                    data.append(f.read())
        else:
            rdf = 'r' if imgtype == uboot.IMGType.SCRIPT else 'rb'
            with open(infiles[0], rdf) as f:
                data = f.read()

        img = uboot.create(imgtype)
        img.ArchType = uboot.ARCHType.StrToValue(arch)
        img.OsType = uboot.OSType.StrToValue(ostype)
        img.Compression = uboot.COMPRESSType.StrToValue(compress)
        img.LoadAddress = laddr
        img.EntryPoint = epaddr
        img.Name = name
        img.Load(data)

        click.echo(img.GetInfo())
        with open(outfile, 'wb') as f:
            f.write(img.Export())

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")

    else:
        click.secho("\nCreated Image: %s" % outfile)


# U-Boot mkimg: Extract image content
@cli.command(short_help="Extract image content")
@click.argument('file',  nargs=1, type=click.Path(exists=True))
def extract(file):
    """ Extract image content """
    def Save(dest_dir, file_info, file_data, file_ext):
        os.makedirs(dest_dir, exist_ok=True)
        # Save info file
        fn = os.path.join(dest_dir, 'info.txt')
        with open(fn, 'w') as f:
            f.write(file_info)
        # Save data file
        fn = os.path.join(dest_dir, 'data.' + file_ext)
        with open(fn, 'w' if file_ext == 'txt' else 'wb') as f:
            f.write(file_data)

    def GetFileExt(header):
        ext_list = ('bin', 'gz', 'bz2', 'lzma', 'lzo', 'lz4')
        if header.ImageType == int(uboot.IMGType.SCRIPT):
            ext = 'txt'
        else:
            ext = ext_list[header.Compression]
        return ext

    try:
        file_path, file_name = os.path.split(file)
        out_path = os.path.normpath(os.path.join(file_path, file_name + ".extracted"))

        with open(file, 'rb') as f:
            raw_data = f.read()

        img = uboot.parse(raw_data)
        if img.ImageType == int(uboot.IMGType.MULTI):
            n = 0
            for item in img.Extract():
                dir_name = os.path.join(out_path, 'Image' + str(n))
                header = item[0]
                data = item[1]
                Save(dir_name, header.GetInfo(), data, GetFileExt(header))
                n += 1
        else:
            dir_name = out_path
            header, data = img.Extract()
            Save(dir_name, header.GetInfo(), data, GetFileExt(header))

    except Exception as e:
        click.echo(str(e) if str(e) else "Unknown Error !")

    else:
        click.secho("\nImage extracted into: %s" % out_path)


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
