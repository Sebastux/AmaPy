"""
Module de gestion de sauvegarde de données dans une DB SQLite.
"""
import os
import sqlite3
from datetime import datetime

import pandas as pd


class AmazDB:
    """
    Classe permettant la sauvegarde des produits dans une DB SQLite.
    """

    def __init__(self, chemin_fic: str):
        # Création des requêtes
        self.__req1 = "INSERT INTO amatable (nom_produit, note, description, evaluation, \
                      status_produit, date_creation) VALUES(?, ?, ?, ?, ?, ?);"

        self.__req2 = "INSERT INTO tblprix (keyzon, prix, monnaie, date_maj) VALUES(?, ?, ?, ?);"
        self.__req3 = "INSERT INTO tbllink (keyzon, url, chemin_image1) VALUES(?, ?, ?);"

        # Création des variables d'instance
        self.chemin_fic = chemin_fic
        self.connecteur_db = None
        self.curseur_db = None

        # Gestion de la BDD
        if os.path.exists(chemin_fic):
            self.open_db_fic()
        else:
            self.create_db_fic()

        # self.connecteur_db.row_factory = sqlite3.Row

    def create_db_fic(self) -> None:
        """
        Méthode permettant de créer un fichier de base de donnèes.
        :return: None
        """
        self.connecteur_db = sqlite3.connect(self.chemin_fic)
        self.curseur_db = self.connecteur_db.cursor()
        with open(os.path.join("requetes", "createdb.sql"), "r+t", encoding="utf-8") as f:
            requete = f.read()
            self.curseur_db.executescript(requete)

    def open_db_fic(self) -> None:
        """
        Méthode permettant d'ouvrir un fichier de base de donnèes.
        :return: None
        """
        self.connecteur_db = sqlite3.connect(self.chemin_fic)
        self.curseur_db = self.connecteur_db.cursor()

    def close_connection(self) -> None:
        """
        Méthode permettant de fenmer un fichier de base de donnèes.
        :return: None
        """
        self.connecteur_db.commit()
        self.connecteur_db.close()

    def drop_db(self) -> None:
        """
        Méthode permettant de supprimer un fichier de base de donnèes.
        :return: None
        """
        self.connecteur_db.commit()
        self.connecteur_db.close()
        os.remove(self.chemin_fic)
        self.create_db_fic()

    def make_request(self, requete: str, commit: bool = False) -> list:
        """
        Méthode permettant de faire une requete sur la base de données
        :param requete: Contenu de la requéte sous forme de chaine de caractères
        :param commit: Si la requête insère ou supprime des données, permet la validation de cette requête.
        :return: Retourne le résultat sous forme d'une liste de tuple.
        """
        self.curseur_db.execute(requete)
        row = self.curseur_db.fetchall()

        if commit is True:
            self.connecteur_db.commit()
        return row

    def make_requests(self, requetes: str, commit: bool = False) -> list:
        """
        Méthode permettant de faire une requete sur la base de données
        :param requetes: Contenu des requétes sous forme de chaine de caractères
        :param commit: Si les requêtes insèrent ou suppriment des données, permet la validation de cette requête.
        :return: Retourne le résultat sous forme d'une liste de tuple.
        """
        self.curseur_db.executescript(requetes)
        lignes = self.curseur_db.fetchall()

        if commit is True:
            self.connecteur_db.commit()
        return lignes

    def add_product(self, product: dict) -> None:
        """
        Ajoute un nouveau produit dans la BDD.
        :param product: Informations du produit sous forme de dictionnaire.
        :return: None
        """
        self.curseur_db.execute("SELECT MAX(keyzon) FROM amatable LIMIT 1;")
        max_key = self.curseur_db.fetchone()
        if max_key[0] is None:
            max_key = 1
        else:
            max_key = max_key[0] + 1
        self.curseur_db.execute(self.__req1, [product["nom_produit"], product["note"], product["description"],
                                              product["evaluation"], product["status_produit"],
                                              product["date_creation"]])

        self.curseur_db.execute(self.__req2, [max_key, product["prix"], product["monnaie"], product["date_maj"]])
        self.curseur_db.execute(self.__req3, [max_key, product["url"], product["chemin_image"]])
        self.connecteur_db.commit()

    def remove_product(self, product: dict) -> None:
        """
        Supprime un produit dans la BDD.
        :param product: Informations du produit sous forme de dictionnaire.
        :return: None
        """
        requete = "delete from amatable where nom_produit = '" + product["nom_produit"] + "';"
        self.curseur_db.execute(requete)
        self.connecteur_db.commit()

    def update_product(self, product: dict) -> bool:
        """
        Méthode permettant la mise à jour d'un produit suite à une nouvelle recherche
        :param product: Dictionnaire contenant la liste des informations à mettre à jour
        :return: True si la MAj est faite et False dans le cas contraire
        """
        # Déclarations de variables
        retour = False
        date_maj = datetime.strptime(product["date_maj"], "%d/%m/%Y")
        date_maj_db = ""
        cle_primaire = 0
        recherche1 = "SELECT keyzon, nom_produit FROM amatable WHERE nom_produit = '" + product["nom_produit"] + "';"
        recherche2 = "SELECT keyzon, prix, date_maj FROM tblprix WHERE keyzon = " + str(cle_primaire) + ";"
        ajout_prix = "INSERT INTO tblprix (keyzon, prix, monnaie, date_maj) VALUES(?, ?, ?, ?);"
        maj_produit = "UPDATE amatable SET note = " + str(product["note"]) + ", evaluation = " + str(product["evaluation"]) + " WHERE keyzon = " + str(cle_primaire) + ";"

        # Récupération de la clé primaire
        self.curseur_db.execute(recherche1)
        resultat_recherche1 = self.curseur_db.fetchone()
        cle_primaire = resultat_recherche1[0]

        # Récupération de la date  de dernière MAJ
        self.curseur_db.execute(recherche2)
        resultat_recherche2 = self.curseur_db.fetchall()
        date_maj_db = datetime.strptime(resultat_recherche2[len(resultat_recherche2) - 1][2], "%d/%m/%Y")

        # Mise à jour du produit
        if date_maj_db < date_maj:
            retour = True
            self.curseur_db.execute(maj_produit)
            self.curseur_db.execute(ajout_prix)
            self.connecteur_db.commit()

        # Emvoi du résultat
        return retour

    def export_datas_to_excell(self, chemin_fic: str, product: dict) -> None:
        """
        Exporte un produit dans un fichier au format xlsx.
        :param chemin_fic: Chemin du fichier excel avec l'extension xlsx
        :param product: Informations du produit sous forme de dictionnaire.
        :return: None
        """
        df = pd.DataFrame(data=product)
        df.to_excel(chemin_fic, sheet_name="Export amapy", engine='xlsxwriter',
                    header=True, float_format="%.2f", index=False)

    def export_datas_to_csv(self, chemin_fic: str, product: dict) -> None:
        """
        Exporte un produit dans un fichier au format csv.
        :param chemin_fic: Chemin du fichier excel avec l'extension xlsx
        :param product: Informations du produit sous forme de dictionnaire.
        :return: None
        """
        df = pd.DataFrame(data=product)
        df.to_csv(chemin_fic, header=True, float_format="%.2f", index=False, sep=",")

    def export_products_to_excell(self, chemin_fic: str, list_product: list) -> None:
        """
        Exporte une liste de produit dans un fichier au format xlsx.
        :param chemin_fic: Chemin du fichier excel avec l'extension xlsx
        :param list_product: Informations des produits sous forme d'une liste de dictionnaire.
        :return: None
        """
        if len(list_product) == 1:
            self.export_datas_to_excell(chemin_fic, list_product[0])
        elif len(list_product) > 1:
            df = pd.DataFrame(list_product[0], index=[0])
            for i in range(1, len(list_product)):
                df.loc[i] = list_product[i]

            df.to_excel(chemin_fic, sheet_name="Export amapy", engine='xlsxwriter',
                        header=True, float_format="%.2f", index=False)

    def export_products_to_csv(self, chemin_fic: str, list_product: list) -> None:
        """
        Exporte une liste de produit dans un fichier au format csv.
        :param chemin_fic: Chemin du fichier excel avec l'extension xlsx
        :param list_product: Informations des produits sous forme d'une liste de dictionnaire.
        :return: None
        """
        if len(list_product) == 1:
            self.export_datas_to_csv(chemin_fic, list_product[0])
        elif len(list_product) > 1:
            df = pd.DataFrame(list_product[0], index=[0])
            for i in range(1, len(list_product)):
                df.loc[i] = list_product[i]

            df.to_csv(chemin_fic, header=True, float_format="%.2f", index=False, sep=",")
