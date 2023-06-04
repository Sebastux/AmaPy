#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List

from PyQt6.QtWidgets import QMainWindow

"""
Module pricipal du logiciel Amapy. Tous les autres module seront
appelé depuis cette classe
"""
class AmapyPpal(QMainWindow):
    """
    Classe principal du logiciel Amapy
    """
    def __init__(self):
        """
        Construteur de la classe.
        """

    def show_ppal(self) -> None:
        """
        Méthode permettant l'affichage de la fenêtre.
        :return: None
        """

    def setup_window(self) -> None:
        """
        Méthode permettant la configuration de la fenêtre et de certain
        de ses éléments.
        :return: None
        """

    def quitter(self) -> None:
        """
        Méthode permettant de faire certaines actions lors de la fermeture de la
        fenetre ppal
        :return: None
        """

    def refresh_db(self) -> None:
        """
        Méthode permettant de raffraichir l'affichage du
        :return: None
        """

    def recherche_produit(self) -> None:
        """
        Pemet d'afficher ou de masquer la fenêtre de recherche
        :return: None
        """

    def load_db(self) -> List[tuple]:
        """
        Méthode permettant de charger entierement la base de données pour
        pouvoir l'afficher ensuite
        :return: Une liste de tuple ou chaque tuple représente une ligne de la requête
        """

    def show_result(self, result: List[tuple]) -> None:
        """
        Affiche le résultat d'une requete dans un objet grile
        :param result: Liste de tuple contenant le résultat de la requête.
        :return: None
        """

    def about_show(self) -> None:
        """
        Affiche la fenêtre À propos.
        :return: None
        """

    def licence_show(self) -> None:
        """
        Affiche les informations de licence du logiciel.
        :return: None
        """

    def options_show(self) -> None:
        """
        Affiche la fenêtre des options du logiciel
        :return: None
        """

    def config_view(self) -> None:
        """
        Méthode permettant de configurer la fenêtre principale.
        :return: None
        """

    def recherche_infos(self) -> None:
        """
        Méthode permettant de générer une requête en fonction des critères de recherche.
        :return: None
        """

def main() -> None:
    """
    Fonction permettant l'execution du module.
    :return: None
    """
