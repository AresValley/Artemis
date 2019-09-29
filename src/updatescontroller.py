import subprocess as sp
import webbrowser
from PyQt5.QtCore import QObject, pyqtSlot, QProcess
from PyQt5.QtWidgets import QMessageBox, qApp
from constants import Constants, Messages, DownloadTarget
from downloadtargetfactory import get_download_target
from utilities import pop_up
from os_utilities import IS_MAC
from executable_utilities import IS_BINARY
from threads import UpdatesControllerThread
from versioncontroller import VersionController


class UpdatesController(QObject):

    def __init__(self, current_version, owner):
        super().__init__()
        self._owner = owner
        self._download_window = self._owner.download_window
        self._current_version = current_version
        self.version_controller = VersionController()
        self._updates_thread = UpdatesControllerThread(self.version_controller)
        self._updates_thread.on_success.connect(self._startup_updates_check)

    def start(self):
        """Start the thread."""
        if IS_BINARY:
            self._updates_thread.start()

    @pyqtSlot()
    def start_verify_software_version(self):
        if not IS_BINARY:
            pop_up(
                self._owner,
                title=Messages.FEATURE_NOT_AVAILABLE,
                text=Messages.SCRIPT_NOT_UPDATE
            ).show()
            return
        if not self._download_window.isVisible():
            self._updates_thread.start()

    @pyqtSlot(bool)
    def _verify_software_version(self, success):
        """Verify if there is a new software version.

        Otherwise notify the user that the software is up to date."""
        if not self._download_window.isVisible():
            if success:
                new_version_found = self._check_new_version()
                if not new_version_found:
                    pop_up(
                        self._owner,
                        title=Messages.UP_TO_DATE,
                        text=Messages.UP_TO_DATE_MSG
                    ).show()
            else:
                pop_up(
                    self._owner,
                    title=Messages.NO_CONNECTION,
                    text=Messages.NO_CONNECTION_MSG
                ).show()

    @pyqtSlot(bool)
    def _startup_updates_check(self, success):
        self._updates_thread.on_success.disconnect()
        self._updates_thread.on_success.connect(self._verify_software_version)
        if success:
            if not self._check_new_version():
                # Check for a new version of the updater only if Artemis is up to date.
                self._check_updater_version()

    def _check_new_version(self):
        """Check whether there is a new software version available.

        Does something only if the running program is a compiled version."""
        if not IS_BINARY:
            return None
        latest_version = self.version_controller.software.version
        if latest_version is None:
            return False
        if latest_version == self._current_version:
            return False
        answer = pop_up(
            self._owner,
            title=Messages.NEW_VERSION_AVAILABLE,
            text=Messages.NEW_VERSION_MSG(latest_version),
            informative_text=Messages.DOWNLOAD_SUGG_MSG,
            is_question=True,
        ).exec()
        if answer == QMessageBox.Yes:
            if IS_MAC:
                webbrowser.open(self.version_controller.software.url)
            else:
                updater = QProcess()
                command = Constants.UPDATER_SOFTWARE + " " + \
                    self.version_controller.software.url + \
                    " " + self.version_controller.software.hash_code + \
                    " " + str(self.version_controller.software.size)
                try:
                    updater.startDetached(command)
                except BaseException:
                    pass
                else:
                    qApp.quit()
        return True

    def _check_updater_version(self):
        """Check is a new version of the updater is available.

        If so, ask to download the new version.
        If the software is not a compiled version, the function is a NOP."""
        if not IS_BINARY or IS_MAC:
            return
        latest_updater_version = self.version_controller.updater.version
        try:
            with sp.Popen(
                [Constants.UPDATER_SOFTWARE, "--version"],
                encoding="UTF-8",
                stdout=sp.PIPE,
                stderr=sp.STDOUT,
                stdin=sp.DEVNULL  # Needed to avoid OsError: [WinError 6] The handle is invalid.
            ) as proc:
                updater_version = proc.stdout.read().rstrip("\r\n")  # Strip any possible newline, to be sure.
        except Exception:
            updater_version = latest_updater_version
        if latest_updater_version is None:
            return
        if updater_version != latest_updater_version:
            answer = pop_up(
                self._owner,
                title=Messages.UPDATES_AVAILABALE,
                text=Messages.UPDATES_MSG,
                is_question=True,
            ).exec()
            if answer == QMessageBox.Yes:
                self._download_window.activate(
                    get_download_target(
                        DownloadTarget.UPDATER,
                        self.version_controller.updater
                    )
                )
