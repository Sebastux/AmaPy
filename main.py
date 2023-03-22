from amascrapp import AmaScrapp
import pprint


def main():
    produit = AmaScrapp()
    produit.get_article("https://www.amazon.fr/Last-Us-Saison-1-Blu-Ray/dp/B0BV4N5R4J/ref=tmm_blu_title_0?_encoding=UTF8&qid=&sr=")
    toto = produit.export_to_dict()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(toto)


if __name__ == "__main__":
    main()
