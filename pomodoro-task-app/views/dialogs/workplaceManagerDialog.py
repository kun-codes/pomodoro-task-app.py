import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QMainWindow, QWidget
from loguru import logger
from qfluentwidgets import FluentStyleSheet, PrimaryPushButton, SubtitleLabel, ListView, setCustomStyleSheet, \
    PushButton, LineEdit, InfoBar, InfoBarPosition
from qfluentwidgets.components.dialog_box.mask_dialog_base import MaskDialogBase

from models.db_tables import Workspace
from models.workspace_list_model import WorkspaceListModel


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
        self.addWorkspaceButton.setObjectName('addWorkspaceButton')
        self.addWorkspaceButton.setDisabled(True)
        self.closeDialogButton = PrimaryPushButton()
        self.closeDialogButton.setText('Close Dialog')

        self.titleLabel = SubtitleLabel('Manage Workspaces', parent=None)
        self.newWorkspaceLineEdit = LineEdit()
        self.workspaceList = ListView()
        self.model = WorkspaceListModel()
        self.workspaceList.setModel(self.model)

        self.__initWidget()

    def __initWidget(self):
        self.__setQss()
        self.__initLayout()

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))

        # self.buttonGroup.setFixedHeight(81)
        self.viewLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        self.viewLayout.addWidget(self.workspaceList, 1)
        self.viewLayout.addWidget(self.newWorkspaceLineEdit, 1)

        self.__connectSignalsToSlots()

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

    def __connectSignalsToSlots(self):
        self.closeDialogButton.clicked.connect(lambda: self.close())
        self.addWorkspaceButton.clicked.connect(self.onAddWorkspaceButtonClicked)
        self.deleteWorkspaceButton.clicked.connect(self.onDeleteWorkspaceButtonClicked)

        self.newWorkspaceLineEdit.textChanged.connect(self.onWorkspaceTextChanged)

        self.workspaceList.selectionModel().selectionChanged.connect(self.onWorkplaceSelectionChanged)

    def onWorkspaceTextChanged(self):
        self.addWorkspaceButton.setDisabled(self.newWorkspaceLineEdit.text().strip() == "")

    def onAddWorkspaceButtonClicked(self):
        new_workspace_name = self.newWorkspaceLineEdit.text().strip()
        if new_workspace_name:
            workspace = Workspace(workspace_name=new_workspace_name)
            self.model.add_workspace(workspace)
            self.newWorkspaceLineEdit.clear()

    def onDeleteWorkspaceButtonClicked(self):
        selected_index = self.workspaceList.currentIndex()
        if selected_index.isValid():
            self.model.delete_workspace(selected_index.row())

    def onWorkplaceSelectionChanged(self, selected, deselected):
        selected_index = selected.indexes()
        if selected_index:
            selected_index = selected_index[0]
            workplace_name = self.model.data(selected_index, Qt.ItemDataRole.DisplayRole)
            logger.debug(f"Selected workspace: {workplace_name}")

            infobar = InfoBar.success(
                title=f"{workplace_name} is selected",
                content="",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=4000,
                parent=self.parent()
            )


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
