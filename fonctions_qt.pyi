from PyQt6.QtWidgets import QMessageBox

"""
Collection de fonctions pour des classes utillisant qt6.
"""


def AfficheMessages(titre: str, texte: str, icone: QMessageBox.Icon, boutons: QMessageBox.StandardButton) -> None:
    """
    Fonction d'affichage des QMessageBox.
    :param titre: Titre de la boite de dialogue
    :param texte: Message de la boite de dialogue
    :param icone: Variable permettant de préciser le tvpe de message. La variable peut avoir les valeurs suivantes :
    QMessageBox.Icon.Question, QMessageBox.Icon.Information, QMessageBox.Icon.Warning, QMessageBox.Icon.Critical.
    :param boutons: Liste des boutons de la boite de dialogue. En cas d'utillisation de plusieurs boutons, il faut
           séparer les boutons par un pipe. Les boutons peuvent avoir la valeur suivante :
           QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes,
           QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Abort,
           QMessageBox.StandardButton.open, QMessageBox.StandardButton.Retry, QMessageBox.StandardButton.Ignore,
           QMessageBox.StandardButton.Save, QMessageBox.StandardButton.Retry, QMessageBox.StandardButton.Apply,
           QMessageBox.StandardButton.Help, QMessageBox.StandardButton.Reset, QMessageBox.StandardButton.SaveAll,
           QMessageBox.StandardButton.YesToAll, QMessageBox.StandardButton.NoToAll
    :return: None
    """