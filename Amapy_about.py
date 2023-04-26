import sys
import os

from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow
from PyQt6 import uic


class AmapyAbout(QMainWindow):
    """
    Affiche la fenetre d'à propos de l'application.
    """

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(os.path.join("ui", "Amapy_about.ui"), self)

    def show_about(self) -> None:
        """
        Affiche la fenetre d'à propos de l'application.
        :return: None
        """
        self.setup_window()
        self.show()

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
        self.ui.ptedt_infos.setReadOnly(True)


def main() -> None:
    """
    Fonction principale de l'application.
    :return: None
    """
    app = QApplication(sys.argv)
    about = AmapyAbout()
    about.show_about()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
