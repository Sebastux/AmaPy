# -*- coding: utf-8 -*-
"""
Module de gestion de sauvegarde de données dans une DB SQLite.
"""
from typing import Dict, List, Tuple


class AmazDB:
    """
    Classe permettant la sauvegarde des produits dans une DB SQLite.
    """

    def __init__(self, chemin_fic: str):
        """
        Constructeur de la classe
        :param chemin_fic: Chemin de la DB à ouvrir ou à créer.
        """
        ...

    def create_db_fic(self) -> None:
        """
        Méthode permettant de créer un fichier de base de donnèes.
        :return: None
        """
        ...

    def open_db_fic(self) -> None:
        """
        Méthode permettant d'ouvrir un fichier de base de donnèes.
        :return: None
        """
        ...

    def close_connection(self) -> None:
        """
        Méthode permettant de fenmer un fichier de base de donnèes.
        :return: None
        """
        ...

    def drop_db(self) -> None:
        """
        Méthode permettant de supprimer un fichier de base de donnèes.
        :return: None
        """
        ...

    def make_request(self, requete: str, commit: bool = False) -> List[Tuple]:
        """
        Méthode permettant de faire une requete sur la base de données
        :param requete: Contenu de la requéte sous forme de chaine de caractères
        :param commit: Si la requête insère ou supprime des données, permet la validation de cette requête.
        :return: Retourne le résultat sous forme d'une liste de tuple.
        """
        ...

    def make_requests(self, requetes: str, commit: bool = False) -> List[Tuple]:
        """
        Méthode permettant de faire une requete sur la base de données
        :param requetes: Contenu des requétes sous forme de chaine de caractères
        :param commit: Si les requêtes insèrent ou suppriment des données, permet la validation de cette requête.
        :return: Retourne le résultat sous forme d'une liste de tuple.
        """
        ...

    def add_product(self, product: Dict) -> None:
        """
        Ajoute un nouveau produit dans la BDD.
        :param product: Informations du produit sous forme de dictionnaire.
        :return: None
        """
        ...

    def remove_product(self, product: str) -> bool:
        """
        Supprime un produit dans la BDD.
        :param: product Informations du produit sous forme de dictionnaire.
        :return: bool True si la suppression est faite et False dans le cas contraire
        """
        ...

    def update_product(self, product: Dict) -> bool:
        """
        Méthode permettant la mise à jour d'un produit suite à une nouvelle recherche
        :param product: Dictionnaire contenant la liste des informations à mettre à jour
        :return: True si la MAJ est faite et False dans le cas contraire
        """
        ...

    def export_datas_to_excell(self, chemin_exp: str, product_list: List) -> bool:
        """
        Exporte un produit dans un fichier au format xlsx. La méthode crée un
        sous répertoire contenant un fichier Excel, une image du produit et
        un graphique de l'évolution des prix.
        :param chemin_exp: Chemin du répertoire où seront copier les exports de fichiers
        :param product_list: Listes de noms de produit à exporter.
        :return:True si l'export s'est bien passé et False dans le cas contraire.
        """
        ...

    def export_datas_to_csv(self, chemin_exp: str, product_list: List) -> bool:
        """
        Export des données au format CSV. L'intégralité des données seront exportée et seul le dernier prix en date sera
        fournie.
        :param chemin_exp: Chemin du répertoire où seront copier les exports de fichiers
        :param product_list: Listes de noms de produit à exporter.
        :return:True si l'export s'est bien passé et False dans le cas contraire.
        """
        # Déclaration de variables
        ...

    def export_datas_to_json(self, chemin_exp: str, product_list: List) -> bool:
        """
        Export des données au format CSV. L'intégralité des données seront exportée et seul le dernier prix en date sera
        fournie.
        :param chemin_exp: Chemin du répertoire où seront copier les exports de fichiers
        :param product_list: Listes de noms de produit à exporter.
        :return:True si l'export s'est bien passé et False dans le cas contraire.
        """
        ...

    def create_product_graph(self, chemin_export: str, product_id: int, extension: str = "jpg") -> bool:
        """
        Création du graphique des produits.
        :param chemin_export: Chemin du répertoire où seront copier les exports de fichiers
        :param product_id: Clé primaire du produit à exporter.
        :param extension: Extension de graphe lors de l'export. Il peut avoir 3 valeurs différentes "jpg" ou "png" ou "pdf".
        :return:True si l'export s'est bien passé et False dans le cas contraire.
        """
        ...
