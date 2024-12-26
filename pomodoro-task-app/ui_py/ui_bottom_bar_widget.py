# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bottom_bar_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QSpacerItem,
    QWidget)

from qfluentwidgets import (PillToolButton, StrongBodyLabel, ToggleToolButton, ToolButton)

class Ui_BottomBarWidget(object):
    def setupUi(self, BottomBarWidget):
        if not BottomBarWidget.objectName():
            BottomBarWidget.setObjectName(u"BottomBarWidget")
        BottomBarWidget.resize(778, 52)
        self.horizontalLayout = QHBoxLayout(BottomBarWidget)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(12, 12, 12, 12)
        self.spacer = QSpacerItem(48, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.spacer)

        self.taskLabel = StrongBodyLabel(BottomBarWidget)
        self.taskLabel.setObjectName(u"taskLabel")

        self.horizontalLayout.addWidget(self.taskLabel)

        self.stopButton = PillToolButton(BottomBarWidget)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stopButton.sizePolicy().hasHeightForWidth())
        self.stopButton.setSizePolicy(sizePolicy)
        self.stopButton.setMinimumSize(QSize(34, 34))
        self.stopButton.setMaximumSize(QSize(34, 34))
        self.stopButton.setIconSize(QSize(16, 16))
        self.stopButton.setChecked(False)

        self.horizontalLayout.addWidget(self.stopButton)

        self.pauseResumeButton = PillToolButton(BottomBarWidget)
        self.pauseResumeButton.setObjectName(u"pauseResumeButton")
        self.pauseResumeButton.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pauseResumeButton.sizePolicy().hasHeightForWidth())
        self.pauseResumeButton.setSizePolicy(sizePolicy)
        self.pauseResumeButton.setMinimumSize(QSize(34, 34))
        self.pauseResumeButton.setMaximumSize(QSize(34, 34))
        self.pauseResumeButton.setIconSize(QSize(16, 16))
        self.pauseResumeButton.setChecked(False)

        self.horizontalLayout.addWidget(self.pauseResumeButton)

        self.skipButton = PillToolButton(BottomBarWidget)
        self.skipButton.setObjectName(u"skipButton")
        self.skipButton.setMinimumSize(QSize(34, 34))
        self.skipButton.setMaximumSize(QSize(34, 34))
        self.skipButton.setIconSize(QSize(16, 16))
        self.skipButton.setChecked(False)

        self.horizontalLayout.addWidget(self.skipButton)

        self.timerLabel = StrongBodyLabel(BottomBarWidget)
        self.timerLabel.setObjectName(u"timerLabel")
        self.timerLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.timerLabel)


        self.retranslateUi(BottomBarWidget)

        QMetaObject.connectSlotsByName(BottomBarWidget)
    # setupUi

    def retranslateUi(self, BottomBarWidget):
        BottomBarWidget.setWindowTitle(QCoreApplication.translate("BottomBarWidget", u"Form", None))
        self.taskLabel.setText(QCoreApplication.translate("BottomBarWidget", u"Strong body label", None))
        self.timerLabel.setText(QCoreApplication.translate("BottomBarWidget", u"Strong body label", None))
    # retranslateUi

