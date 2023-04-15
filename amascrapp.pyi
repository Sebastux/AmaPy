# -*- coding: utf-8 -*-
"""
   Module permettant l'extraction et le traitement des données extraite des pages Amazon.
"""

from typing import Dict

class AmaScrapp:
    """
    Classe permettant l'extraction et le traitement des données extraite des pages Amazon.
    """
    def __init__(self):
        ...

    def get_user_agent(self) -> None:
        """
        Méthode qui permet de choisir un user agent au hasard parmi une liste contenue dans un fichier.
        la méthode met à jour la variable d'instance
        :return: None
        """
        ...

    def get_article_name(self, soup: BeautifulSoup) -> None:
        """
        Méthode qui permet la récupération du nom du produit.
        :param soup: Objet BeautifullSoup permettant la récupération de l'information
        :return: None
        """
        ...

    def get_article_price(self, soup: BeautifulSoup) -> None:
        """
        Méthode qui permet la récupération du prix du produit.
        :param soup: Objet BeautifullSoup permettant la récupération de l'information
        :return: None
        """
        ...

    def get_article_note(self, soup: BeautifulSoup) -> None:
        """
        Méthode qui permet la récupération de la note du produit.
        :param soup: Objet BeautifullSoup permettant la récupération de l'information
        :return: None
        """
        ...

    def get_article_status(self, soup: BeautifulSoup) -> None:
        """
        Méthode qui permet la récupération du status du produit.
        :param soup: Objet BeautifullSoup permettant la récupération de l'information
        :return: None
        """
        ...

    def get_article_review(self, soup: BeautifulSoup) -> None:
        """
        Méthode qui permet la récupération du nombre de note du produit.
        :param soup: Objet BeautifullSoup permettant la récupération de l'information
        :return: None
        """
        ...

    def get_article_description(self, soup: BeautifulSoup) -> None:
        """
        Méthode qui permet la récupération de la description du produit.
        :param soup: Objet BeautifullSoup permettant la récupération de l'information
        :return: None
        """
        ...

    def get_article_image(self, soup: BeautifulSoup, repertoire: str, chemin_ko: str = None) -> None:
        """
        Méthode qui permet la récupération de l'URL de l'image du produit
        :param repertoire: Chemin du répertoire de sauvearde des images..
        :param chemin_ko: Chemin d'une image par défaut en cas d'échec.
        :param soup: Objet BeautifullSoup permettant la récupération de l'information
        :return: None
        """
        ...

    def get_article(self, url: str) -> None:
        """
        Méthode qui permet la récupération de l'ensemble des informations du produit
        :param url: url du produit à traiter
        :return: None
        """
        ...

    def export_to_dict(self) -> Dict:
        """
        Méthode permettant l'exportation des données produit seus formede dictionnaire.
        :return: Dictionnaire contenant les informations produit
        """
        ...

    def export_to_excell(self, chemin_fic: str) -> None:
        """
        Méthode permettant l'export de données dans un fichier excell au format xlsx
        :param chemin_fic:  chemin du fichier de destination
        :return: None
        """
        ...

    def export_to_csv(self, chemin_fic: str) -> None:
        """
        Méthode permettant l'export de données dans un fichier au format csv
        :param chemin_fic:  chemin du fichier de destination
        :return: None
        """
        ...

    def export_to_json(self, chemin_fic: str) -> None:
        """
        Méthode permettant l'export de données dans un fichier au format json
        :param chemin_fic:  chemin du fichier de destination
        :return: None
        """
        ...
