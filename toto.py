import os
import shutil
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt

from amazdb import AmazDB

produit = {'status_produit': 'Cet article paraîtra le 19 juillet 2023.',
           'date_creation': date.today().strftime("%d/%m/%Y"),
           'date_maj': date.today().strftime("%d/%m/%Y"),
           'description': 'Description du produit   Boîtier avec fourreauIntégrale '
                          'saison 1 :1.01 - Quand tu es perdu dans les ténèbres (When '
                          "You're Lost in the Darkness)1.02 - Infecté (Infected)1.03 "
                          "- Longtemps... (Long, Long Time)1.04 - S'il te plaît, "
                          'tiens ma main (Please Hold to My Hand)1.05 - Endurer et '
                          'survivre (Endure and Survive)1.06 - Proches (Kin)1.07 - '
                          'Abandonner (Left Behind)1.08 - Quand on est dans le besoin '
                          '(When We Are in Need)1.09 - Cherchez la lumière (Look for '
                          'the Light)   Synopsis   20 ans après la destruction de la '
                          'civilisation moderne, Joel, un survivant endurci, est '
                          'engagé pour faire sortir Ellie, une jeune fille de 14 ans, '
                          "d'une zone de quarantaine oppressante. Ce qui commence "
                          'comme un petit boulot devient rapidement un voyage brutal '
                          "et émouvant alors qu'ils doivent tous deux traverser les "
                          "États-Unis et dépendre l'un de l'autre pour survivre.",
           'evaluation': 31,
           'monnaie': '€',
           'nom_produit': 'The Last of Us-Saison 1',
           'note': 4.6,
           'prix': 39.99,
           'url': 'https://www.amazon.fr/Last-Us-Saison-1-Blu-Ray/dp/B0BV4N5R4J/ref=tmm_blu_title_0?_encoding=UTF8&qid=&sr=',
           'chemin_image': ""}

BDD = AmazDB("/home/Sebastien/Dépots/publique/AmaPy/bdd/toto.db")

product = BDD.make_request("SELECT * FROM amatable WHERE keyzon = 1 or keyzon = 2 or keyzon = 3 or keyzon = 4 or keyzon = 5 or keyzon = 6 or keyzon = 7 or keyzon = 8 or keyzon = 9 or keyzon = 10 or keyzon = 11 or keyzon = 12 or keyzon = 13 or keyzon = 14 or keyzon = 15;")

chemin_export = "/home/Sebastien/Dépots/publique/AmaPy/export"
nom_fic = ""
nom_fic_export = ""
nom_fic_image = ""
rep_export = ""
liste_date = []
liste_prix = []

for j in range(len(product)):
    product_dict = {"Nom du produit": [product[j][1]],
                    "Description du produit": [product[j][3]],
                    "Note": [product[j][2]],
                    "Évaluation": [product[j][4]],
                    "Status du produit": [product[j][5]],
                    "Date de création": [product[j][6]]}

    prix_bdd = BDD.make_request(f"SELECT prix, monnaie, date_maj, chemin_image1 FROM tblprix INNER JOIN tbllink ON tblprix.keyzon = tbllink.keyzon WHERE tblprix.keyzon = {product[j][0]} ORDER by date_maj;")

    df1 = pd.DataFrame(product_dict)

    prix_dict = {"Prix": [prix_bdd[0][0]],
                 "Monnaie": [prix_bdd[0][1]],
                 "Date de mise à jour": [prix_bdd[0][2]]}

    liste_date.append(prix_bdd[0][2][0:5])
    liste_prix.append(prix_bdd[0][0])

    df2 = pd.DataFrame(prix_dict)
    chemin_image_bdd = prix_bdd[0][3]
    if len(prix_bdd) > 1:
        for i in range(1, len(prix_bdd)):
            prix_dict = {"Prix": prix_bdd[i][0],
                         "Monnaie": prix_bdd[i][1],
                         "Date de mise à jour": prix_bdd[i][2]}

            df2.loc[i] = prix_dict
            liste_date.append(prix_bdd[i][2][0:5])
            liste_prix.append(prix_bdd[i][0])

    nom_fic_export = str(product[j][1]).strip().lower().replace(" ", "")[:15] + ".xlsx"
    rep_export = os.path.join(chemin_export, str(product[j][1]).strip().lower().replace(" ", "")[:10])
    nom_fic = os.path.join(rep_export, nom_fic_export)
    nom_image_bdd = os.path.basename(chemin_image_bdd)
    chemin_image = os.path.join(chemin_export, rep_export, nom_image_bdd)
    chemin_graphique = os.path.join(chemin_export, rep_export, "graphique.png")
    try:
        os.mkdir(rep_export)
    except FileExistsError:
        shutil.rmtree(rep_export, ignore_errors=True)
        os.mkdir(rep_export)

    plt.figure(figsize=(40, 5))
    plt.title("Évolution du prix")
    plt.xlabel('Date', fontsize=14, color='red')
    plt.ylabel("Prix en €")
    plt.grid()
    plt.plot(liste_date, liste_prix)

    # Sauvegarde du graphique
    plt.savefig(chemin_graphique)
    liste_date.clear()
    liste_prix.clear()

    try:
        shutil.copy(chemin_image_bdd, chemin_image)
    except FileNotFoundError:
        pass

    with pd.ExcelWriter(nom_fic, date_format="DD-MM-YYYY") as writer:
        df1.to_excel(writer, sheet_name="Produit", engine='xlsxwriter', header=True, float_format="%.2f", index=False)
        df2.to_excel(writer, sheet_name="historique Prix", engine='xlsxwriter', header=True, float_format="%.2f", index=False)
