import sys
import os

from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow
from PyQt6 import uic


class AmapyOptions(QMainWindow):
    """
    Affiche la fenetre d'options de l'application.
    """

    def __init__(self):
        super().__init__()

        # Initialisation de variables
        self.ui = uic.loadUi(os.path.join("ui", "options_frm.ui"), self)

        # Copnfiguration de la fenetre
        self.setup_window()

        # Déclaration des événements
        self.ui.btn_ok.clicked.connect(self.ok_clicked)
        self.ui.btn_annuler.clicked.connect(self.annuler_clicked)

    def setup_window(self) -> None:
        """
        Configure la fenetre d'options de l'application.
        :return: None
        """
        # Taille fixe pour la fenetre
        self.setFixedWidth(self.frameGeometry().width())
        self.setFixedHeight(self.frameGeometry().height())

        # Centrage de la femnetre
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_options(self) -> None:
        """
        Affiche la fenetre de configuration de l'application.
        :return: None
        """
        self.show()

    def ok_clicked(self) -> None:
        """
        Sauvegarde les parametres et ferme la fenetre.
        :return: None
        """
        self.close()

    def annuler_clicked(self) -> None:
        """
        Ferme la fenetre de configuration sans sauvegardes les options.
        :return: None
        """
        self.close()


def main() -> None:
    """
    Fonction principale de l'application.
    :return: None
    """
    app = QApplication(sys.argv)
    options = AmapyOptions()
    options.show_options()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
