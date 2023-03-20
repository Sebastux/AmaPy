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
                self.user_agent = {"user-agent": useragent.replace("\n", "")}
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
            price = soup.find("span", attrs={"class": "a-offscreen"}).getText().replace(",", ".").replace("€", "")
            self.article.prix = float(price)
            self.article.monnaie = soup.find("span", attrs={"class": "a-offscreen"}).getText()[-1]
        except AttributeError:
            self.article.prix = 0.0
            self.article.monnaie = "F"

    def get_article_note(self, soup: BeautifulSoup) -> None:
        note_str = soup.find("span", class_="a-icon-alt").getText().strip()
        self.article.note = float(note_str.split()[0].replace(",", "."))

    def get_article_review(self, soup: BeautifulSoup) -> None:
        try:
            result = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).getText().strip().split()[0:2]
            result.remove("évaluations")
            self.article.evaluation = int(''.join(result))
        except AttributeError:
            self.article.evaluation = 0
        except ValueError:
            self.article.evaluation = 0

    def get_article(self, url: str) -> None:
        self.article.url = url
        self.get_user_agent()
        page = requests.get(url=self.article.url, headers=self.user_agent, timeout=5)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")
            self.get_article_name(soup)
            self.get_article_price(soup)
            self.get_article_note(soup)
            self.get_article_review(soup)
            self.article.date_creation = date.today()
            self.article.date_maj = date.today()

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
        }
        return dict_article

