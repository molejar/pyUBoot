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


# ----------------------------------------------------------------------------------------------------------------------
# Enum Class
# ----------------------------------------------------------------------------------------------------------------------
class Enum(object):
    @classmethod
    def validate(cls, value):
        for item in cls._nfo:
            if isinstance(value, str) and value == item[1]:
                return True
            elif value == item[0]:
                return True
        return False

    @classmethod
    def value(cls, name):
        if not isinstance(name, str):
            raise Exception("Item name must be a string type !")
        for item in cls._nfo:
            if name == item[1]:
                return item[0]
        raise ValueError("Unsupported name: %s" % name)

    @classmethod
    def all_values(cls):
        return [item[0] for item in cls._nfo]

    @classmethod
    def name(cls, value):
        for item in cls._nfo:
            if value == item[0]:
                return item[1]
        return "0x{0:08X}".format(value)

    @classmethod
    def all_names(cls):
        return [item[1] for item in cls._nfo]

    @classmethod
    def desc(cls, value):
        for item in cls._nfo:
            if isinstance(value, str) and value == item[1]:
                return item[2]
            elif value == item[0]:
                return item[2]

    @classmethod
    def all_descs(cls):
        return [item[3] for item in cls._nfo]
# ----------------------------------------------------------------------------------------------------------------------

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
    """ Header: Supported UBoot Image Types """
    STANDALONE = 1  # Standalone Image
    KERNEL = 2  # Kernel Image
    RAMDISK = 3  # RamDisk Image
    MULTI = 4  # Multi-File Image
    FIRMWARE = 5  # Firmware Image
    SCRIPT = 6  # U-Boot Script Image
    FILESYSTEM = 7  # Filesystem Image
    FLATDT = 8  # Flat Device Tree Image
    KWB = 9  # Kirkwood Boot Image
    IMX = 10  # Freescale IMXBoot Image
    UBL = 11  # Davinci UBL Image
    OMAP = 12  # TI OMAP Config Header Image
    AIS = 13  # TI Davinci IS Image

    KNOLOAD = 14  # OS Kernel Image, can run from any load address
    PBL = 15  # Freescale PBL Boot Image
    MXS = 16  # Freescale MXS Boot Image
    GP = 17  # TI Keystone GP-Header Image
    ATMEL = 18  # ATMEL ROM bootable Image
    SOCFPGA = 19  # Altera SOCFPGA Preloader
    X86SETUP = 20  # x86 setup.bin Image
    LPC32XX = 21  # -
    LOADABLE = 22  # A list of typeless images
    RKBOOT = 23  # Rockchip Boot Image
    RKSD = 24  # Rockchip SD card
    RKSPI = 25  # Rockchip SPI image
    ZYNQ = 26  # Xilinx Zynq Boot Image
    ZYNQMP = 27  # Xilinx ZynqMP Boot Image
    FPGA = 28  # FPGA Image
    VYBRID = 29  # VYBRID.vyb Image
    TEE = 30  # Trusted Execution Environment OS Image
    FW_IVT = 31  # Firmware Image with HABv4 IVT
    PMMC = 32  # TI Power Management Micro-Controller Firmware

    _nfo = (
        # Flag  |  Name  | Description
        (AIS, "aisimage", "Davinci AIS image"),
        (FILESYSTEM, "filesystem", "Filesystem Image"),
        (FIRMWARE, "firmware", "Firmware"),
        (FLATDT, "flat_dt", "Flat Device Tree"),
        (GP, "gpimage", "TI Keystone SPL Image"),
        (KERNEL, "kernel", "Kernel Image"),
        (KNOLOAD, "kernel_noload", "Kernel Image (no loading done)"),
        (KWB, "kwbimage", "Kirkwood Boot Image"),
        (IMX, "imximage", "Freescale i.MX Boot Image"),
        (MULTI, "multi", "Multi-File Image"),
        (OMAP, "omapimage", "TI OMAP SPL With GP CH"),
        (PBL, "pblimage", "Freescale PBL Boot Image"),
        (RAMDISK, "ramdisk", "RAMDisk Image"),
        (SCRIPT, "script", "Script"),
        (SOCFPGA, "socfpgaimage", "Altera SOCFPGA preloader"),
        (STANDALONE, "standalone", "Standalone Program"),
        (UBL, "ublimage", "Davinci UBL image"),
        (MXS, "mxsimage", "Freescale MXS Boot Image"),
        (ATMEL, "atmelimage", "ATMEL ROM-Boot Image"),
        (X86SETUP, "x86_setup", "x86 setup.bin"),
        (LPC32XX, "lpc32xximage", "LPC32XX Boot Image"),
        (RKBOOT, "rkimage", "Rockchip Boot Image"),
        (RKSD, "rksd", "Rockchip SD Boot Image"),
        (RKSPI, "rkspi", "Rockchip SPI Boot Image"),
        (VYBRID, "vybridimage", "Vybrid Boot Image"),
        (ZYNQ, "zynqimage", "Xilinx Zynq Boot Image"),
        (ZYNQMP, "zynqmpimage", "Xilinx ZynqMP Boot Image"),
        (FPGA, "fpga", "FPGA Image"),
        (TEE, "tee", "Trusted Execution Environment Image"),
        (FW_IVT, "firmware_ivt", "Firmware with HABv4 IVT"),
        (PMMC, "pmmc", "TI Power Management Micro-Controller Firmware"),
    )


# ----------------------------------------------------------------------------------------------------------------------
# Operating System Codes
# ----------------------------------------------------------------------------------------------------------------------

# The following are exposed to uImage header.
# Do not change values for backward compatibility.

class EnumOsType(Enum):
    """ Header: Supported Operating Systems """
    OPENBSD = 1  # OpenBSD
    NETBSD = 2  # NetBSD
    FREEBSD = 3  # FreeBSD
    BSD4 = 4  # 4-4BSD
    LINUX = 5  # Linux
    SVR4 = 6  # SVR4
    ESIX = 7  # Esix
    SOLARIS = 8  # Solaris
    IRIX = 9  # Irix
    SCO = 10  # SCO
    DELL = 11  # Dell
    NCR = 12  # NCR
    LYNXOS = 13  # LynxOS
    VXWORKS = 14  # VxWorks
    PSOS = 15  # pSOS
    QNX = 16  # QNX
    UBOOT = 17  # Firmware
    RTEMS = 18  # RTEMS
    ARTOS = 19  # ARTOS
    UNITY = 20  # Unity OS
    INTEGRITY = 21  # INTEGRITY
    OSE = 22  # OSE
    PLAN9 = 23  # Plan 9
    OPENRTOS = 24  # OpenRTOS

    _nfo = (
        # Flag  |  Name  | Description
        (LINUX, "linux", "Linux"),
        (LYNXOS, "lynxos", "LynxOS"),
        (NETBSD, "netbsd", "NetBSD"),
        (OSE, "ose", "Enea OSE"),
        (PLAN9, "plan9", "Plan 9"),
        (RTEMS, "rtems", "RTEMS"),
        (UBOOT, "u-boot", "U-Boot"),
        (VXWORKS, "vxworks", "VxWorks"),
        (QNX, "qnx", "QNX"),
        (INTEGRITY, "integrity", "INTEGRITY"),
        (BSD4, "4-4bsd", "4-4BSD"),
        (DELL, "dell", "Dell"),
        (ESIX, "esix", "Esix"),
        (FREEBSD, "freebsd", "FreeBSD"),
        (IRIX, "irix", "Irix"),
        (NCR, "ncr", "NCR"),
        (OPENBSD, "openbsd", "OpenBSD"),
        (PSOS, "psos", "pSOS"),
        (SCO, "sco", "SCO"),
        (SOLARIS, "solaris", "Solaris"),
        (SVR4, "svr4", "SVR4"),
        (OPENRTOS, "openrtos", "OpenRTOS"),
    )


# ----------------------------------------------------------------------------------------------------------------------
# CPU Architecture Codes (supported by Linux)
# ----------------------------------------------------------------------------------------------------------------------

# The following are exposed to uImage header.
# Do not change values for backward compatibility.

class EnumArchType(Enum):
    """ Header: Supported CPU Architectures """
    ALPHA = 1  # Alpha
    ARM = 2  # ARM
    I386 = 3  # Intel x86
    IA64 = 4  # IA64
    MIPS = 5  # MIPS
    MIPS64 = 6  # MIPS 64 Bit
    PPC = 7  # PowerPC
    S390 = 8  # IBM S390
    SH = 9  # SuperH
    SPARC = 10  # Sparc
    SPARC64 = 11  # Sparc 64 Bit
    M68K = 12  # M68K
    NIOS = 13  # Nios - 32
    MICROBLAZE = 14  # MicroBlaze
    NIOS2 = 15  # Nios - II
    BLACKFIN = 16  # Blackfin
    AVR32 = 17  # AVR32
    ST200 = 18  # STMicroelectronics ST200
    SANDBOX = 19  # Sandbox architecture (test only)
    NDS32 = 20  # ANDES Technology - NDS32
    OPENRISC = 21  # OpenRISC 1000
    ARM64 = 22  # ARM64
    ARC = 23  # Synopsis DesignWare ARC
    X86_64 = 24  # AMD x86_64, Intel and Via
    XTENSA = 25  # Xtensa

    _nfo = (
        # Flag  |   Name   | Description
        (ALPHA, "alpha", "Alpha"),
        (ARM, "arm", "ARM"),
        (I386, "x86", "Intel x86"),
        (IA64, "ia64", "IA64"),
        (M68K, "m68k", "M68K"),
        (MICROBLAZE, "microblaze", "MicroBlaze"),
        (MIPS, "mips", "MIPS"),
        (MIPS64, "mips64", "MIPS 64-Bit"),
        (NIOS2, "nios2", "NIOS II"),
        (PPC, "powerpc", "PowerPC"),
        (PPC, "ppc", "PowerPC"),
        (S390, "s390", "IBM S390"),
        (SH, "sh", "SuperH"),
        (SPARC, "sparc", "SPARC"),
        (SPARC64, "sparc64", "SPARC 64 Bit"),
        (BLACKFIN, "blackfin", "Blackfin"),
        (AVR32, "avr32", "AVR32"),
        (NDS32, "nds32", "NDS32"),
        (OPENRISC, "or1k", "OpenRISC 1000"),
        (SANDBOX, "sandbox", "Sandbox"),
        (ARM64, "arm64", "AArch64"),
        (ARC, "arc", "ARC"),
        (X86_64, "x86_64", "AMD x86_64"),
        (XTENSA, "xtensa", "Xtensa"),
    )


# ----------------------------------------------------------------------------------------------------------------------
# Compression Types
# ----------------------------------------------------------------------------------------------------------------------

# The following are exposed to uImage header.
# Do not change values for backward compatibility.

class EnumCompressionType(Enum):
    """ Header: Supported Data Compression """
    NONE = 0
    GZIP = 1
    BZIP2 = 2
    LZMA = 3
    LZO = 4
    LZ4 = 5

    _nfo = (
        # Flag  |  Name  | Description
        (NONE, "none", "uncompressed"),
        (GZIP, "gzip", "gzip compressed"),
        (BZIP2, "bzip2", "bzip2 compressed"),
        (LZMA, "lzma", "lzma compressed"),
        (LZO, "lzo", "lzo compressed"),
        (LZ4, "lz4", "lz4 compressed"),
    )
