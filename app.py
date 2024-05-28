import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QGuiApplication, QIcon

from artemis.utils.constants import Constants
from artemis.utils.ui_utils import set_ui
from artemis.ui.artemis import UIArtemis


def main():
    set_ui()

    QCoreApplication.setOrganizationName(Constants.ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(Constants.ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(Constants.APPLICATION_NAME)

    app = QGuiApplication(sys.argv)

    icon_file_path = (':/images/artemis_icon.ico')
    app.setWindowIcon(QIcon(icon_file_path))

    UIArtemis()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
