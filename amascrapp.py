"""
   Module permettant l'extraction et le traitement des données extraite des pages Amazon.
"""

import os
import random
from datetime import date
from PIL import Image

from bs4 import BeautifulSoup
import requests

from dtcamazon import AmazonDatas


class AmaScrapp:
    """
    Classe permettant l'extraction et le traitement des données extraite des pages Amazon.
    """
    def __init__(self):
        self.article = AmazonDatas()
        self.header = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "fr-FR,fr;q=0.5",
                "Connection": "keep-alive",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": "",
                      }

    def get_user_agent(self) -> None:
        """
        Méthode qui permet de choisir un user agent au hasard parmi une liste contenue dans un fichier.
        la méthode met à jour la variable d'instance
        :return: None
        """
        try:
            with open(os.path.join("datas", "user-agents.txt"), "r+t", encoding="utf-8") as f:
                ligne = f.readlines()
                user_agent = random.choice(ligne)
                self.header.update({"User-Agent": user_agent.replace("\n", "")})
        except FileNotFoundError:
            self.header.update({"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0", })
        finally:
            self.header.update({"Referer": self.article.url})

    def get_article_name(self, soup: BeautifulSoup) -> None:
        """
        Méthode qui permet la récupération du nom du produit.
        :param soup: Objet BeautifullSoup permettant la récupération de l'information
        :return: None
        """
        try:
            self.article.nom_produit = soup.find("div", attrs={'id': 'titleSection'}).getText().strip()
        except AttributeError:
            self.article.nom_produit = "Inconnu"

    def get_article_price(self, soup: BeautifulSoup) -> None:
        """
        Méthode qui permet la récupération du prix du produit.
        :param soup: Objet BeautifullSoup permettant la récupération de l'information
        :return: None
        """
        try:
            prix = soup.find("span", attrs={"class": "a-offscreen"}).getText().replace(",", ".")
            self.article.prix = float(prix.replace(prix[-1], ""))
            self.article.monnaie = prix[-1]
        except AttributeError:
            self.article.prix = 0.0
            self.article.monnaie = "F"
        except ValueError:
            self.article.prix = 0.0
            self.article.monnaie = "F"

    def get_article_note(self, soup: BeautifulSoup) -> None:
        """
        Méthode qui permet la récupération de la note du produit.
        :param soup: Objet BeautifullSoup permettant la récupération de l'information
        :return: None
        """
        try:
            note_str = soup.find("span", class_="a-icon-alt").getText().strip()
            self.article.note = float(note_str.split()[0].replace(",", "."))
        except:
            self.article.note = 0.0

    def get_article_status(self, soup: BeautifulSoup) -> None:
        """
        Méthode qui permet la récupération du status du produit.
        :param soup: Objet BeautifullSoup permettant la récupération de l'information
        :return: None
        """
        try:
            available = soup.find("div", attrs={'id': 'availability'})
            if available is not None:
                self.article.status_produit = available.find("span").string.strip().replace(',', '')
            else:
                self.article.status_produit = soup.find("span", attrs={"class": "a-color-price a-text-bold"}).getText().strip()
        except AttributeError:
            self.article.status_produit = "inconnu"
        except ValueError:
            available = soup.find("div", attrs={'id': 'availability'})
            if available is not None:
                self.article.status_produit = available.find("span").string.strip().replace(',', '')
            else:
                self.article.status_produit = soup.find("span", attrs={"class": "a-color-price a-text-bold"}).getText().strip()

    def get_article_review(self, soup: BeautifulSoup) -> None:
        """
        Méthode qui permet la récupération du nombre de note du produit.
        :param soup: Objet BeautifullSoup permettant la récupération de l'information
        :return: None
        """
        try:
            result = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).getText().strip().split()[0:2]
            result.remove("évaluations")
            self.article.evaluation = int(''.join(result))
        except AttributeError:
            self.article.evaluation = 0
        except ValueError:
            self.article.evaluation = 0

    def get_article_description(self, soup: BeautifulSoup) -> None:
        """
        Méthode qui permet la récupération de la description du produit.
        :param soup: Objet BeautifullSoup permettant la récupération de l'information
        :return: None
        """
        try:
            self.article.description = soup.find('div', {'id': "productDescription"}).getText().strip()
            if len(self.article.description) == 0:
                self.article.description = "Inconnue"
        except AttributeError:
            self.article.description = "Inconnue"

    def get_article_image(self, soup: BeautifulSoup, repertoire: str, chemin_ko: str = None) -> None:
        """
        Méthode qui permet la récupération de l'URL de l'image du produit
        :param repertoire: Chemin du répertoire de sauvearde des images..
        :param chemin_ko: Chemin d'une image par défaut en cas d'échec.
        :param soup: Objet BeautifullSoup permettant la récupération de l'information
        :return: None
        """
        balise_image = soup.find("div", class_="imgTagWrapper")

        balise_image_str = str(balise_image.contents)
        debut_url = balise_image_str.find("https")
        fin_url = balise_image_str.find("jpg") + 3
        url = balise_image_str[debut_url:fin_url]

        extension = os.path.splitext(url)[1]
        nom_image = self.article.nom_produit.replace(" ", "").lower()[:15] + extension

        try:
            self.article.chemin_image = os.path.join(repertoire, nom_image)
            img = Image.open(requests.get(url, timeout=5, headers=self.header, stream=True).raw)
            img.save(self.article.chemin_image)
        except Exception as e:
            # e.add_note('Add some information')
            if chemin_ko is not None:
                self.article.chemin_image = chemin_ko
            else:
                self.article.chemin_image = ""
            raise

    def get_article(self, url: str) -> None:
        """
        Méthode qui permet la récupération de l'ensemble des informations du produit
        :param url: url du produit à traiter
        :return: None
        """
        self.article.url = url
        self.get_user_agent()
        page = requests.get(url=self.article.url, headers=self.header, timeout=5)
        if page.status_code == 200:
            # soup = BeautifulSoup(page.content, "html.parser", from_encoding="utf-8")
            soup = BeautifulSoup(page.content, "html.parser", from_encoding="utf-8")
            self.get_article_name(soup)
            self.get_article_price(soup)
            self.get_article_note(soup)
            self.get_article_review(soup)
            self.get_article_status(soup)
            self.get_article_description(soup)
            self.get_article_image(soup, repertoire="/home/Sebastien/Dépots/publique/AmaPy/images/", chemin_ko="/home/Sebastien/Dépots/publique/AmaPy/images/no_image.jpg")
            self.article.date_creation = date.today().strftime("%d/%m/%Y")
            self.article.date_maj = date.today().strftime("%d/%m/%Y")

    def export_to_dict(self) -> dict:
        """
        Méthode permettant l'exportation des données produit seus formede dictionnaire.
        :return: Dictionnaire contenant les informations produit
        """
        dict_article = {
            "url": self.article.url,
            "nom_produit": self.article.nom_produit,
            "note": self.article.note,
            "description": self.article.description,
            "evaluation": self.article.evaluation,
            "prix": self.article.prix,
            "monnaie": self.article.monnaie,
            "date_creation": self.article.date_creation,
            "date_maj": self.article.date_maj,
            "disponnibilité": self.article.status_produit,
            "chemin_image": self.article.chemin_image,
            "status_produit": self.article.status_produit
        }
        return dict_article

    def export_to_excell(self, chemin_fic: str) -> None:
        """
        Méthode permettant l'export de données dans un fichier excell au format xlsx
        :param chemin_fic:  chemin du fichier de destination
        :return: None
        """
        self.article.export_datas_to_excell(chemin_fic)

    def export_to_csv(self, chemin_fic: str) -> None:
        """
        Méthode permettant l'export de données dans un fichier au format csv
        :param chemin_fic:  chemin du fichier de destination
        :return: None
        """
        self.article.export_datas_to_csv(chemin_fic)

    def export_to_json(self, chemin_fic: str) -> None:
        """
        Méthode permettant l'export de données dans un fichier au format json
        :param chemin_fic:  chemin du fichier de destination
        :return: None
        """
        self.article.export_datas_to_json(chemin_fic)
