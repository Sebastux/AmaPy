from typing import Optional
from dataclasses import dataclass
from  datetime import date
import json

import pandas as pd



@dataclass
class AmazonDatas:
    url: Optional[str] = ""
    nom_produit: Optional[str] = ""
    note: Optional[int] = 0
    description: Optional[str] = ""
    evaluation: Optional[int] = 0
    prix: Optional[float] = 0.0
    monnaie: Optional[str] = "€"
    status_produit: Optional[str] = "OK"
    date_creation: Optional[str] = date.today().strftime("%d/%m/%Y")
    date_maj: Optional[str] = date.today().strftime("%d/%m/%Y")

    def export_datas_to_csv(self, chemin_fic: str):
        # Création du dataframe
        d = {"URL": [self.url], "Nom du produit": [self.nom_produit],
             "Description du produit": [self.description],
             "Note": [self.note], "Évaluation": [self.evaluation],
             "Prix": [self.prix], "Monnaie": [self.monnaie],
             "Status du produit": [self.status_produit],
             "date de création": [self.date_creation],
             "date maj": [self.date_maj]}

        df = pd.DataFrame(data=d)
        df.to_csv(chemin_fic, header=True, sep=',', index=False, encoding="utf-8")

    def export_datas_to_excell(self, chemin_fic: str):
        # Création du dataframe
        d = {"URL": [self.url], "Nom du produit": [self.nom_produit],
             "Description du produit": [self.description],
             "Note": [self.note], "Évaluation": [self.evaluation],
             "Prix": [self.prix], "Monnaie": [self.monnaie],
             "Status du produit": [self.status_produit],
             "date creation": [self.date_creation],
             "date maj": [self.date_maj]}

        df = pd.DataFrame(data=d)
        df.to_excel(chemin_fic, sheet_name="Export amapy", engine='xlsxwriter',
                    float_format="%.2f", index=False)

    def export_datas_to_json(self, chemin_fic: str):
        # Création du dictionnaire
        d = {"URL": self.url, "Nom du produit": self.nom_produit,
             "Description du produit": self.description,
             "Note": self.note, "Évaluation": self.evaluation,
             "Prix": self.prix, "Monnaie": self.monnaie,
             "date creation": self.date_creation,
             "date maj": self.date_maj}

        json_data = json.dumps(d)
        with open(chemin_fic, "w", encoding="utf-8") as f:
            f.write(json_data)

    def import_datas_to_csv(self, chemin_fic: str):
        pass

    def import_datas_to_excell(self, chemin_fic: str):
        pass

    def import_datas_to_json(self, chemin_fic: str):
        pass
