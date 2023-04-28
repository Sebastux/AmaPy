import sys
import os
from pathlib import Path
import configparser

from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QFileDialog
from PyQt6 import uic
from pathlib import Path
from fonctions_qt import AfficheMessages


class AmapyOptions(QMainWindow):
    """
    Affiche la fenetre d'options de l'application.
    """

    def __init__(self):
        super().__init__()

        # Initialisation de variables
        self.ui = uic.loadUi(os.path.join("ui", "options_frm.ui"), self)

        # config de la tab par défaut
        self.ui.tabw_options.setCurrentIndex(0)

        # Déclaration des événements
        self.ui.btn_ok.clicked.connect(self.ok_clicked)
        self.ui.btn_annuler.clicked.connect(self.annuler_clicked)
        self.ui.tbn_bdd.clicked.connect(self.tbn_bdd_clicked)
        self.ui.tbtn_export.clicked.connect(self.tbtn_export_clicked)
        self.ui.tbtn_images.clicked.connect(self.tbtn_images_clicked)

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

    def show_options(self) -> None:
        """
        Affiche la fenêtre de configuration de l'application.
        :return: None
        """
        # Affichage de la fenêtre
        self.show()

    def ok_clicked(self) -> None:
        """
        Sauvegarde les parametres et ferme la fenêtre.
        :return: None
        """
        self.close()

    def annuler_clicked(self) -> None:
        """
        Ferme la fenêtre de configuration sans sauvegardes les options.
        :return: None
        """
        self.close()

    def tbn_bdd_clicked(self) -> None:
        """
        Permet de selectionner le répertoire de la BDD.
        :return: None
        """
        chemin_bdd = QFileDialog.getExistingDirectory(self, "Chemin de sauvegarde de la base de données.")
        if chemin_bdd:
            path = Path(chemin_bdd)
            self.ui.edt_bdd.setText(str(path))

    def tbtn_export_clicked(self) -> None:
        """
        Permet de selectionner le répertoire d'export.
        :return: None
        """
        chemin_export = QFileDialog.getExistingDirectory(self, "Chemin de sauvegarde des export.")
        if chemin_export:
            path = Path(chemin_export)
            self.ui.edt_export.setText(str(path))

    def tbtn_images_clicked(self) -> None:
        """
        Permet de selectionner le répertoire d'export des images.
        :return: None
        """
        chemin_images = QFileDialog.getExistingDirectory(self, "Chemin de sauvegarde des images.")
        if chemin_images:
            path = Path(chemin_images)
            self.ui.edt_images.setText(str(path))


def main() -> None:
    """
    Fonction principale de l'application.
    :return: None
    """
    app = QApplication(sys.argv)
    options = AmapyOptions()
    options.setup_window()
    options.show_options()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
