import random
import os
from datetime import date

from bs4 import BeautifulSoup
import requests

from dtcamazon import AmazonDatas


class AmaScrapp:
    def __init__(self):
        self.article = AmazonDatas()
        self.user_agent = ""

    def get_user_agent(self):
        try:
            with open(os.path.join("datas", "user-agents.txt"), "r+t", encoding="utf-8") as f:
                ligne = f.readlines()
                useragent = random.choice(ligne)
                self.user_agent = {"user-agent": useragent.replace("\n", ""),
                                   "Accept-Language": "fr-FR,fr;q=0.5",
                                   "Accept-Encoding": "gzip, deflate, br",
                                   "DNT": "1",
                                   }
        except FileNotFoundError:
            self.user_agent = {"user-agent":
                                   "Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFTT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36"}

    def get_article_name(self, soup: BeautifulSoup) -> None:
        try:
            self.article.nom_produit = soup.find("div", attrs={'id': 'titleSection'}).getText().strip()
        except AttributeError:
            self.article.nom_produit = "Inconnu"

    def get_article_price(self, soup: BeautifulSoup) -> None:
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
        try:
            note_str = soup.find("span", class_="a-icon-alt").getText().strip()
            self.article.note = float(note_str.split()[0].replace(",", "."))
        except:
            self.article.note = 0.0

    def get_article_status(self, soup: BeautifulSoup) -> None:
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
        try:
            result = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).getText().strip().split()[0:2]
            result.remove("évaluations")
            self.article.evaluation = int(''.join(result))
        except AttributeError:
            self.article.evaluation = 0
        except ValueError:
            self.article.evaluation = 0

    def get_article_description(self, soup: BeautifulSoup) -> None:
        self.article.description = soup.find('div', {'id': "productDescription"}).getText().strip()
        if len(self.article.description) == 0:
            self.article.description = "Inconnue"

    def get_article(self, url: str) -> None:
        self.article.url = url
        self.get_user_agent()
        page = requests.get(url=self.article.url, headers=self.user_agent, timeout=5)
        if page.status_code == 200:
            # soup = BeautifulSoup(page.content, "html.parser", from_encoding="utf-8")
            soup = BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
            self.get_article_name(soup)
            self.get_article_price(soup)
            self.get_article_note(soup)
            self.get_article_review(soup)
            self.get_article_status(soup)
            self.get_article_description(soup)
            self.article.date_creation = date.today().strftime("%d/%m/%Y")
            self.article.date_maj = date.today().strftime("%d/%m/%Y")

    def export_to_dict(self):
        dict_article = {
            "url": self.article.url,
            "nom produit": self.article.nom_produit,
            "note": self.article.note,
            "description": self.article.description,
            "evaluation": self.article.evaluation,
            "prix": self.article.prix,
            "monnaie": self.article.monnaie,
            "date creation": self.article.date_creation,
            "date maj": self.article.date_maj,
            "Disponnibilité": self.article.status_produit
        }
        return dict_article

    def export_to_excell(self, chemin_fic: str):
        self.article.export_datas_to_excell(chemin_fic)

    def export_to_csv(self, chemin_fic: str):
        self.article.export_datas_to_csv(chemin_fic)

    def export_to_json(self, chemin_fic: str):
        self.article.export_datas_to_json(chemin_fic)
