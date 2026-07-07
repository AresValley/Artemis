import sys
import logging

from PySide6.QtCore import QCoreApplication, QTranslator
from PySide6.QtGui import QGuiApplication, QIcon

from .utils.constants import Constants
from .utils.ui_utils import set_ui
from .utils.config_utils import CONFIGURE_QT
from .ui.artemis import UIArtemis

from . import resources


def main():
    logger = logging.getLogger("peewee")
    logger.setLevel(logging.WARNING)
    logger.addHandler(logging.StreamHandler())

    set_ui()

    QCoreApplication.setOrganizationName(Constants.ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(Constants.ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(Constants.APPLICATION_NAME)

    app = QGuiApplication(sys.argv)

    translator = QTranslator()
    locale = CONFIGURE_QT.value('Localization', 'language', 'en_US')
    translator.load(f":/artemis/i18n/{locale}.qm")
    app.installTranslator(translator)

    icon_file_path = ":/data/images/artemis_icon.ico"
    app.setWindowIcon(QIcon(icon_file_path))

    UIArtemis()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
