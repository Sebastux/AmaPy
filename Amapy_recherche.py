import sys
import os

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6 import uic


class AmapyRecherche(QMainWindow):
    def __init__(self):
        # Appel du constuteur de la classe mére
        super().__init__()

        # Chargement de l'interface
        self.ui = uic.loadUi(os.path.join("ui", "Amapy_recherche.ui"), self)

    def show_recherche(self) -> None:
        self.setup_window()
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

    def get_nom_produit(self) -> str:
        return self.ui.edt_nom_produit.text()


def main() -> None:
    app = QApplication(sys.argv)
    frm_recherche = AmapyRecherche()
    frm_recherche.setWindowIcon(QIcon(QPixmap(os.path.join("ressources/Principal", "chercher.png"))))
    frm_recherche.setup_window()
    frm_recherche.show_recherche()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
