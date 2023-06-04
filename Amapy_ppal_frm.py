#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from typing import List

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6 import uic

from amazdb import AmazDB
from Amapy_about import AmapyAbout
from Amapy_options import AmapyOptions
from Amapy_licence import AmapyLicence


class AmapyPpal(QMainWindow):
    def __init__(self):
        # Appel du constuteur de la classe mére
        super().__init__()

        # Chargement de l'interface
        self.ui = uic.loadUi(os.path.join("ui", "Amapy_ppal.ui"), self)

        # Déclarations de variables
        self.about = None
        self.licence = None
        self.recherche = None
        self.affiche_recherche = False
        self.ui.frme_recherche.hide()

        # Chargement des options du logiciel
        self.options = AmapyOptions()
        self.chemin_db = self.options.get_chemin_bdd()
        self.chemin_images = self.options.get_chemin_images()
        self.chemin_export = self.options.get_chemin_export()

        # Chargement de la base de données
        # self.db = AmazDB(os.path.join(self.chemin_db, "AmazDB.db"))
        self.db = AmazDB(os.path.join(self.chemin_db, "toto.db"))
        self.nb_lignes = self.db.make_request("SELECT count(*) FROM amatable;")[0][0]

        # Configuration de la progress bar
        self.ui.pgb_amaprogress.reset()
        self.ui.pgb_amaprogress.setRange(0, self.nb_lignes)

        # Création des événements
        self.ui.actionA_propos.triggered.connect(self.about_show)
        self.ui.action_Licence.triggered.connect(self.licence_show)
        self.ui.action_Options.triggered.connect(self.options_show)
        self.ui.action_Quitter.triggered.connect(self.quitter)
        self.ui.tbtn_exit.clicked.connect(self.quitter)
        self.ui.action_Mettre_tout_jour.triggered.connect(self.refresh_db)
        self.ui.tbtn_rafraichir.clicked.connect(self.refresh_db)
        self.ui.tbtn_rechercher.clicked.connect(self.recherche_produit)
        self.ui.btn_frame_chercher.clicked.connect(self.recherche_infos)

    def show_ppal(self) -> None:
        self.setup_window()
        self.config_view()
        self.ui.pgb_amaprogress.setValue(0)
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

    def config_view(self) -> None:
        # Déclaration des variables
        header_h = ["Nom du produit", "Description du produit", "Note", "Évaluation", "Prix", "Monnaie",
                    "Status du produit", "Date d'ajout", "Date de mise à jour"]
        header_v = []
        resultat = ""

        for i in range(self.nb_lignes):
            header_v.append(str(i + 1))

        self.ui.tbw_amazdb.setRowCount(len(header_v))
        self.ui.tbw_amazdb.setColumnCount(len(header_h))
        self.ui.tbw_amazdb.setHorizontalHeaderLabels(header_h)
        self.ui.tbw_amazdb.setVerticalHeaderLabels(header_v)

        resultat = self.load_db()
        self.show_result(resultat)

    def load_db(self) -> List[tuple]:
        # Récupération du contenu de la DB
        with open(os.path.join("requetes", "load_db.sql"), "r+t", encoding="utf-8") as f:
            requete = f.read()
        result = self.db.make_request(requete)

        return result

    def show_result(self, result: List[tuple]) -> None:
        # Suppression des anciennes données
        self.ui.tbw_amazdb.clearContents()

        # Configuration de la progress bar
        self.ui.pgb_amaprogress.reset()
        self.ui.pgb_amaprogress.setRange(0, len(result))

        # Affichage des données
        for i in range(len(result)):
            self.ui.tbw_amazdb.setItem(i, 0, QTableWidgetItem(str(result[i][0])))
            self.ui.tbw_amazdb.setItem(i, 1, QTableWidgetItem(str(result[i][1])))
            self.ui.tbw_amazdb.setItem(i, 2, QTableWidgetItem(str(result[i][2])))
            self.ui.tbw_amazdb.setItem(i, 3, QTableWidgetItem(str(result[i][3])))
            self.ui.tbw_amazdb.setItem(i, 4, QTableWidgetItem(str(result[i][4])))
            self.ui.tbw_amazdb.setItem(i, 5, QTableWidgetItem(str(result[i][5])))
            self.ui.tbw_amazdb.setItem(i, 6, QTableWidgetItem(str(result[i][6])))
            self.ui.tbw_amazdb.setItem(i, 7, QTableWidgetItem(str(result[i][7])))
            self.ui.tbw_amazdb.setItem(i, 8, QTableWidgetItem(str(result[i][8])))
            self.ui.pgb_amaprogress.setValue(i + 1)

    def about_show(self) -> None:
        about = AmapyAbout()
        about.setWindowIcon(QIcon(QPixmap(os.path.join("ressources/Principal", "info.png"))))
        about.setup_window()
        about.show_about()

    def licence_show(self) -> None:
        self.licence = AmapyLicence()
        self.licence.setup_window()
        self.licence.show_licence()

    def options_show(self) -> None:
        self.options = AmapyOptions()
        self.options.setup_window()
        self.options.show_options()

    def quitter(self) -> None:
        self.db.close_connection()
        self.close()

    def refresh_db(self) -> None:
        self.ui.tbw_amazdb.clear()
        resultat = self.load_db()
        self.show_result(resultat)

    def recherche_produit(self) -> None:
        if self.affiche_recherche == True:
            self.ui.frme_recherche.hide()
        else:
            self.ui.frme_recherche.show()

        self.affiche_recherche = not self.affiche_recherche

    def recherche_infos(self) -> None:
        recherche = f'amatable.nom_produit = "{self.ui.edt_frame_chercher.text()}"'

        # Récupération du contenu de la DB
        with open(os.path.join("requetes", "name_search.sql"), "r+t", encoding="utf-8") as f:
            requete = f.read()

        if len(self.ui.edt_frame_chercher.text()) == 0:
            self.ui.edt_frame_chercher.setStyleSheet("QLineEdit {background : red;}")
        else:
            self.ui.edt_frame_chercher.setStyleSheet("")
            resultat = self.db.make_request(requete.format(recherche = recherche))
            self.show_result(resultat)


def main() -> None:
    app = QApplication(sys.argv)
    frm_ppal = AmapyPpal()
    frm_ppal.setWindowIcon(QIcon(QPixmap(os.path.join("ressources/Commun", "amazonppal.png"))))
    frm_ppal.setup_window()
    frm_ppal.show_ppal()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
