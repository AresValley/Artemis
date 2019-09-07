<img src="../documentation/ArtemisLogoSmall.png" align="right" />

# ARTEMIS 3 ![LICENSE](https://img.shields.io/github/license/AresValley/Artemis.svg?style=flat-square) ![ISSUE](https://img.shields.io/github/issues/AresValley/Artemis.svg?style=flat-square) ![LANGUAGE](https://img.shields.io/github/languages/top/AresValley/Artemis.svg?style=flat-square)

*Radio Signals Recognition Manual*

## ARTEMIS 3 .SPEC FILES

Artemis 3 .spec files are used by the package **pyinstaller** (https://www.pyinstaller.org/) to build a single standalone executable (or a one-dir package). Every external dependency is already embedded into the bundle. The interpreter of Python 3 is also included.

## Requirements
- Python 3.7.0+
- Pyinstaller

**IMPORTANT:** *To generate the standalone and the one-dir package, you must use an operating system that coincides with the target one (pyinstaller doesn't allow cross-compilation).* 

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


You can save a copy of the executable in a folder of you choice. At startup it will ask you to download
the database and also warn you that the `themes` folder is missing. To avoid this,
copy `src/Data` and `src/themes` in the folder containing the executable.
