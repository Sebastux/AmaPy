import sys
import os
from pathlib import Path
import configparser

from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QFileDialog
from PyQt6 import uic

from fonctions_qt import AfficheMessages


class AmapyOptions(QMainWindow):
    """
    Affiche la fenetre d'options de l'application.
    """

    def __init__(self):
        # Appel du construteur de la classe parent
        super().__init__()

        # Initialisation de variables
        self.ui = uic.loadUi(os.path.join("ui", "Amapy_options.ui"), self)
        self.list_extensions = ["jpg", "jpeg", "png", "pdf"]
        self.verif_chemins = [False, False, False]

        # config de la tab par défaut
        self.ui.tabw_options.setCurrentIndex(0)

        # Instenciation de la classe de configuration
        self.config = configparser.ConfigParser(comment_prefixes='#', allow_no_value=True)

        # Déclaration des événements
        self.ui.btn_ok.clicked.connect(self.ok_clicked)
        self.ui.btn_annuler.clicked.connect(self.annuler_clicked)
        self.ui.tbn_bdd.clicked.connect(self.tbn_bdd_clicked)
        self.ui.tbtn_export.clicked.connect(self.tbtn_export_clicked)
        self.ui.tbtn_images.clicked.connect(self.tbtn_images_clicked)

    def setup_window(self) -> None:
        """
        Configure la fenêtre d'options de l'application.
        :return: None
        """
        # Taille fixe pour la fenêtre
        self.setFixedWidth(self.frameGeometry().width())
        self.setFixedHeight(self.frameGeometry().height())

        # Centrage de la fenêtre
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_options(self) -> None:
        """
        Affiche la fenêtre de configuration de l'application.
        :return: None
        """
        # initialisation de la liste des extensions
        self.ui.cbx_extensions.clear()
        self.ui.cbx_extensions.addItems(self.list_extensions)

        # Chargement de la configuration
        self.load_config()

        # Affichage de la fenêtre
        self.show()

    def ok_clicked(self) -> None:
        """
        Sauvegarde les parametres et ferme la fenêtre.
        :return: None
        """
        if self.verif_chemins[0] and self.verif_chemins[1] and self.verif_chemins[2]:
            self.write_config()
            self.close()
        else:
            AfficheMessages("Sauvegarde de la configuration impossible",
                            "Veuillez vérifier les chemins de sauvegarde.", QMessageBox.Icon.Warning,
                            QMessageBox.StandardButton.Ok)

    def annuler_clicked(self) -> None:
        """
        Ferme la fenêtre de configuration sans sauvegardes les options.
        :return: None
        """
        self.close()

    def tbn_bdd_clicked(self) -> None:
        """
        Permet de selectionner le répertoire de la BDD.
        :return: None
        """
        chemin_bdd = QFileDialog.getExistingDirectory(self, "Chemin de sauvegarde de la base de données.")
        if chemin_bdd:
            path = Path(chemin_bdd)
            self.ui.edt_bdd.setText(str(path))
            self.ui.edt_bdd.setStyleSheet("")
            self.verif_chemins[0] = True

    def tbtn_export_clicked(self) -> None:
        """
        Permet de selectionner le répertoire d'export.
        :return: None
        """
        chemin_export = QFileDialog.getExistingDirectory(self, "Chemin de sauvegarde des export.")
        if chemin_export:
            path = Path(chemin_export)
            self.ui.edt_export.setText(str(path))
            self.ui.edt_export.setStyleSheet("")
            self.verif_chemins[1] = True

    def tbtn_images_clicked(self) -> None:
        """
        Permet de selectionner le répertoire d'export des images.
        :return: None
        """
        chemin_images = QFileDialog.getExistingDirectory(self, "Chemin de sauvegarde des images.")
        if chemin_images:
            path = Path(chemin_images)
            self.ui.edt_images.setText(str(path))
            self.ui.edt_images.setStyleSheet("")
            self.verif_chemins[2] = True

    def load_config(self) -> None:
        """
        Charge les parametres de configuration.
        :return: None
        """
        # Déclaration de variables
        rep_courant = os.getcwd()
        option = ""

        # Test de l'éxistance du fichier de configuration
        if not os.path.isfile(os.path.join(rep_courant, "amapy.cfg")):
            AfficheMessages("Information de configuration", "Le fichier de configuration n'existe "
                                                            "pas.\nLes information par défaut seront "
                                                            "utilisés.",
                            QMessageBox.Icon.Information, QMessageBox.StandardButton.Ok)

            self.ui.edt_bdd.setText(os.path.join(rep_courant, "bdd"))
            self.ui.edt_export.setText(os.path.join(rep_courant, "export"))
            self.ui.edt_images.setText(os.path.join(rep_courant, "images"))
            # self.ui.cb_proxy.setCheckState(False)
            return None
        try:
            with open(os.path.join(rep_courant, "amapy.cfg"), "r", encoding="utf-8") as file:
                self.config.read_file(file)

                # Gestion de répertoire de stockage de la BDD
                option = self.config.get("fichier", "bdd", fallback=os.path.join(rep_courant, "bdd"))
                if len(option.strip()) == 0:
                    self.ui.edt_bdd.setText("CHEMIN VIDE")
                    self.ui.edt_bdd.setStyleSheet("QLineEdit"
                                                  "{""background : red;""}")
                    self.verif_chemins[0] = False
                elif not os.path.isdir(option):
                    self.ui.edt_bdd.setText(f"{option} LE RÉPERTOIRE N'EXISTE PAS")
                    self.ui.edt_bdd.setStyleSheet("QLineEdit"
                                                  "{""background : red;""}")
                    self.verif_chemins[0] = False
                else:
                    self.ui.edt_bdd.setText(option.strip())
                    self.verif_chemins[0] = True

                # Gestion de répertoire de stockage des exports
                option = self.config.get("fichier", "export", fallback=os.path.join(rep_courant, "export"))
                if len(option.strip()) == 0:
                    self.ui.edt_export.setText("CHEMIN VIDE")
                    self.ui.edt_export.setStyleSheet("QLineEdit"
                                                     "{""background : red;""}")
                    self.verif_chemins[1] = False
                elif not os.path.isdir(option):
                    self.ui.edt_export.setText(f"{option} LE RÉPERTOIRE N'EXISTE PAS")
                    self.ui.edt_export.setStyleSheet("QLineEdit"
                                                     "{""background : red;""}")
                    self.verif_chemins[1] = False
                else:
                    self.ui.edt_export.setText(option.strip())
                    self.verif_chemins[1] = True

                # Gestion de répertoire de stockage des images
                option = self.config.get("fichier", "images", fallback=os.path.join(rep_courant, "images"))
                if len(option.strip()) == 0:
                    self.ui.edt_images.setText("CHEMIN VIDE")
                    self.ui.edt_images.setStyleSheet("QLineEdit"
                                                     "{""background : red;""}")
                    self.verif_chemins[2] = False

                elif not os.path.isdir(option):
                    self.ui.edt_images.setText(f"{option} LE RÉPERTOIRE N'EXISTE PAS")
                    self.ui.edt_images.setStyleSheet("QLineEdit"
                                                     "{""background : red;""}")
                    self.verif_chemins[2] = False

                else:
                    self.ui.edt_images.setText(option.strip())
                    self.verif_chemins[2] = True

                # Gestion de l'extension des images
                option = self.config.get("fichier", "extension", fallback="jpg")
                if not option.strip() in self.list_extensions:
                    self.ui.cbx_extensions.setCurrentIndex(0)
                else:
                    self.ui.cbx_extensions.setCurrentIndex(self.list_extensions.index(option.strip()))

        except (FileNotFoundError, configparser.NoSectionError, configparser.NoOptionError,
                configparser.MissingSectionHeaderError):
            AfficheMessages("Erreur de chargement du fichier de configuration.",
                            "Une erreur s'est produite lors du chargemend du fichier de configuration. Veuillez vérifier le contenu du fichier ou le supprimer.",
                            QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok)
        except ValueError:
            AfficheMessages("Erreur de chargement du fichier de configuration.",
                            "L'un des paramètres numériques est incorrecte. Utilisation des valeurs par défaut.",
                            QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok)

    def write_config(self) -> None:
        # Déclaration de variables
        rep_courant = os.getcwd()
        nom_config = os.path.join(rep_courant, "amapy.cfg")
        try:
            if not self.config.has_section("fichier"):
                self.config.add_section("fichier")
            if not self.config.has_section("reseau"):
                self.config.add_section("reseau")
            with open(nom_config, "w", encoding="utf-8") as file:
                self.config.set("fichier", "bdd", self.ui.edt_bdd.text())
                self.config.set("fichier", "export", self.ui.edt_export.text())
                self.config.set("fichier", "images", self.ui.edt_images.text())
                self.config.set("fichier", "extension", self.ui.cbx_extensions.currentText())
                self.config.set("reseau", "proxy", "false")
                self.config.write(file)
        except (FileNotFoundError, PermissionError):
            AfficheMessages("Erreur d'écriture du fichier",
                            "Une erreur s'est produite lors de la sauvegarde des paramètres.",
                            QMessageBox.Icon.Critical, QMessageBox.StandardButton.Ok)

    def get_chemin_export(self) -> str:
        self.load_config()
        return self.ui.edt_export.text()

    def get_chemin_bdd(self) -> str:
        self.load_config()
        return self.ui.edt_bdd.text()

    def get_chemin_images(self) -> str:
        self.load_config()
        return self.ui.edt_images.text()


def main() -> None:
    """
    Fonction principale de l'application.
    :return: None
    """
    app = QApplication(sys.argv)
    options = AmapyOptions()
    options.setup_window()
    options.show_options()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
