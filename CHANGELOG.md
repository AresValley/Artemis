# Changelog
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and the format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

The first release is [3.0.0] because this is actually the third major version (completely rewritten) of the software.

## [Unreleased]

### Fixed
- Support new `JSON` format for some forecast data ([#21](https://github.com/AresValley/Artemis/pull/14)).
- Fixed categorization for very low x-ray flux according to NOAA format.
- Add some basic logging to the application. Also for severe errors, track them in info.log file in local folder.

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
[Unreleased]: https://github.com/AresValley/Artemis/compare/v3.2.0...HEAD
[3.2.0]: https://github.com/AresValley/Artemis/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/AresValley/Artemis/compare/v3.0.1...v3.1.0
[3.0.1]: https://github.com/AresValley/Artemis/compare/v3.0.0...v3.0.1
[3.0.0]: https://github.com/AresValley/Artemis/releases/tag/v3.0.0