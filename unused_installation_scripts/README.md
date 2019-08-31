<img src="../documentation/ArtemisLogoSmall.png" align="right" />

# ARTEMIS 3 ![LICENSE](https://img.shields.io/github/license/AresValley/Artemis.svg?style=flat-square) ![ISSUE](https://img.shields.io/github/issues/AresValley/Artemis.svg?style=flat-square) ![LANGUAGE](https://img.shields.io/github/languages/top/AresValley/Artemis.svg?style=flat-square)

*Radio Signals Recognition Manual*

## ARTEMIS 3 - Unused Deployment Scripts

This folder contains a third option to run Artemis 3 on your pc. The method of installation is based on an automatic script that set privileges, install dependencies and create a working shortcut to your desktop/menu.

**For the sake of completeness, the documentation is available below, but we strongly discourage any attempt to use it.**

## Run using deploy script

<img src="../documentation/win.png" align="right" />

> ### Windows:
>
> 1. Windows don't offer a native version of Python. Download and install Python 3 (> 3.7) from the official website (https://www.python.org/downloads/). Be sure to select the flag `Add Python 3.x to PATH` during the first part of the installation. To verify the correct installation of Python open a CMD terminal (Open the **run** windows with **Win+R** and type **cmd**) and check the version of the just installed python 3 with:
> ```
> python --version
> ```
> 2. Use the `clone or download` button (https://github.com/AresValley/Artemis/archive/master.zip) to download the source code of Artemis 3.
> 3. Extract the .zip and place Artemis folder where you prefer. The code must always be accompanied by a `themes` folder.
> 4. To install the necessary libraries open the `Artemis/deploy/Windows` folder. Run (with a double click) the script `deploy_win.bat`. The script will:
> 
>     * Set the correct read/write privileges for Artemis folder. The main folder **must have the reading/writing permission** to download the Signals Database.
>     * Install the required Python 3 libraries with pip3.
>     * Generate a .pyw file (script launcher without console), and it will create a shortcut on the desktop.


<img src="../documentation/linux.png" align="right" />

> ### Linux:
>
> 1. Linux already offers a native version of python on board. Please verify the presence of Python 3 and check the version (> 3.7) opening a terminal and typing:
> ```
> python --version
> ```
> If, for some reasons python, it is not present in your system follow the specific instructions to install it on your distro. For the common Linux OS:
> * **Ubuntu**, **Mint**: `sudo apt-get install python3.7`  
> * **Fedora**: `sudo dnf install python37` 
> 2. Use the `clone or download` button (https://github.com/AresValley/Artemis/archive/master.zip) to download the source code of Artemis 3.
> 3. Extract the .zip where you like (use `unzip Artemis-master.zip`). The code must always be accompanied by a `themes` folder.
> 4. To install the necessary libraries open the `Artemis/deploy/Linux` folder. Run the script `deploy_linux.sh` typing in a terminal:
> ```
> cd PATH / TO / ARTEMIS / FOLDER /deploy/Linux
> sh deploy_linux.sh
> ```
> 
> 5. Follow the terminal instructions. At the end, you will find a shortcut to Artemis 3 in the main menu. The script `deploy_linux.sh` will:
> 
>     * Set the correct read/write privileges for Artemis folder. The main folder **must have the reading/writing permission** to download the Signals Database.
>     * Install the required Python 3 libraries with pip3.
>     * Generate a .desktop file (script launcher without console) in `$HOME/.local/share/applications` and it will copy the .svg Artemis icon in `/usr/share/icons/`.


<img src="../documentation/apple.png" align="right" />

> ### MacOS:
>
> 1. To Be Completed...

## License
This program (ARTEMIS 3, 2014-2019) is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see: www.gnu.org/licenses

## Thanks
* **Marco Dalla Tiezza** - *Artemis I-II developer, DB parsing, Website*
* [**Alessandro Ceccato**](https://github.com/alessandro90 "GitHub profile") - *Artemis III lead developer*
* **Paolo Romani (IZ1MLL)** - *Lead β Tester, RF specialist*
* **Carl Colena** - *Sigidwiki admin, β Tester, Signals expert*
* [**Marco Bortoli**](https://github.com/marbort "GitHub profile") - *macOS deployment, β Tester*
* [**Pierpaolo Pravatto**](https://github.com/ppravatto "GitHub profile") - *Wiki page, β Tester*
* [**Francesco Capostagno**](https://github.com/fcapostagno "GitHub profile"), **Luca**, **Pietro** - *β Tester*
