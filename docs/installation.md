# Installation

=== ":fontawesome-brands-microsoft: Windows"

    ## Installer

    Download the installer from the main website ([Aresvalley](https://aresvalley.com)) or from GitHub repository (in the Assets menu from the [:material-download: LATEST RELEASE](https://github.com/AresValley/Artemis/releases)) and follow the guided procedure to complete the installation process.

    ## WinGet

    To install Artemis with winget, use the following command:

    ```
    winget install -e --id AresValley.Artemis
    ```

=== ":fontawesome-brands-linux: Linux"

    The easiest and recommended way to install the application on both Linux PCs (**x64**) and Raspberry Pi (**arm64**) is via **Flathub**.
    <div align="center">
        <a href='https://flathub.org/it/apps/com.aresvalley.artemis'>
            <img width='240' alt='Get it on Flathub' src='https://flathub.org/api/badge?svg&locale=en'/>
        </a>
    </div>

    Alternatively, you can search for it directly in your distribution's Software Center if Flatpak support is already enabled.

=== ":fontawesome-brands-apple: MacOS"

    !!! warning "No Pre-compiled Binaries for macOS"
        We do not provide pre-compiled binaries (`.app` or `.dmg`) for macOS due to Apple's strict code-signing requirements.
        
        Packaging a macOS application for public distribution requires a valid Apple Developer Account and an official Application Distribution Certificate (99 USD per year, thanks Apple). Without these, `Briefcase` (the tool used to build the executable) can only package the app using an **ad-hoc identity**. 
        
        Ad-hoc signed applications are locked to the specific machine that compiled them and **will not run on any other computer** due to macOS Gatekeeper restrictions. Therefore, to run this app on macOS, you must clone the repository and build it locally.

    Then, you can choose from:

    - **Run the program directly from the source:** Follow the instructions provided in [this chapter](run_from_source.md) to launch the program from the source code.
    - **Compile the Artemis binaries** on your machine following the instructions in [this chapter](build_package.md#__tabbed_1_3).
