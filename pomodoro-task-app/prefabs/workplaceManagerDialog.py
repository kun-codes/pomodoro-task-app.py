import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QMainWindow, QWidget, \
    QListWidgetItem

from qfluentwidgets import FluentStyleSheet, PrimaryPushButton, SubtitleLabel, ListWidget, setCustomStyleSheet, \
    PushButton
from qfluentwidgets.components.dialog_box.mask_dialog_base import MaskDialogBase


class ManageWorkspaceDialog(MaskDialogBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.buttonGroup = QFrame(self.widget)

        # contains both self.viewLayout and self.buttonLayout
        self.vBoxLayout = QVBoxLayout(self.widget)

        self.viewLayout = QVBoxLayout()
        self.buttonLayout = QVBoxLayout(self.buttonGroup)

        # initializing buttons
        self.deleteWorkspaceButton = PushButton()
        self.deleteWorkspaceButton.setText('Delete Workspace')
        self.addWorkspaceButton = PushButton()
        self.addWorkspaceButton.setText('Add Workspace')
        self.closeDialogButton = PrimaryPushButton()
        self.closeDialogButton.setText('Close Dialog')

        self.titleLabel = SubtitleLabel('Manage Workspaces', parent=None)
        self.workspaceList = ListWidget()

        self.__initWidget()

    def __initWidget(self):
        self.__setQss()
        self.__initLayout()

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))

        # self.buttonGroup.setFixedHeight(81)
        self.viewLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        self.viewLayout.addWidget(self.workspaceList, 1, Qt.AlignCenter)

    def __initLayout(self):
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.viewLayout, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, Qt.AlignBottom)

        self.viewLayout.setSpacing(12)
        self.viewLayout.setContentsMargins(24, 24, 24, 24)

        self.buttonLayout.setSpacing(12)
        self.buttonLayout.setContentsMargins(24, 24, 24, 24)

        self.buttonLayout.addWidget(self.deleteWorkspaceButton, 1, Qt.AlignVCenter)
        self.buttonLayout.addWidget(self.addWorkspaceButton, 1, Qt.AlignVCenter)
        self.buttonLayout.addWidget(self.closeDialogButton, 1, Qt.AlignVCenter)

        # self.buttonLayout.addWidget(self.yesButton, 1, Qt.AlignVCenter)
        # self.buttonLayout.addWidget(self.cancelButton, 1, Qt.AlignVCenter)

    def __setQss(self):
        self.buttonGroup.setObjectName('buttonGroup')
        qss = f"""
            {__class__.__name__} #buttonGroup,
            {__class__.__name__} #buttonGroup {{
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
        }}
        """
        FluentStyleSheet.DIALOG.apply(self)

        # from: https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/707
        self.style().unpolish(self)
        self.style().polish(self)

        # setStyleSheet()
        setCustomStyleSheet(self, qss, qss)


if __name__ == '__main__':
    # create a mainwindow

    app = QApplication(sys.argv)

    window = QMainWindow()

    central_widget = QWidget()
    layout = QHBoxLayout(central_widget)
    btn = QPushButton("Open dialog")
    layout.addWidget(btn)
    window.setCentralWidget(central_widget)
    window.show()

    btn.clicked.connect(lambda: ManageWorkspaceDialog(window).show())

    sys.exit(app.exec())
