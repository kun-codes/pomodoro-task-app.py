# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_view.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            Qt)
from PySide6.QtWidgets import (QScrollArea, QSizePolicy, QVBoxLayout,
                               QWidget)

from qfluentwidgets import TitleLabel


class Ui_SettingsView(object):
    def setupUi(self, SettingsView):
        if not SettingsView.objectName():
            SettingsView.setObjectName(u"SettingsView")
        SettingsView.resize(648, 591)
        self.verticalLayout = QVBoxLayout(SettingsView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(SettingsView)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"QScrollArea{background: transparent; border: none}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 630, 573))
        self.scrollAreaWidgetContents.setStyleSheet(u"QWidget{background: transparent}")
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.TitleLabel = TitleLabel(self.scrollAreaWidgetContents)
        self.TitleLabel.setObjectName(u"TitleLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TitleLabel.sizePolicy().hasHeightForWidth())
        self.TitleLabel.setSizePolicy(sizePolicy)
        self.TitleLabel.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_2.addWidget(self.TitleLabel, 0, Qt.AlignmentFlag.AlignTop)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(SettingsView)

        QMetaObject.connectSlotsByName(SettingsView)

    # setupUi

    def retranslateUi(self, SettingsView):
        SettingsView.setWindowTitle(QCoreApplication.translate("SettingsView", u"Form", None))
        self.TitleLabel.setText(QCoreApplication.translate("SettingsView", u"Settings", None))
    # retranslateUi
