import sys
import os

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AmapyLicence(QMainWindow):
    """
    Affichage de la licence du logiciel.
    """

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(os.path.join("ui", "Amapy_licence.ui"), self)

        # Chargement de fichier licence
        self.load_licence_file()

    def load_licence_file(self):
        # Déclaration des variables
        licence = ""

        # Chargement du fichier licence.
        try:
            with open("LICENSE.md", "r", encoding="utf-8") as f:
                licence = f.read()
                self.ptedt_licence.insertPlainText(licence)
        except FileNotFoundError:
            self.ptedt_licence.insertPlainText("Impossible d'ouvrir le fichier LICENSE.md.\n")
            self.ptedt_licence.insertPlainText("Veuillez vérifier la présence du fichier.\n")
            self.ptedt_licence.insertPlainText("Vous pouvez le télécharger sur github ou réinstaller le logiciel.\n")
            self.ptedt_licence.insertPlainText("https://github.com/Sebastux/AmaPy/blob/master/LICENSE.md.\n")
            self.ptedt_licence.insertPlainText("Si le problème persiste, merci de contacter le développeur.")

        # Mise en lecture seul de l'objet
        self.ui.ptedt_licence.setReadOnly(True)

    def setup_window(self) -> None:
        """
        Configure la fenêtre d'options de l'application.
        :return: None
        """
        # Taille fixe pour la fenêtre
        self.setFixedWidth(self.frameGeometry().width())
        self.setFixedHeight(self.frameGeometry().height())

        # Centrage de la fenêtre
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Zone de text en lecture seule
        self.ui.ptedt_licence.setReadOnly(True)

    def show_licence(self) -> None:
        """
        Affiche la fenêtre de licence.
        :return: None
        """
        self.show()


def main():
    app = QApplication(sys.argv)
    lic = AmapyLicence()
    lic.setup_window()
    lic.show_licence()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
