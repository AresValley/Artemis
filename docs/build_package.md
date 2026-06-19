# Build Package

Building a distributable package with an executable for Artemis creates a practical solution for end-users, as they can run the application without needing to interact with the terminal and they can easily share the application as a standalone package.

!!! info
    We assume that:

    - Python is already installed on the system.
    - The Artemis source code has been downloaded and extracted.

=== ":fontawesome-brands-microsoft: Windows"

    1. Create the virtual environement with UV and sync the dependencies following the steps 1 to 4 in the [run from source section](run_from_source.md)

    2. Execute the following command to start the build process:

        ```
        .\building\Windows\build_nuitka.ps1
        ```

    3. Wait for the build process to complete. This may take a few minutes depending on your system's performance. Once the process finishes, check the `artemis.dist/` directory: it will contain the standalone software with the `artemis.exe` executable.

=== ":fontawesome-brands-linux: Linux"

    1. Open a terminal in the main `Artemis` folder and install [Briefcase](https://github.com/beeware/briefcase):

        ```
        python -m pip install briefcase
        ```

    2. Initialize the application's build environment:

        ```
        briefcase build
        ```

    3. Once the build process is complete, generate the final redistributable package:

        ```
        briefcase package
        ```

    4. Once the process finishes, check the `dist` directory: it will contain the native distribution packages for your Linux target (a `.deb` package for Ubuntu/Debian and an `.rpm` package for Fedora/RHEL).
    5. You can then install them like any normal package using your system's package manager (e.g., `sudo apt install ./artemis_*.deb` or `sudo dnf install ./artemis_*.rpm`). Once installed, Artemis will be available in your system's Application Menu or via the terminal by typing `artemis`.

=== ":fontawesome-brands-apple: Mac OS"

    1. Open a terminal in the main `Artemis` folder and install [Briefcase](https://github.com/beeware/briefcase):

        ```
        python -m pip install briefcase
        ```

    2. Initialize the application's build environment:

        ```
        briefcase build
        ```

    3. Once the build process is complete, generate the final redistributable package:

        ```
        briefcase package macOS -p dmg
        ```

    4. Once the process finishes, check the `dist` directory: it will contain the native macOS disk image (`.dmg`).
    5. To install it, simply open the `.dmg` file and drag the `Artemis` icon into your `Applications` folder. Once installed, Artemis will be available in your Launchpad, Applications folder, or via Spotlight.
