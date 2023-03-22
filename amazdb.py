import sqlite3
import os



class AmazDB:
    def __init__(self, chemin_fic: str):
        self.chemin_fic = chemin_fic
        self.connecteur_db = None
        self.curseur_db = None

        if os.path.exists(chemin_fic):
            self.open_db_fic()
        else:
            self.create_db_fic()

    def create_db_fic(self) -> None:
        """

        :return:
        """
        self.connecteur_db = sqlite3.connect(self.chemin_fic)
        self.curseur_db = self.connecteur_db.cursor()
        with open(os.path.join("requetes", "createdb.sql"), "r+t", encoding="utf-8") as f:
            requete = f.read()
            self.curseur_db.execute(requete)

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
        with open(os.path.join("requetes", "droptables.sql"), "r+t", encoding="utf-8") as f:
            requete = f.read()
            self.curseur_db.execute(requete)

    def make_request(self, requete: str):
        """

        :param requete:
        :return:
        """
        retour = self.curseur_db.execute(requete)
        self.connecteur_db.commit()
        return retour

    def add_product(self) -> None:
        """

        :return:
        """
        pass

    def remove_product(self) -> None:
        """

        :return:
        """
        pass

    def update_product(self) -> None:
        """

        :return:
        """
        pass

    def update_price(self) -> None:
        """

        :return:
        """
        pass

    def export_datas_to_excell(self, chemin_fic: str) -> None:
        """
        Méthode qui permet de stocker le contenu de la requete
        dans un fichier au format excell
        :param chemin_fic: Chemin du fichier excell
        :return: None
        """
        # Création du dataframe
        d = {}

        self.curseur_db.execute("")

        df = pd.DataFrame(data=d)
        df.to_excel(chemin_fic, sheet_name="Export amapy", engine='xlsxwriter',
                    header=True, float_format="%.2f", index=False)
