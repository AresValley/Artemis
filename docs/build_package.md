# Build Package
Building a distributable package with an executable for Artemis creates a practical solution for end-users, as they can run the application without needing to interact with the terminal and they can easily share the application as a standalone package.

## Requirements
* Python (3.11 or higher)

!!! info
    We assume that Python is already installed on the system and the Artemis source code has been downloaded and extracted. If these prerequisites are not met, please follow steps 1 to 3 in the [run from source section](run_from_source.md).

!!! warning "Cross-Compilation"
    An operating system that matches the target OS must be used to generate standalone packages, as Nuitka does not support cross-compilation. For example, you cannot build binaries on Windows that work on Linux or macOS.

## :simple-windows: Windows

### Procedure

1. Open a PowerShell terminal in the main Artemis folder and execute the following command to start the build process:

    ```
    .\building\Windows\build_windows.ps1
    ```

2. Wait for the build process to complete. This may take a few minutes depending on your system's performance. Once the process finishes, check the `artemis.dist/` directory: it will contain the standalone software with the `artemis.exe` executable.

---

## :simple-linux: Linux

### Procedure

1. Open a terminal in the main Artemis folder and execute the following command to start the build process:
    ```
    . ./building/Linux/build_linux.sh
    ```

2. Wait for the build process to complete. This may take a few minutes depending on your system's performance. Once the process finishes, check the `artemis.dist/` directory: it will contain the standalone software with the `app.bin` executable.
3. If you wish to create a shortcut, follows the procedure in the [installation section](installation.md/#create-a-shortcut)

---

## :simple-apple: Mac OS

!!! warning
    The support for the macOS compiled version of the program is temporarily limited due to a lack of machines for extensive testing. Feel free to contribute by reporting any issues you encounter by [opening an Issue](https://github.com/AresValley/Artemis/issues).

### Procedure

1. Open a terminal in the main Artemis folder and execute the following command to start the build process:
    ```
    . ./building/macOS/build_macos.sh
    ```
