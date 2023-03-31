"""
rsaurisaunrsan
"""

from datetime import date
import random

from amazdb import AmazDB
from amascrapp import AmaScrapp

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
           'chemin_image': "/home/Sebastien/Dépots/publique/AmaPy/images/no_image.jpg"}

bdd = AmazDB("/home/Sebastien/Dépots/publique/AmaPy/bdd/toto.db")
bdd.drop_db()
amazon = AmaScrapp()

for i in range(100):
    produit.update({'nom_produit': f"produit {i + 1}",
                    'evaluation': random.randint(0, 100000),
                    'note': round(random.uniform(0, 5), 2),
                    'prix': round(random.uniform(1, 100), 2), })
    bdd.add_product(produit)

produit = {'status_produit': 'Dispo.',
           'date_creation': date.today().strftime("%d/%m/%Y"),
           'date_maj': date.today().strftime("%d/%m/%Y"),
           'description': "Petit produit de test histoire de",
           'evaluation': random.randint(0, 100000),
           'monnaie': '€',
           'nom_produit': 'produit de ouf guedin',
           'note': round(random.uniform(0, 5), 2),
           'prix': 10000,
           'url': 'https://www.amazon.fr/oufguedin',
           'chemin_image': "/home/Sebastien/Dépots/publique/AmaPy/images/no_image.jpg"}
bdd.add_product(produit)

amazon.get_article("https://www.amazon.fr/Cyclonic-Aspirateur-Performant-Silencieux-Accessoires/dp/B0845GMBC9?ref_=Oct_DLandingS_D_a2171984_61")
prod = amazon.export_to_dict()
bdd.add_product(prod)
for i in range(1, 11):
    for j in range(1, 31):
        bdd.make_request(f"INSERT INTO tblprix (keyzon, prix, monnaie, date_maj) VALUES({i}, {round(random.uniform(1.00, 400.00), 2)}, '€', '{str(j).zfill(2)}/03/2023');", True)

for j in range(1, 5):
    bdd.make_request(
        f"INSERT INTO tblprix (keyzon, prix, monnaie, date_maj) VALUES(12, {round(random.uniform(1.00, 400.00), 2)}, '€', '{str(j).zfill(2)}/03/2023');", True)

for j in range(1, 10):
    bdd.make_request(
        f"INSERT INTO tblprix (keyzon, prix, monnaie, date_maj) VALUES(13, {round(random.uniform(1.00, 400.00), 2)}, '€', '{str(j).zfill(2)}/03/2023');", True)

for j in range(1, 15):
    bdd.make_request(f"INSERT INTO tblprix (keyzon, prix, monnaie, date_maj) VALUES(14, {round(random.uniform(1.00, 400.00), 2)}, '€', '{str(j).zfill(2)}/03/2023');", True)

for j in range(1, 20):
    bdd.make_request(f"INSERT INTO tblprix (keyzon, prix, monnaie, date_maj) VALUES(15, {round(random.uniform(1.00, 400.00), 2)}, '€', '{str(j).zfill(2)}/03/2023');", True)
bdd.close_connection()
