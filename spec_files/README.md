<img src="../documentation/ArtemisLogoSmall.png" align="right" />

# ARTEMIS 3 ![LICENSE](https://img.shields.io/github/license/AresValley/Artemis.svg?style=flat-square) ![ISSUE](https://img.shields.io/github/issues/AresValley/Artemis.svg?style=flat-square) ![LANGUAGE](https://img.shields.io/github/languages/top/AresValley/Artemis.svg?style=flat-square)

*Radio Signals Recognition Manual*

## ARTEMIS 3 .SPEC FILES

Artemis 3 .spec files are used by the package **pyinstaller** (https://www.pyinstaller.org/) to build a single standalone executable (or a one-dir package). Every external dependency is already embedded into the bundle. The interpreter of Python 3 is also included.

## Requirements
- Python 3.7.0+
- Pyinstaller

**IMPORTANT:** *To generate the standalone and the one-dir package, you must use an operating system that coincides with the target one (pyinstaller doesn't allow cross-compilation).* 

**IMPORTANT (LINUX COMPILING):** *The executable that PyInstaller builds is not fully static, in that it still depends on the system libc. **Under Linux, the ABI of GLIBC is backward compatible, but not forward compatible. So if you link against a newer GLIBC, you can't run the resulting executable on an older system**. The supplied binary bootloader should work with older GLIBC. However, the libpython.so and other dynamic libraries still depend on the newer GLIBC. The solution is to compile the Python interpreter with its modules (and also probably bootloader) on the oldest system you have around so that it gets linked with the oldest version of GLIBC.* (Source: PyInstaller)

**NOTE.** Depending on the number of packages installed in your python environemnt, the size of the executables file can vary significantly. In order to get the smallest size possible it is recommend to initialize a fresh virtual environment with just the requirements and pyinstaller.

## Package Building (standalone aka one-file, high portability, **suggested**)
1. Download/clone the git repository.
2. In the `spec_files/<your OS>` folder open a terminal and type
```
pyinstaller Artemis.spec
```
3. An Artemis executable should be produced in the `dist/` folder. The `build/` folder
   can be deleted.

## Package Building (one-dir, shorter startup time, low portability)
1. Download/clone the git repository.
2. In the `spec_files/<your OS>` folder open a terminal and type
```
pyinstaller Artemis_onedir.spec
```
3. An Artemis executable should be produced in  `dist/Artemis/`. The `build/` can
   be deleted.


You can save a copy of the executable in a folder of you choice. At startup it will ask you to download the database and also warn you that the `themes` folder is missing. To avoid this, copy `src/Data` and `src/themes` in the folder containing the executable.

## Build scripts
Provided you satisfy the requirements (see [requirements.txt](../requirements/requirements.txt)) and have pyinstaller installed, running a `build.*` script in `<your os>` folder will produce an `output` folder with:

- Executable versions of Artemis and the updater;
  - compressed versions of the same files;
- a folder called `Artemis/` containing the executables and the `theme` folder
  - a compressed version of the folder

At the end of the process the script writes on standard output the size and sha256 code for the compressed files.

**NOTE.** For Windows you will need a 7z installation. Also check the path hardcoded in `/Windows/build.bat`.