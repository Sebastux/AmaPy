import sqlite3
import os

import pandas as pd


class AmazDB:
    def __init__(self, chemin_fic: str):
        # Création des requêtes
        self.__req1 = "INSERT INTO amatable (nom_produit, note, description, evaluation, \
                      status_produit, date_creation, url) VALUES(?, ?, ?, ?, ?, ?, ?);"

        self.__req2 = "INSERT INTO tblprix (keyzon, prix, monnaie, date_maj) VALUES(?, ?, ?, ?);"

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

        :return:
        """
        self.connecteur_db = sqlite3.connect(self.chemin_fic)
        self.curseur_db = self.connecteur_db.cursor()
        with open(os.path.join("requetes", "createdb.sql"), "r+t", encoding="utf-8") as f:
            requete = f.read()
            self.curseur_db.executescript(requete)

    def open_db_fic(self) -> None:
        """

        :return:
        """
        self.connecteur_db = sqlite3.connect(self.chemin_fic)
        self.curseur_db = self.connecteur_db.cursor()

    def close_connection(self) -> None:
        """

        :return:
        """
        self.connecteur_db.commit()
        self.connecteur_db.close()

    def drop_db(self) -> None:
        """

        :return:
        """
        self.connecteur_db.commit()
        self.connecteur_db.close()
        os.remove(self.chemin_fic)
        self.create_db_fic()

    def make_request(self, requete: str, commit: bool = False):
        """

        :param requete:
        :param commit:
        :return:
        """
        self.curseur_db.execute(requete)
        row = self.curseur_db.fetchone()

        if commit is True:
            self.connecteur_db.commit()
        return row

    def make_requests(self, requetes: str, commit: bool = False):
        """

        :param requetes:
        :param commit:
        :return:
        """
        self.curseur_db.executescript(requetes)
        row = self.curseur_db.fetchone()

        if commit is True:
            self.connecteur_db.commit()
        return row

    def add_product(self, product: dict) -> None:
        """

        :param product:
        :return:
        """
        self.curseur_db.execute("SELECT MAX(keyzon) FROM amatable LIMIT 1;")
        max_key = self.curseur_db.fetchone()
        if max_key[0] is None:
            max_key = 1
        else:
            max_key = max_key[0] + 1
        self.curseur_db.execute(self.__req1, [product["nom produit"], product["note"], product["description"],
                                              product["evaluation"], product["status_produit"],
                                              product["date_creation"], product["url"]])

        self.curseur_db.execute(self.__req2, [max_key, product["prix"], product["monnaie"], product["date_maj"]])
        self.connecteur_db.commit()

    def remove_product(self, product: dict) -> None:
        """

        :return:
        """

    def update_product(self, product: dict) -> None:
        """

        :return:
        """

    def update_price(self, product: dict) -> None:
        """

        :param product:
        :return:
        """

    def export_datas_to_excell(self, chemin_fic: str, product: dict) -> None:
        """

        :param chemin_fic:
        :param product:
        :return:
        """
        df = pd.DataFrame(data=product)
        df.to_excel(chemin_fic, sheet_name="Export amapy", engine='xlsxwriter',
                    header=True, float_format="%.2f", index=False)

    def export_datas_to_csv(self, chemin_fic: str, product: dict) -> None:
        """

        :param chemin_fic:
        :param product:
        :return:
        """
        df = pd.DataFrame(data=product)
        df.to_csv(chemin_fic, header=True, float_format="%.2f", index=False, sep=",")

    def export_products_to_excell(self, chemin_fic: str, list_product: list) -> None:
        """

        :param chemin_fic:
        :param list_product:
        :return:
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

        :param chemin_fic:
        :param list_product:
        :return:
        """

        if len(list_product) == 1:
            self.export_datas_to_csv(chemin_fic, list_product[0])
        elif len(list_product) > 1:
            df = pd.DataFrame(list_product[0], index=[0])
            for i in range(1, len(list_product)):
                df.loc[i] = list_product[i]

            df.to_csv(chemin_fic, header=True, float_format="%.2f", index=False, sep=",")
