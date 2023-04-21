# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Amapy_licence_frm.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QPlainTextEdit,
    QSizePolicy, QWidget)

class Ui_Frm_Licence(object):
    def setupUi(self, Frm_Licence):
        if not Frm_Licence.objectName():
            Frm_Licence.setObjectName(u"Frm_Licence")
        Frm_Licence.setWindowModality(Qt.ApplicationModal)
        Frm_Licence.resize(589, 468)
        icon = QIcon()
        icon.addFile(u"Icones/Amazon.ico", QSize(), QIcon.Normal, QIcon.Off)
        Frm_Licence.setWindowIcon(icon)
        Frm_Licence.setLayoutDirection(Qt.LeftToRight)
        self.cw_licence = QWidget(Frm_Licence)
        self.cw_licence.setObjectName(u"cw_licence")
        self.cw_licence.setFocusPolicy(Qt.ClickFocus)
        self.cw_licence.setAutoFillBackground(False)
        self.gridLayout_2 = QGridLayout(self.cw_licence)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gl_licence = QGridLayout()
        self.gl_licence.setSpacing(0)
        self.gl_licence.setObjectName(u"gl_licence")
        self.ptedt_licence = QPlainTextEdit(self.cw_licence)
        self.ptedt_licence.setObjectName(u"ptedt_licence")
        self.ptedt_licence.setEnabled(True)

        self.gl_licence.addWidget(self.ptedt_licence, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gl_licence, 0, 0, 1, 1)

        Frm_Licence.setCentralWidget(self.cw_licence)

        self.retranslateUi(Frm_Licence)

        QMetaObject.connectSlotsByName(Frm_Licence)
    # setupUi

    def retranslateUi(self, Frm_Licence):
        Frm_Licence.setWindowTitle(QCoreApplication.translate("Frm_Licence", u"Licence Amapy", None))
    # retranslateUi

