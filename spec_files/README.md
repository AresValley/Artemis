<img src="../documentation/ArtemisLogoSmall.png" align="right" />

# ARTEMIS 3 ![LICENSE](https://img.shields.io/github/license/AresValley/Artemis.svg?style=flat-square) ![ISSUE](https://img.shields.io/github/issues/AresValley/Artemis.svg?style=flat-square) ![LANGUAGE](https://img.shields.io/github/languages/top/AresValley/Artemis.svg?style=flat-square)

*Radio Signals Recognition Manual*

## ARTEMIS 3 .SPEC FILES

Artemis 3 .spec files are used by the package **pyinstaller** (https://www.pyinstaller.org/) to build a single standalone executable. The extreme versatility of this package is the fact that every external dependency is already embedded into the bundle. The interpreter of Python 3 is also included.

## Requirements
- Python 3.7.0+
- Pyinstaller

## Package Building
**IMPORTANT:** *To generate the standalone, you must use an operating system that coincides with the target one (pyinstaller doesn't allow cross-compilation).* 
1. Download a fresh copy of the git repository.
2. Choose the target OS in `spec_files` folder and copy the whole content into `src`
3. Open a terminal into `src` and run:
```
pyinstaller Artemis.spec
```
4. The ready-to-use compiled software is now present into `src/dist` folder.

## License
This program (ARTEMIS 3, 2014-2019) is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see: www.gnu.org/licenses

## Thanks
* **Marco D.T.** - *Artemis I-II programmer, DB parsing, Website*
* **Alessandro C.** - *Artemis III lead programmer*
* **Paolo R. (IZ1MLL)** - *Lead β Tester, RF specialist*
* **Carl C.** - *Sigidwiki admin, β Tester, Signals expert*
* **Marco B.** - *macOS deployment, β Tester*
* **Francesco C., Pierpaolo P., Luca XYZ, Paolo XYZ, Daniele XYZ** - *β Tester*
