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
        self.show()


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
