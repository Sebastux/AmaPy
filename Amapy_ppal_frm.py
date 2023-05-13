import sys
import os

from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QTableWidgetItem
from PyQt6 import uic

from amazdb import AmazDB


class AmapyPpal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(os.path.join("ui", "Amapy_ppal_frm.ui"), self)

        self.db = AmazDB("/home/Sebastien/Dépots/publique/AmaPy/bdd/toto.db")
        self.nb_lignes = self.db.make_request("SELECT count(*) FROM amatable;")[0][0]

        # Configuration de la progress bar
        self.ui.pgb_amaprogress.reset()
        self.ui.pgb_amaprogress.setRange(0, self.nb_lignes)

        # Création des événements
        self.ui.tbtn_test.clicked.connect(self.config_view)

    def show_ppal(self) -> None:
        self.setup_window()
        self.show()

    def setup_window(self) -> None:
        # Taille fixe pour la fenêtre
        self.setFixedWidth(self.frameGeometry().width())
        self.setFixedHeight(self.frameGeometry().height())

        # Couleur de la grille
        self.ui.tbw_amazdb.setStyleSheet("gridline-color: black;")

        # Centrage de la fenêtre
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main() -> None:
    app = QApplication(sys.argv)
    frm_ppal = AmapyPpal()
    frm_ppal.setup_window()
    frm_ppal.show_ppal()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
