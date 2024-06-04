# Run from source code
Running Artemis directly from the source code using the Python interpreter is considered the most reliable and least problematic method. This approach ensures maximum compatibility and reduces the likelihood of encountering runtime issues. However, it is also the less practical option, as it requires the use of the terminal for the execution.

## Requirements
* Python (3.11 or higher)

## Procedure

1. Download and install Python (3.11 or higher) from the official [website](https://www.python.org/downloads/). Be sure to select the flag `Add Python 3.x to PATH` during the first part of the installation.

2. Download Artemis source code from the [latest release](https://github.com/AresValley/Artemis/releases) in the GitHub repository.

3. Extract the downloaded archive.

4. Open the terminal in Artemis folder and install the required Python libraries with PIP:
    ```
    pip install -r requirements.txt --user
    ```

5. Launch Artemis:
    ```
    python app.py
    ```

!!! example "Note for Developers"
    Whenever modifications are made to any **.qml** file or any assets (such as images, icons, etc.), it is essential to recompile the **resource.py** file to ensure that the changes are reflected in the application. To achieve this, execute the following command:
    ```
    pyside6-rcc ./artemis.qrc -o artemis/resources.py
    ```

## Folders Structure
Artemis can be safely executed and/or installed in any folder (even protected ones, such as `Program Files (x86)` in Windows) because Artemis performs read-only operations in the `BASE_DIR` folder from where it runs. All the reading-writing operations (such as database ops, logging, etc.) are performed in standard folders as follow:

### :simple-windows: Windows
* Data, Cache, Configurations: `$USER\AppData\Local\AresValley\Artemis`
* Logs: `$USER\AppData\Local\Temp`

### :simple-linux: Linux
* Data, Cache, Configurations: `~/.local/share/AresValley/Artemis`
* Logs: `/tmp`

### :simple-apple: Mac OS
* Data, Cache, Configurations: `~/Library/Application Support/AresValley/Artemis`
* Logs: `/tmp`
