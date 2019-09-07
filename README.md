<img src="documentation/ArtemisLogoSmall.png" align="right" />

# ARTEMIS 3 ![LICENSE](https://img.shields.io/github/license/AresValley/Artemis.svg?style=flat-square) ![ISSUE](https://img.shields.io/github/issues/AresValley/Artemis.svg?style=flat-square) ![LANGUAGE](https://img.shields.io/github/languages/top/AresValley/Artemis.svg?style=flat-square)

*Radio Signals Recognition Manual*

## ARTEMIS. In a nutshell.

In short, ARTEMIS is a signals hunter software and a useful aid for radio listeners! The analysis of real-time spectra (from your SDR, for instance) is made simple: you can take advantage using one of the largest RF signal database (with over 370 records). Compare several signals properties (such as frequency, bandwidth, modulation, etc.) and verify what you are searching for through a waterfall/audio sample. A collection of filters allows you to narrow your search, making the identification of unknown signals, odd buzzes or weird noises way easier.

## Table of contents

  - [Run the software](#Run-the-software)
    - [Run from binary](#Run-from-binary)
    - [Run from source code](#Run-from-source-code)
    - [Compile from source code](#Compile-from-source-code)
  - [Database](#database)
    - [Syntax](#syntax)
    - [Multiple Items fields (Location, Modulation)](#multiple-items-fields-location-modulation)
  - [Themes](#themes)
  - [License](#license)
  - [Thanks](#thanks)

## Run the software

Artemis 3 is entirely written in Python, so if you already have Python 3.7.0+ installed in your system, you can directly run the main script. Otherwise you can download a binary executable (see below).

### Run from binary
**If you don't know what you want or you are not sure where to look, this is for you.** 

Basically, this is the easiest, smooth, and clean way to run Artemis 3. A Python installation is not required.
For more information, follow [the main page of Artemis 3](https://aresvalley.com/artemis/) (detailed documentation at the end of the main page)

### Run from source code
Run the software from the source code with the Python interpreter is the simplest and natural way to run Artemis 3. Requirements:
- Python (ver. 3.7.0+)
- Python libraries (in `requirements/requirements.txt`)

1. Download and install Python (ver. 3.7.0+) from the official [website](https://www.python.org/downloads/). Be sure to select the flag `Add Python 3.x to PATH` during the first part of the installation.

2. Install the necessary Python libraries with PIP. Open a console in Artemis/requirements folder and type:
   
```
pip install -r  requirements.txt --user
```

3. After that launch the software in the Artemis folder with:
   
```
python3 artemis.py
```

### Compile from source code
If you want to compile Artemis yourself from the source code follow the instructions in the [spec_files/README](spec_files/README.md) file.

## Database

The database (db.csv) is directly extracted from sigidwiki.com with a DB parser and reworked to a standard format defined as follow. Artemis DB is a human-readable csv file where the delimiter is the character `*` (Asterisk, Unicode: U+002A). The new entry (separation between signals) is the End Of Line (EOL) escape sequence `\n`. Every signal is directly connected to spectra and audio sample stored in **Spectra** and **Audio** folders, respectively. Every signal is composed of 12 columns:

| Column | Description | Unit of Measurement | Multiple Items | Type|
| :-: | :-: | :-: | :-: | :-: |
| 1 | Signal name | - | - | string |
| 2 | Freq. Lower Limit | Hz | - | integer |
| 3 | Freq. Upper Limit | Hz  | - | integer |
| 4 | Mode | - | - | string |
| 5 | Band. Lower Limit | Hz | - | integer |
| 6 | Band. Upper Limit | Hz | - | integer |
| 7 | Location | - | ✔ | string |
| 8 | sigidwiki URL | - | - | string |
| 9 | Description | - | - | string |
| 10 | Modulation | - | ✔ | string |
| 11 | ID Code | - | - | integer |
| 12 | Auto-correlation function | ms | - | string |

### Syntax

1. **Signal Name**: The name of the signal. A simple string that describes in short the analyzed signal. Special characters are allowed (except the main delimiter `*`).
2. **Frequency (Lower Limit)**: The frequency lower bound expressed in Hertz.
3. **Frequency (Upper Limit)**: The same as above but this express the frequency upper bound of the received signal.
   
   * In the case of a single frequency transmitter/service the **Freq. Lower Limit** and the **Freq. Upper Limit** must be coincident (same value)
   * Transmission with different protocols must be added in two or more distinct entry. **DO NOT USE** the same signal page to add different transmission protocols (with different frequencies, bandwidth, modes,...). For example, NOAA-19 satellite transimit images and data with two different protocols:
     
     *  APT (Analog): 137.1000 MHz - 137.3125 MHz
     *  HRPT (Digital): 1698 MHz - 1707 MHz
   
      Add two separate entry (APT and HRPT) with the correct Lower and Upper bound frequency. **DO NOT ADD** a single signal entry with a Freq. Lower Bound of 137.100 MHz and the Upper Bound of 1707 MHz.

4. **Mode**: This field reports the way how a signals has been decoded during the reception.
5. **Bandwidth (Lower Limit)**: As reported above for frequency (points 2 and 3). Also here the value is reported in Hz.
6. **Bandwidth (Upper Limit)**: As reported above for frequency (points 2 and 3).
7. **Location**: This is the location where the signal is distributed/received. Avoid the usage of the precise location of the TX station or very small town (very rare). It's a good habit to use nations/continents or special location (worldwide). 
8. **sigidiwki URL**: The sigidwiki URL of the selected signal. This is a direct connection to the online database where further details of the signal are collected.
9.  **Description**: The short description is used to explain the purpose of the signal and some other useful details.
10. **Modulation**: The modulation is the way how the information have been encoded into the main signal (carrier). Several modification of the properties (Amplitude, Frequecy, ...) are possible and a tx station could transmit with different modulations.
11. **ID Code**: The category code, known as ID Code, is a sequence of 0/1 and its main purpose is to assign the signal to their families/categories. It's formed by 17 digits:

    |1|2|3|4|5|6|7|8|9|10|
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | Military | Radar | Active | Inactive | HAM | Commercial | Aviation | Marine | Analogue | Digital|

    |11|12|13|14|15|16|17|
    |:-:|:-:|:-:|:-:|:-:|:-:|:-:|
    | Trunked | Utility | Sat | Navigation | Interfering | Number Stations | Time Signal |

12. **Auto-correlation funtion (ACF)**: The ACF is an awesome discriminator when the signal is composed of redundant pattern that continouosly repeats. It is reported in **ms**. An extended description with an example signal analysis is available here: https://aresvalley.com/documentation/

### Multiple Items fields (Location, Modulation)
The necessity to manage a multiple Location/Modulation search pushed us to implement a fictitious 'secondary delimiter' chosen to be the `;` character. For instance:

```
Band. Upper Limit * Location 1 ; Location 2 ; ... * sigidwiki URL
```
or
```
Description * Modulation 1 ; Modulation 2 ; ... * ID Code
```

## Themes
The only folder with the pre-built package is the `themes` one. In this way the themes are fully customizable and you can add your own. New themes (in the `themes` folder) will appear automatically in the main menu and the last used theme will be saved as the favorite one (a restart of Artemis will use the last used theme).

Some of the available themes were adapted from https://github.com/GTRONICK/QSS.

## License
This program (ARTEMIS 3, 2014-2019) is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see: www.gnu.org/licenses

## Thanks
* **Marco Dalla Tiezza** - *Artemis I-II developer, DB parsing, Website*
* [**Alessandro Ceccato**](https://github.com/alessandro90 "GitHub profile") - *Artemis III lead developer*
* **Paolo Romani (IZ1MLL)** - *Lead β Tester, RF specialist*
* **Carl Colena** - *Sigidwiki admin, β Tester, Signals expert*
* **Marco Bortoli** - *macOS deployment, β Tester*
* **Pierpaolo Pravatto** - *Wiki page, β Tester*
* **Francesco Capostagno, Luca, Pietro** - *β Tester*
