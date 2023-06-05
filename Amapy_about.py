#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import platform
import os

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6 import uic
import pandas as pd
from importlib_metadata import version


class AmapyAbout(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(os.path.join("ui", "Amapy_about.ui"), self)

    def show_about(self) -> None:
        self.setup_window()
        self.get_packages_version()
        self.show()

    def setup_window(self) -> None:
        # Taille fixe pour la fenêtre
        self.setFixedWidth(self.frameGeometry().width())
        self.setFixedHeight(self.frameGeometry().height())

        # Centrage de la fenêtre
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Zone de text en lecture seule
        self.ui.ptedt_infos.setReadOnly(True)

    def get_packages_version(self) -> None:
        self.ui.ptedt_infos.appendPlainText("")
        self.ui.ptedt_infos.appendPlainText(
            f"Ce logiciel est développé en python {platform.python_version()} et utilise les bibliothèques tiers suivants :")
        self.ui.ptedt_infos.appendPlainText("- Qt version 6.5.0")
        self.ui.ptedt_infos.appendPlainText(f"- PyQt6 version {version('PyQt6')}")
        self.ui.ptedt_infos.appendPlainText(f"- pandas version {pd.__version__}")
        self.ui.ptedt_infos.appendPlainText(f"- XlsxWriter version {version('XlsxWriter')}")
        self.ui.ptedt_infos.appendPlainText(f"- matplotlib version {version('matplotlib')}")
        self.ui.ptedt_infos.appendPlainText(f"- numpy version {version('numpy')}")
        self.ui.ptedt_infos.appendPlainText(f"- Pillow version {version('Pillow')}")
        self.ui.ptedt_infos.appendPlainText(f"- requests version {version('requests')}")
        self.ui.ptedt_infos.appendPlainText(f"- beautifulsoup4 version {version('beautifulsoup4')}")
        self.ui.ptedt_infos.appendPlainText(f"- xlrd version {version('xlrd')}")


def about_menu() -> None:
    about = AmapyAbout()
    about.setWindowIcon(QIcon(QPixmap(os.path.join("ressources/Principal", "info.png"))))
    about.setup_window()
    about.show_about()


def main() -> None:
    app = QApplication(sys.argv)
    about = AmapyAbout()
    about.setWindowIcon(QIcon(QPixmap(os.path.join("ressources/Principal", "info.png"))))
    about.setup_window()
    about.show_about()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
