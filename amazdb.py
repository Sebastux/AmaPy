# -*- coding: utf-8 -*-
import json
import os
import sqlite3
import shutil
from datetime import datetime
from typing import Dict, List, Tuple
import pandas as pd
import matplotlib.pyplot as plt


class AmazDB:
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

    def create_db_fic(self) -> None:
        self.connecteur_db = sqlite3.connect(self.chemin_fic)
        self.curseur_db = self.connecteur_db.cursor()
        with open(os.path.join("requetes", "createdb.sql"), "r+t", encoding="utf-8") as f:
            requete = f.read()
            self.curseur_db.executescript(requete)

    def open_db_fic(self) -> None:
        self.connecteur_db = sqlite3.connect(self.chemin_fic)
        self.curseur_db = self.connecteur_db.cursor()

    def close_connection(self) -> None:
        self.connecteur_db.commit()
        self.connecteur_db.close()

    def drop_db(self) -> None:
        self.connecteur_db.commit()
        self.connecteur_db.close()
        os.remove(self.chemin_fic)
        self.create_db_fic()

    def make_request(self, requete: str, commit: bool = False) -> List[Tuple]:
        self.curseur_db.execute(requete)
        row = self.curseur_db.fetchall()

        if commit is True:
            self.connecteur_db.commit()
        return row

    def make_requests(self, requetes: str, commit: bool = False) -> List[Tuple]:
        self.curseur_db.executescript(requetes)
        lignes = self.curseur_db.fetchall()

        if commit is True:
            self.connecteur_db.commit()
        return lignes

    def add_product(self, product: Dict) -> None:
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

    def remove_product(self, product: Dict) -> None:
        requete = "delete from amatable where nom_produit = '" + product["nom_produit"] + "';"
        self.curseur_db.execute(requete)
        self.connecteur_db.commit()

    def update_product(self, product: Dict) -> bool:
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

        # Récupération de la date de dernière MAJ
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

    def export_datas_to_excell(self, chemin_exp: str, product_list: List) -> bool:
        # Déclaration de variables
        requete = ""
        product = ""
        chemin_export = chemin_exp
        nom_fic = ""
        nom_fic_export = ""
        rep_export = ""
        liste_date = []
        liste_prix = []

        # Vérification de l'exstance du répertoire de sortie
        if not os.path.isdir(chemin_export):
            return False

        # Test de la taille de la liste et création de la requête
        if len(product_list) == 0:
            return False
        elif len(product_list) == 1:
            requete = f"SELECT * FROM amatable WHERE nom_produit = '{product_list[0]}';"
        elif len(product_list) > 1:
            requete = f"SELECT * FROM amatable WHERE nom_produit = '{product_list[0]}'"
            for i in range(1, len(product_list)):
                requete += f" OR nom_produit = '{product_list[i]}'"
            requete += " ORDER by keyzon;"

        # Exécution de la requête
        product = self.make_request(requete)
        for j in range(len(product)):
            product_dict = {"Nom du produit": [product[j][1]],
                            "Note": [product[j][2]],
                            "Évaluation": [product[j][4]],
                            "Status du produit": [product[j][5]],
                            "Date de création": [datetime.strptime(product[j][6], "%d/%m/%Y").date()],
                            "Description du produit": [product[j][3]]}

            requete = f"SELECT prix, monnaie, date_maj, chemin_image1 FROM tblprix INNER JOIN tbllink ON tblprix.keyzon = tbllink.keyzon WHERE tblprix.keyzon = {product[j][0]} ORDER by date_maj;"
            prix_bdd = self.make_request(requete)

            df1 = pd.DataFrame(product_dict)

            # "Date de mise à jour": [datetime.strptime(prix_bdd[0][2], "%d/%m/%Y").date()],
            prix_dict = {"Date de mise à jour": [datetime.strptime(prix_bdd[0][2], "%d/%m/%Y").date()],
                         "Prix": [prix_bdd[0][0]],
                         "Monnaie": [prix_bdd[0][1]]}

            liste_date.append(prix_bdd[0][2][0:5])
            liste_prix.append(prix_bdd[0][0])

            df2 = pd.DataFrame(prix_dict)
            chemin_image_bdd = prix_bdd[0][3]
            if len(prix_bdd) > 1:
                for i in range(1, len(prix_bdd)):
                    prix_dict = {"Prix": float(prix_bdd[i][0]),
                                 "Monnaie": prix_bdd[i][1],
                                 "Date de mise à jour": datetime.strptime(prix_bdd[i][2], "%d/%m/%Y").date()}

                    df2.loc[i] = prix_dict
                    liste_date.append(prix_bdd[i][2][0:5])
                    liste_prix.append(prix_bdd[i][0])

            nom_fic_export = str(product[j][1]).strip().lower().replace(" ", "")[:15] + ".xlsx"
            rep_export = os.path.join(chemin_export, str(product[j][1]).strip().lower().replace(" ", "")[:10])
            nom_fic = os.path.join(rep_export, nom_fic_export)
            nom_image_bdd = os.path.basename(chemin_image_bdd)
            chemin_image = os.path.join(chemin_export, rep_export, nom_image_bdd)
            try:
                os.mkdir(rep_export)
            except FileExistsError:
                shutil.rmtree(rep_export, ignore_errors=True)
                os.mkdir(rep_export)

            liste_date.clear()
            liste_prix.clear()

            try:
                shutil.copy(chemin_image_bdd, chemin_image)
            except FileNotFoundError:
                pass

            # Configusation du type des colones du DataFrame  "Date de création": "datetime64[ns]",
            df1 = df1.astype({'Note': 'float16', "Évaluation": "int64",
                              "Nom du produit": "string", "Status du produit": "string", "Description du produit": "string"})
            df2 = df2.astype({"Prix": "float32", "Monnaie": "string"}).sort_values(by="Date de mise à jour", ascending=True)

            # Écriture du fichier
            with pd.ExcelWriter(nom_fic, mode="w", date_format="DD/MM/YYYY") as writer:
                df1.to_excel(writer, sheet_name="Produit", engine='xlsxwriter', header=True, float_format="%.2f", index=False)
                df2.to_excel(writer, sheet_name="historique Prix", engine='xlsxwriter', header=True, float_format="%.2f", index=False)
        return True

    def export_datas_to_csv(self, chemin_exp: str, product_list: List) -> bool:
        # Déclaration de variables
        requete = ""
        chemin_export = chemin_exp
        nom_fic = "export_amapy.csv"
        liste_date = []
        df: pd.DataFrame = pd.DataFrame()

        # Vérification de l'exstance du répertoire de sortie
        if not os.path.isdir(chemin_export):
            return False

        # Test de la taille de la liste et création de la requête
        if len(product_list) == 0:
            return False

        if len(product_list) == 1:
            requete = f"SELECT * FROM amatable WHERE nom_produit = '{product_list[0]}';"
        elif len(product_list) > 1:
            requete = f"SELECT * FROM amatable WHERE nom_produit = '{product_list[0]}'"
            for i in range(1, len(product_list)):
                requete += f" OR nom_produit = '{product_list[i]}'"
            requete += " ORDER by keyzon;"

        # Exécution de la requête et récupération des données
        product = self.make_request(requete)
        for i in range(len(product)):
            product_dict = {"Nom du produit": product[i][1],
                            "Note":  product[i][2],
                            "Évaluation": product[i][4],
                            "Status du produit": product[i][5],
                            "Date de création": product[i][6]}

        # Récupération du dernier prix en date
            requete_prix = f"SELECT date_maj, prix, monnaie FROM tblprix WHERE keyzon = '{product[i][0]}';"
            prix_bdd = self.make_request(requete_prix)
            for j in range(len(prix_bdd)):
                liste_date.append(datetime.strptime(prix_bdd[j][0], "%d/%m/%Y").date())

            date_str = datetime.strftime(sorted(liste_date)[0], '%d/%m/%Y')
            requete_prix = f"SELECT date_maj, prix, monnaie FROM tblprix WHERE keyzon = {product[i][0]} AND date_maj = '{date_str}';"
            prix_bdd = self.make_request(requete_prix)
            # product_dict.update({"Date de mise à jour": datetime.strptime(prix_bdd[0][0], "%d/%m/%Y").date()})
            product_dict.update({"Date de mise à jour": prix_bdd[0][0]})
            product_dict.update({"Prix du produit": prix_bdd[0][1]})
            product_dict.update({"Monnaie": prix_bdd[0][2]})
            product_dict.update({"Description du produit": product[i][3]})

        # Création du dataframe
            if i == 0:
                df = pd.DataFrame([product_dict])
                # df.style.format(precision=2, decimal=",")
            else:
                # df.loc[i] = copy.deepcopy(product_dict)
                df.loc[i] = product_dict

        # Réinitialisation de la liste
            liste_date.clear()

        # Création du fichier csv
        df = df.astype({"Prix du produit": 'float', 'Note': 'float', "Évaluation": "int", "Date de mise à jour": "datetime64[ns]", "Date de création": "datetime64[ns]"})
        df.to_csv(os.path.join(chemin_export, nom_fic), header=True, index=False, sep=",", date_format="%d/%m/%Y",
                  mode="w", encoding="utf-8", decimal=",", float_format="%.2f")
        return True

    def export_datas_to_json(self, chemin_exp: str, product_list: List) -> bool:
        # Déclaration de variables
        requete = ""
        dict_prix = {}
        product_json = ""

        # Vérification de l'exstance du répertoire de sortie
        if not os.path.isdir(chemin_exp):
            return False

        # Test de la taille de la liste et création de la requête
        if len(product_list) == 0:
            return False

        if len(product_list) == 1:
            requete = f"SELECT * FROM amatable WHERE nom_produit = '{product_list[0]}';"
        elif len(product_list) > 1:
            requete = f"SELECT * FROM amatable WHERE nom_produit = '{product_list[0]}'"
            for i in range(1, len(product_list)):
                requete += f" OR nom_produit = '{product_list[i]}'"
            requete += " ORDER by keyzon;"

        # Exécution de la requête et récupération des données
        product = self.make_request(requete)
        for i in range(len(product)):
            product_dict = {"NomDuProduit": product[i][1],
                            "Note":  product[i][2],
                            "Evaluation": product[i][4],
                            "StatusDuProduit": product[i][5],
                            "DateDeCreation": product[i][6],
                            "DescriptionDuProduit": product[i][3]}

            requete_prix = f"SELECT date_maj, prix, monnaie FROM tblprix WHERE keyzon = {product[i][0]};"
            prix_bdd = self.make_request(requete_prix)

            for j in range(len(prix_bdd)):
                prix_str = str(prix_bdd[j][1]) + prix_bdd[j][2]
                dict_prix.update({prix_bdd[j][0]: prix_str})

            product_dict.update({"ListeDesPrix": dict_prix})
            product_json = json.dumps(product_dict, indent=4)
            try:
                nom_fic_export = str(product[i][1]).strip().lower().replace(" ", "")[:15] + ".json"
            except IndexError:
                nom_fic_export = str(product[i][1]).strip().lower().replace(" ", "") + ".json"
            nom_fic = os.path.join(chemin_exp, nom_fic_export)
            with open(nom_fic, "w", encoding="utf-8") as f:
                f.write(product_json)

            product_dict.clear()
            dict_prix.clear()

        return True

    def create_product_graph(self, chemin_export: str, product_id: int, extension: str = "jpg" | "png" | "pdf") -> bool:
        pass
