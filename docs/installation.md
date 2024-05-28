# Installation

**Requirements:**

* **Windows** 8 or later
* **Linux** Ubuntu 20.04+ / Mint 20+ / Fedora 32+ and many other
* **macOS** 11+ (Big Sur or later)

## :simple-windows: Windows
Just download the installer and follow the guided procedure to complete the installation process.

---

## :simple-linux: Linux
Download and extract the tarball archive in a folder of your choice and run the executable `app.bin`.

### Create a Shortcut

1. To create a direct shortcut (in the main menu) launch the bash script in the terminal with the command:

    ```
    . create_shortcut.sh
    ```

This script will:

- Set the correct read/write privileges of the Artemis folder
- Create the artemis.desktop file (shortcut) in /home/$USER/.local/share/applications
- Move the Artemis icon file to /usr/share/icons

---

## :simple-apple: Mac OS
The support for the macOS compiled version of the program is temporarily limited due to a lack of machines for extensive testing. To use Artemis on a macOS device, you have the following options:

* **Run the program directly from the source:** Follow the instructions provided in [this chapter](run_from_source.md) to launch the program from the source code.
* **Compile the Artemis 4 binaries on your machine:** In this case, you can contribute by reporting any issues you encounter by [opening an Issue](https://github.com/AresValley/Artemis/issues).
* **Use the last available compiled version (3.2.1):** Although this version is no longer officially supported, it remains available for use.