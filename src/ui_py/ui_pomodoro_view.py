# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pomodoro_view.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLayout,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (CardWidget, PillToolButton, ProgressBar, ProgressRing,
    TitleLabel, ToggleToolButton, ToolButton)

class Ui_PomodoroView(object):
    def setupUi(self, PomodoroView):
        if not PomodoroView.objectName():
            PomodoroView.setObjectName(u"PomodoroView")
        PomodoroView.resize(486, 489)
        self.gridLayout = QGridLayout(PomodoroView)
        self.gridLayout.setObjectName(u"gridLayout")
        self.CardWidget = CardWidget(PomodoroView)
        self.CardWidget.setObjectName(u"CardWidget")
        self.verticalLayout = QVBoxLayout(self.CardWidget)
        self.verticalLayout.setSpacing(21)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pomodoroLabel = TitleLabel(self.CardWidget)
        self.pomodoroLabel.setObjectName(u"pomodoroLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pomodoroLabel.sizePolicy().hasHeightForWidth())
        self.pomodoroLabel.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.pomodoroLabel)

        self.topVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.topVerticalSpacer)

        self.ProgressRing = ProgressRing(self.CardWidget)
        self.ProgressRing.setObjectName(u"ProgressRing")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ProgressRing.sizePolicy().hasHeightForWidth())
        self.ProgressRing.setSizePolicy(sizePolicy1)
        self.ProgressRing.setMinimumSize(QSize(220, 220))
        self.ProgressRing.setMaximumSize(QSize(220, 220))
        self.ProgressRing.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.ProgressRing, 0, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(21)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.leftHorizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.leftHorizontalSpacer)

        self.restartButton = PillToolButton(self.CardWidget)
        self.restartButton.setObjectName(u"restartButton")
        self.restartButton.setMinimumSize(QSize(68, 68))
        self.restartButton.setIconSize(QSize(21, 21))
        self.restartButton.setChecked(False)

        self.horizontalLayout.addWidget(self.restartButton)

        self.pauseResumeButton = PillToolButton(self.CardWidget)
        self.pauseResumeButton.setObjectName(u"pauseResumeButton")
        self.pauseResumeButton.setMinimumSize(QSize(68, 68))
        self.pauseResumeButton.setIconSize(QSize(21, 21))
        self.pauseResumeButton.setChecked(False)

        self.horizontalLayout.addWidget(self.pauseResumeButton)

        self.skipButton = PillToolButton(self.CardWidget)
        self.skipButton.setObjectName(u"skipButton")
        self.skipButton.setMinimumSize(QSize(68, 68))
        self.skipButton.setIconSize(QSize(21, 21))
        self.skipButton.setChecked(False)

        self.horizontalLayout.addWidget(self.skipButton)

        self.rightHorizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.rightHorizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.bottomVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.bottomVerticalSpacer)


        self.gridLayout.addWidget(self.CardWidget, 0, 0, 1, 1)


        self.retranslateUi(PomodoroView)

        QMetaObject.connectSlotsByName(PomodoroView)
    # setupUi

    def retranslateUi(self, PomodoroView):
        PomodoroView.setWindowTitle(QCoreApplication.translate("PomodoroView", u"Form", None))
        self.pomodoroLabel.setText(QCoreApplication.translate("PomodoroView", u"Pomodoro", None))
    # retranslateUi

