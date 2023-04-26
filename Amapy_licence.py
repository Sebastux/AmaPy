import sys
import os

from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow
from PyQt6 import uic


class AmapyLicence(QMainWindow):
    """
    Affichage de la licence du logiciel.
    """
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(os.path.join("ui", "Amapy_licence_frm.ui"), self)

        # Chargement de fichier licence
        self.load_licence_file()

        self.show()

    def load_licence_file(self):
        # Déclaration des variables
        licence = ""

        # Chargement du fichier licence.
        with open("LICENSE.md", "r", encoding="utf-8") as f:
            licence = f.read()
            self.ptedt_licence.insertPlainText(licence)

        # Mise en lecture seul de l'objet
        self.ui.ptedt_licence.setReadOnly(True)


def main():
    app = QApplication(sys.argv)
    lic = Amapy_Licence()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
