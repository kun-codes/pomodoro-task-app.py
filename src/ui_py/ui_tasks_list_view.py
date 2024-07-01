# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tasks_list_view.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (CardWidget, ScrollArea, TitleLabel, ToolButton)

class Ui_TaskView(object):
    def setupUi(self, TaskView):
        if not TaskView.objectName():
            TaskView.setObjectName(u"TaskView")
        TaskView.resize(800, 600)
        self.gridLayout = QGridLayout(TaskView)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 10, 10, -1)
        self.ScrollArea = ScrollArea(TaskView)
        self.ScrollArea.setObjectName(u"ScrollArea")
        self.ScrollArea.setAutoFillBackground(True)
        self.ScrollArea.setStyleSheet(u"QScrollArea{background: transparent; border: none}")
        self.ScrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.ScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 780, 581))
        self.scrollAreaWidgetContents.setStyleSheet(u"QWidget{background: transparent}")
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.addTaskButton = ToolButton(self.scrollAreaWidgetContents)
        self.addTaskButton.setObjectName(u"addTaskButton")

        self.horizontalLayout.addWidget(self.addTaskButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.todoTasksLabel = TitleLabel(self.scrollAreaWidgetContents)
        self.todoTasksLabel.setObjectName(u"todoTasksLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.todoTasksLabel.sizePolicy().hasHeightForWidth())
        self.todoTasksLabel.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.todoTasksLabel)

        self.todoTasksCard = CardWidget(self.scrollAreaWidgetContents)
        self.todoTasksCard.setObjectName(u"todoTasksCard")
        self.verticalLayout_2 = QVBoxLayout(self.todoTasksCard)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.verticalLayout.addWidget(self.todoTasksCard)

        self.completedTasksLabel = TitleLabel(self.scrollAreaWidgetContents)
        self.completedTasksLabel.setObjectName(u"completedTasksLabel")
        sizePolicy.setHeightForWidth(self.completedTasksLabel.sizePolicy().hasHeightForWidth())
        self.completedTasksLabel.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.completedTasksLabel)

        self.CardWidget = CardWidget(self.scrollAreaWidgetContents)
        self.CardWidget.setObjectName(u"CardWidget")

        self.verticalLayout.addWidget(self.CardWidget)

        self.ScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.ScrollArea, 0, 0, 1, 1)


        self.retranslateUi(TaskView)

        QMetaObject.connectSlotsByName(TaskView)
    # setupUi

    def retranslateUi(self, TaskView):
        TaskView.setWindowTitle(QCoreApplication.translate("TaskView", u"Form", None))
        self.todoTasksLabel.setText(QCoreApplication.translate("TaskView", u"Todo Tasks", None))
        self.completedTasksLabel.setText(QCoreApplication.translate("TaskView", u"Completed Tasks", None))
    # retranslateUi

