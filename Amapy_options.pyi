"""
Module permettant la gestion des options du logiciel Amapy
"""

from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QFileDialog

class AmapyOptions(QMainWindow):
    """
    Affiche la fenetre d'options de l'application.
    """

    def __init__(self): ...

    def setup_window(self) -> None:
        """
        Configure la fenêtre d'options de l'application.
        :return: None
        """

    def show_options(self) -> None:
        """
        Affiche la fenêtre de configuration de l'application.
        :return: None
        """

    def ok_clicked(self) -> None:
        """
        Sauvegarde les parametres et ferme la fenêtre.
        :return: None
        """

    def annuler_clicked(self) -> None:
        """
        Ferme la fenêtre de configuration sans sauvegardes les options.
        :return: None
        """

    def tbn_bdd_clicked(self) -> None:
        """
        Permet de selectionner le répertoire de la BDD.
        :return: None
        """

    def tbtn_export_clicked(self) -> None:
        """
        Permet de selectionner le répertoire d'export.
        :return: None
        """

    def tbtn_images_clicked(self) -> None:
        """
        Permet de selectionner le répertoire d'export des images.
        :return: None
        """

    def load_config(self) -> None:
        """
        Charge les parametres de configuration.
        :return: None
        """
        # Déclaration de variables

    def write_config(self) -> None:
        """
        Méthode penrmettant la sauvegarde de la configuration d'Amapy
        :return: None
        """


    def get_chemin_export(self) -> str:
        """
        Renvoi le chemin d'export des fichiers.
        :return: Chemin d'export des fichiers.
        """

    def get_chemin_bdd(self) -> str:
        """
        Renvoi le chemin de stockage de la DB.
        :return: Chemin de stockage de la DB.
        """

    def get_chemin_images(self) -> str:
        """
        Renvoi le chemin de stockage des images.
        :return: Chemin de stockage des images.
        """


def main() -> None:
    """
    Fonction principale de l'application.
    :return: None
    """