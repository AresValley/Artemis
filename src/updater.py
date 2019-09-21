import argparse
import os
import os.path
import sys
from PyQt5.QtCore import QObject, QProcess
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, qApp
from download_window import DownloadWindow
from os_utilities import is_mac_os
from executable_utilities import is_executable_version
from constants import Constants, __BASE_FOLDER__, DownloadObj


__VERSION__ = "0.0.1"


# Global stylesheet.
stylesheet = """
/*************************************
Main Window and Splitters
**************************************/
QWidget:window {
    background-color: #29353B;
}

/*************************************
Main menu (Bar)
**************************************/
QMenuBar {
    background-color: transparent;
    color: #AFBDC4;
}

QMenuBar::item {
    background-color: transparent;
}

QMenuBar::item:disabled {
    color: gray;
}

QMenuBar::item:selected {
    color: #FFFFFF;
    border-bottom: 2px solid #88cc00;
}

QMenuBar::item:pressed {
    color: #FFFFFF;
    border-bottom: 2px solid #88cc00;
}

QToolBar {
    background-color: transparent;
    border: 1px solid transparent;
}

QToolBar:handle {
    background-color: transparent;
    border-left: 2px dotted #80CBC4;
    color: transparent;
}

QToolBar::separator {
    border: 0;
}

QMenu {
    background-color: #263238;
    color: #AFBDC4;
}

QMenu::item:selected {
    color: #FFFFFF;
}

QMenu::item:pressed {
    color: #FFFFFF;
}

QMenu::separator {
    background-color: transparent;
    height: 1px;
    margin-left: 10px;
    margin-right: 10px;
    margin-top: 5px;
    margin-bottom: 5px;
}


/*************************************
Progressbar
**************************************/
QProgressBar
{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center;
}

QProgressBar::chunk
{
    background-color: #88cc00;
    width: 2.15px;
    margin: 0.5px;
}

/*************************************
Labels and Rich Text boxes
**************************************/
QLabel {
    background-color: transparent;
    color: #CFD8DC;
}

QDialog {
    background-color: transparent;
    color: #949a9c;
}

QTextBrowser {
    background-color: transparent;
    color: #949a9c;
}

/*************************************
Buttons
**************************************/
QPushButton {
    background-color: transparent;
    color: #AFBDC4;
    border: 1px solid transparent;
    padding: 4px 22px;
}

QPushButton:hover {
    border-left: 2px solid #88cc00;
    border-right: 2px solid #88cc00;
    color: #FFFFFF;
}

QPushButton:pressed {
    color: #FFFFFF;
}

QPushButton:disabled {
    color:#546E7A;
}

QPushButton:checked {
    color: #88cc00;
}
"""


class DownloadObjCustom:
    def __init__(self, url, hash_code, size):
        self.url = url
        self.hash_code = hash_code
        self.size = size
        self.dest_path = __BASE_FOLDER__
        self.target = DownloadObj.UPDATER

    def delete_files(self):
        if os.path.exists(Constants.UPDATER_SOFTWARE):
            os.remove(Constants.UPDATER_SOFTWARE)


class _ArtemisUpdater(QObject):
    """Updater of the main software."""

    def __init__(self, target):
        super().__init__()
        self.target = target
        self.download_window = DownloadWindow()
        self.download_window.setStyleSheet(stylesheet)
        self.download_window.cancel_btn.clicked.connect(qApp.quit)
        self.download_window.complete.connect(self.start_main_program)

    def start(self):
        """Close the main program and start the download."""
        self.download_window.activate(self.target)

    def start_main_program(self):
        """Restart the (updated) main program and close the updater."""
        self.download_window.setVisible(False)
        artemis = QProcess()
        try:
            artemis.startDetached(Constants.EXECUTABLE_NAME)
        except BaseException:
            pass
        qApp.quit()


if __name__ == '__main__':
    # For executables running on Mac Os systems.
    if is_executable_version() and is_mac_os() and not __BASE_FOLDER__:
        os.chdir(sys._MEIPASS)

    parser = argparse.ArgumentParser(prog='Artemis Updater')
    parser.add_argument("url", nargs="?", default="", type=str, help="Download url")
    parser.add_argument("hash_code", nargs="?", default="", type=str, help="sha256 of the file")
    parser.add_argument("size", nargs="?", default=0, type=int, help="Size (KB) of the file")
    parser.add_argument('--version', action='version', version=__VERSION__)
    args = parser.parse_args()

    my_app = QApplication(sys.argv)
    ARTEMIS_ICON = os.path.join(":", "icon", "default_pics", "Artemis3.500px.png")
    img = QPixmap(ARTEMIS_ICON)
    updater = _ArtemisUpdater(DownloadObjCustom(args.url, args.hash_code, args.size))

    if not args.url or not args.hash_code or not args.size:
        updater.start_main_program()
    else:
        updater.start()
        sys.exit(my_app.exec_())
