# Changelog

> [!NOTE]  
> This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and the format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [4.0.5] - 2024-06-15

### Added
- Possibility to navigate Artemis just with the keyboard [#50](https://github.com/AresValley/Artemis/issues/50)
- **Windows:** automatic updates have been implemented. When a software update is available, Artemis will download the new version and install the updates automatically 
- Multiple sigID databases can be conserved. In the case of autoload, the latest local version will be loaded
- Added creation date and DB version in DB manager window

### Changed
- Improved readability of labels for filter ranges for frequency, bandwidth, and ACF
- Improved Update manager and Downloader functionalities
- OS-dependent temporary folders are now used for database download and Artemis updates
- The logic for searching the last sigID database has changed now the discriminant is no longer the folder name but is reported as a signature in the database itself (-1 in the editable field; see documentation)
- Old sigID databases are not deleted anymore when a new version is downloaded. This is to avoid removing databases with user changes or additions

### Fixed
- Added a database load check to avoid (noncritical) exceptions when applying filters without having loaded a database.
- Fixed a potential issue involving the forcible closure of the downloader window, but the downloader instance keeps running
- With the new logic in the latest sigID database search, manually imported sigID databases are officially recognized as proper ones

## [4.0.3] - 2024-06-10

### Changed
- Optimized final package size (reduced by 30% to 50%) by explicitly including necessary plugins/DLLs and excluding unnecessary ones with Nuitka [#47](https://github.com/AresValley/Artemis/issues/47)

### Fixed
- When the links/urls in the description field of a signal are clicked, they open the default browser [#46](https://github.com/AresValley/Artemis/issues/46)
- Fixed an error occurig on Linux where configuration file path are not properly resolved during startup with the binary version of the program (they are if running from source) [#48](https://github.com/AresValley/Artemis/issues/48)

## [4.0.1] - 2024-06-9
### Added
- Database format has been changed from .csv to a proper relational DB (sqlite) which is much easier handled thanks to the native library shipped with python
- Possibility to create an arbitrary number of new databases for storing new custom signals
- Every signal allows an arbitrary number of parameters
- All signal parameters (such as frequency, modulation, location, etc.) are now followed by a description
- Databases can be exported/imported for easy sharing
- Possibility to store and view all type of documents related to a signal entry
- Filtration process is now much more efficient due to usage of SQL queries
- D-Region Absorption Predictions (DRAP) and Aurora OVATION model are now present in the Space Weather window

### Changed
- Updated GUI libray from PyQt5 to PySide6. Artemis 4 now relies on the QtQuick framework.
- SigID standard database is now hosted on GitHub (the server is much faster) along with the website parser
- Undefined value for frequency and bandwidth is now deprecated
- Drastically reduced the number of third party libraries
- The signals filtering page has been simplified to be more immediate and user friendly
- Space weather page has been greatly improved and now relies on Poseidon daemon (hosted on aresvalley.com)

### Fixed
- Artemis can be execunted inside standard pretected folder (such as Program Files) without using elevated privileges

## [3.2.4] - 2022-09-30
### Fixed
- Fixed crash on opening the Rx/Tx Condition tab

## [3.2.3] - 2022-09-29
### Added
- Add auto-packaging feature using GitHub actions for Windows OS (experimental)
### Fixed
- Fix crash for playing audio ([#34](https://github.com/AresValley/Artemis/pull/34))

## [3.2.2] - 2022-07-29
### Fixed
- Fixed crash on startup or if checking for updates without an internet connection ([#23](https://github.com/AresValley/Artemis/pull/23))
- Updated dependencies for security reasons (urllib3) and to address the main application failure to launch under certain conditions.

## [3.2.1] - 2020-04-25
### Added
- Add some basic logging to the application. Also for severe errors, track them in info.log file in local folder.
- Add Raspberry PI support ([#18](https://github.com/AresValley/Artemis/pull/18), [#20](https://github.com/AresValley/Artemis/pull/20))

### Fixed
- Support new `JSON` format for some forecast data ([#21](https://github.com/AresValley/Artemis/pull/14)).
- Fixed categorization for very low x-ray flux according to NOAA format.
- Remove the `exclusive` parameter in a PyQt function ([#16](https://github.com/AresValley/Artemis/pull/16)).
  

## [3.2.0] - 2019-12-14
### Added
- The default font can be changed ([#14](https://github.com/AresValley/Artemis/pull/14)).
- Move `Themes` into `Settings`.
- Better settings management in `settings.json`.

### Fixed
- Fix a bug in the space weather. An inactive k-index caused a crash.

## [3.1.0] - 2019-10-21
### Added
- Automatic updates. From this version Artemis can update itself if a new version is available. Works only when running the executable version (disabled when running from source). The feature is partially unavailable for Mac, you can only download the new version.
- The software version displayed has now a `.Dev` appended when running from script (_e.g._ 3.1.0.Dev) to differentiate from an actual binary executable. The `.Dev` thus implies that the running version of the software could not correspond to a particular release.
- The `*.spec` files can be executed without copying the source code into
  their folder.
- Add a link to the GitHub repository in the action bar.
- Add support for signals with multiple-value acf ([#9](https://github.com/AresValley/Artemis/pull/9)). This partially breaks the backward compatibility because the database changed structure.

### Fixed
- Adding the `Artemis` folder to `PATH` as the expected behaviour. Prior to this fix, Artemis could not find the `Data` and `themes` folders if started from outside the `Artemis` folder.
- The audio buttons are of the same dimension also for high resolution screens ([#13](https://github.com/AresValley/Artemis/pull/13))
- An audio sample can be paused and a different one can be played without a program crash ([#12](https://github.com/AresValley/Artemis/pull/12))

## [3.0.1] - 2019-8-1
### Added
- The audio player has now a loop button ([#3](https://github.com/AresValley/Artemis/pull/3)).
- The project has now a Changelog file.

### Fixed
- Added SSL certificates for all downloads. Avoid a crash of the program for certain systems ([#6](https://github.com/AresValley/Artemis/pull/6)).
- Start the application in maximized mode. The label in the propagation data are well displayed ([#7](https://github.com/AresValley/Artemis/pull/7)).
- Compile the executable for Linux on an older version to avoid GLIBC compatibilities issues ([#8](https://github.com/AresValley/Artemis/pull/8)).

## [3.0.0] - 2019-07-23
First release.


<!-- Links definitions -->
[Unreleased]: https://github.com/AresValley/Artemis/compare/v4.0.5...HEAD
[4.0.5]: https://github.com/AresValley/Artemis/compare/v4.0.3...v4.0.5
[4.0.3]: https://github.com/AresValley/Artemis/compare/v4.0.1...v4.0.3
[4.0.1]: https://github.com/AresValley/Artemis/compare/v3.2.4...v4.0.1
[3.2.4]: https://github.com/AresValley/Artemis/compare/v3.2.1...v3.2.4
[3.2.3]: https://github.com/AresValley/Artemis/compare/v3.2.2...v3.2.3
[3.2.2]: https://github.com/AresValley/Artemis/compare/v3.2.1...v3.2.2
[3.2.1]: https://github.com/AresValley/Artemis/compare/v3.2.0...v3.2.1
[3.2.0]: https://github.com/AresValley/Artemis/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/AresValley/Artemis/compare/v3.0.1...v3.1.0
[3.0.1]: https://github.com/AresValley/Artemis/compare/v3.0.0...v3.0.1
[3.0.0]: https://github.com/AresValley/Artemis/releases/tag/v3.0.0
