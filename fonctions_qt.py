from PyQt6.QtWidgets import QMessageBox


def AfficheMessages(titre: str, texte: str, icone: QMessageBox.Icon, boutons: QMessageBox.StandardButton):
    msgBox = QMessageBox()
    msgBox.setIcon(icone)
    msgBox.setText(texte)
    msgBox.setWindowTitle(titre)
    msgBox.setStandardButtons(boutons)
    return msgBox.exec()
