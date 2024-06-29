# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tasks.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

from qfluentwidgets import (LineEdit, ListView, PushButton)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(329, 405)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.todoView = ListView(self.centralwidget)
        self.todoView.setObjectName(u"todoView")

        self.verticalLayout.addWidget(self.todoView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.completedButton = PushButton(self.centralwidget)
        self.completedButton.setObjectName(u"completedButton")

        self.horizontalLayout.addWidget(self.completedButton)

        self.deleteButton = PushButton(self.centralwidget)
        self.deleteButton.setObjectName(u"deleteButton")

        self.horizontalLayout.addWidget(self.deleteButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.todoEdit = LineEdit(self.centralwidget)
        self.todoEdit.setObjectName(u"todoEdit")

        self.verticalLayout.addWidget(self.todoEdit)

        self.addButton = PushButton(self.centralwidget)
        self.addButton.setObjectName(u"addButton")

        self.verticalLayout.addWidget(self.addButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 329, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.completedButton.setText(QCoreApplication.translate("MainWindow", u"Task Completed", None))
        self.deleteButton.setText(QCoreApplication.translate("MainWindow", u"Delete Task", None))
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"Add Task", None))
    # retranslateUi

