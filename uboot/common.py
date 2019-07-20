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


from easy_enum import Enum

# ----------------------------------------------------------------------------------------------------------------------
# Image Types
# ----------------------------------------------------------------------------------------------------------------------

# "Standalone Programs" are directly runnable in the environment
#   provided by U-Boot; it is expected that (if they behave
#   well) you can continue to work in U-Boot after return from
#   the Standalone Program.

# "OS Kernel Images" are usually images of some Embedded OS which
#   will take over control completely. Usually these programs
#   will install their own set of exception handlers, device
#   drivers, set up the MMU, etc. - this means, that you cannot
#   expect to re-enter U-Boot except by resetting the CPU.

# "RAMDisk Images" are more or less just data blocks, and their
#   parameters (address, size) are passed to an OS kernel that is
#   being started.

# "Multi-File Images" contain several images, typically an OS
#   (Linux) kernel image and one or more data images like
#   RAMDisks. This construct is useful for instance when you want
#   to boot over the network using BOOTP etc., where the boot
#   server provides just a single image file, but you want to get
#   for instance an OS kernel and a RAMDisk image.

# "Firmware Images" are binary images containing firmware (like
#   U-Boot or FPGA images) which usually will be programmed to
#   flash memory.

# "Script files" are command sequences that will be executed by
#   U-Boot's command interpreter; this feature is especially
#   useful when you configure U-Boot to use a real shell (hush)
#   as command interpreter (=> Shell Scripts).

# The following are exposed to uImage header.
# Do not change values for backward compatibility.


class EnumImageType(Enum):
    """ Supported UBoot Image Types """

    STANDALONE = (1, "standalone", "Standalone Program")
    KERNEL = (2, "kernel", "Kernel Image")
    RAMDISK = (3, "ramdisk", "RAMDisk Image")
    MULTI = (4, "multi", "Multi-File Image")
    FIRMWARE = (5, "firmware", "Firmware Image")
    SCRIPT = (6, "script", "U-Boot Script Image")
    FILESYSTEM = (7, "filesystem", "Filesystem Image")
    FLATDT = (8, "flat_dt", "Flat Device Tree Image")
    KWB = (9, "kwbimage", "Kirkwood Boot Image")
    IMX = (10, "imximage", "Freescale i.MX Boot Image")
    UBL = (11, "ublimage", "Davinci UBL image")
    OMAP = (12, "omapimage", "TI OMAP SPL With GP CH")
    AIS = (13, "aisimage", "Davinci AIS image")

    KNOLOAD = (14, "kernel_noload", "Kernel Image (no loading done)")
    PBL = (15, "pblimage", "Freescale PBL Boot Image")
    MXS = (16, "mxsimage", "Freescale MXS Boot Image")
    GP = (17, "gpimage", "TI Keystone SPL Image")
    ATMEL = (18, "atmelimage", "ATMEL ROM-Boot Image")
    SOCFPGA = (19, "socfpgaimage", "Altera SOCFPGA preloader")
    X86SETUP = (20, "x86_setup", "x86 setup.bin")
    LPC32XX = (21, "lpc32xximage", "LPC32XX Boot Image")
    LOADABLE = (22, "loadable", "A list of typeless images")
    RKBOOT = (23, "rkimage", "Rockchip Boot Image")
    RKSD = (24, "rksd", "Rockchip SD Boot Image")
    RKSPI = (25, "rkspi", "Rockchip SPI Boot Image")
    ZYNQ = (26, "zynqimage", "Xilinx Zynq Boot Image")
    ZYNQMP = (27, "zynqmpimage", "Xilinx ZynqMP Boot Image")
    FPGA = (28, "fpga", "FPGA Image")
    VYBRID = (29, "vybridimage", "Vybrid Boot Image")
    TEE = (30, "tee", "Trusted Execution Environment Image")
    FW_IVT = (31, "firmware_ivt", "Firmware with HABv4 IVT")
    PMMC = (32, "pmmc", "TI Power Management Micro-Controller Firmware")


# ----------------------------------------------------------------------------------------------------------------------
# Operating System Codes
# ----------------------------------------------------------------------------------------------------------------------

# The following are exposed to uImage header.
# Do not change values for backward compatibility.

class EnumOsType(Enum):
    """ Supported Operating Systems """

    OPENBSD = (1, "openbsd", "OpenBSD")
    NETBSD = (2, "netbsd", "NetBSD")
    FREEBSD = (3, "freebsd", "FreeBSD")
    BSD4 = (4, "4-4bsd", "4-4BSD")
    LINUX = (5, "linux", "Linux")
    SVR4 = (6, "svr4", "SVR4")
    ESIX = (7, "esix", "Esix")
    SOLARIS = (8, "solaris", "Solaris")
    IRIX = (9, "irix", "Irix")
    SCO = (10, "sco", "SCO")
    DELL = (11, "dell", "Dell")
    NCR = (12, "ncr", "NCR")
    LYNXOS = (13, "lynxos", "LynxOS")
    VXWORKS = (14, "vxworks", "VxWorks")
    PSOS = (15, "psos", "pSOS")
    QNX = (16, "qnx", "QNX")
    UBOOT = (17, "u-boot", "U-Boot Firmware")
    RTEMS = (18, "rtems", "RTEMS")
    ARTOS = (19, "artos", "ARTOS")
    UNITY = (20, "unity", "Unity OS")
    INTEGRITY = (21, "integrity", "INTEGRITY")
    OSE = (22, "ose", "Enea OSE")
    PLAN9 = (23, "plan9", "Plan 9")
    OPENRTOS = (24, "openrtos", "OpenRTOS")


# ----------------------------------------------------------------------------------------------------------------------
# CPU Architecture Codes (supported by Linux)
# ----------------------------------------------------------------------------------------------------------------------

# The following are exposed to uImage header.
# Do not change values for backward compatibility.

class EnumArchType(Enum):
    """ Supported CPU Architectures """

    ALPHA = (1, "alpha", "Alpha")
    ARM = (2, "arm", "ARM")
    I386 = (3, "x86", "Intel x86")
    IA64 = (4, "ia64", "IA64")
    MIPS = (5, "mips", "MIPS")
    MIPS64 = (6, "mips64", "MIPS 64-Bit")
    PPC = (7, "powerpc", "PowerPC")
    S390 = (8, "s390", "IBM S390")
    SH = (9, "sh", "SuperH")
    SPARC = (10, "sparc", "SPARC")
    SPARC64 = (11, "sparc64", "SPARC 64 Bit")
    M68K = (12, "m68k", "M68K")
    NIOS = (13, "nios", "Nios 32")
    MICROBLAZE = (14, "microblaze", "MicroBlaze")
    NIOS2 = (15, "nios2", "NIOS II")
    BLACKFIN = (16, "blackfin", "Blackfin")
    AVR32 = (17, "avr32", "AVR32")
    ST200 = (18, "ST200", "STMicroelectronics ST200")
    SANDBOX = (19, "sandbox", "Sandbox architecture (test only)")
    NDS32 = (20, "nds32", "ANDES Technology - NDS32")
    OPENRISC = (21, "or1k", "OpenRISC 1000")
    ARM64 = (22, "arm64", "AArch64")
    ARC = (23, "arc", "Synopsis DesignWare ARC")
    X86_64 = (24, "x86_64", "AMD x86_64, Intel and Via")
    XTENSA = (25, "xtensa", "Xtensa")


# ----------------------------------------------------------------------------------------------------------------------
# Compression Types
# ----------------------------------------------------------------------------------------------------------------------

# The following are exposed to uImage header.
# Do not change values for backward compatibility.

class EnumCompressionType(Enum):
    """ Supported Data Compression """

    NONE = (0, 'none', 'Uncompressed')
    GZIP = (1, 'gzip', 'Compressed with GZIP')
    BZIP2 = (2, 'bzip2', 'Compressed with BZIP2')
    LZMA = (3, 'lzma', 'Compressed with LZMA')
    LZO = (4, 'lzo', 'Compressed with LZO')
    LZ4 = (5, 'lz4', 'Compressed with LZ4')
