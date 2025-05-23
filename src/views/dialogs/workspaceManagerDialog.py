import sys

from loguru import logger
from PySide6.QtCore import QItemSelectionModel, Qt
from PySide6.QtGui import QColor, QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import (
    FluentStyleSheet,
    InfoBar,
    InfoBarPosition,
    LineEdit,
    PrimaryPushButton,
    PushButton,
    SubtitleLabel,
    setCustomStyleSheet,
)
from qfluentwidgets.components.dialog_box.mask_dialog_base import MaskDialogBase

from models.db_tables import Workspace
from models.workspace_list_model import WorkspaceListModel
from models.workspace_lookup import WorkspaceLookup
from prefabs.roundedListItemDelegate import RoundedListItemDelegate
from prefabs.workspaceListView import WorkspaceListView


class ManageWorkspaceDialog(MaskDialogBase):
    def __init__(self, workspaceListModel: WorkspaceListModel, parent=None):
        super().__init__(parent=parent)
        self.buttonGroup = QFrame(self.widget)

        # contains both self.viewLayout and self.buttonLayout
        self.vBoxLayout = QVBoxLayout(self.widget)

        self.viewLayout = QVBoxLayout()
        self.buttonLayout = QVBoxLayout(self.buttonGroup)

        # initializing buttons
        self.deleteWorkspaceButton = PushButton()
        self.deleteWorkspaceButton.setText("Delete Workspace")
        self.addWorkspaceButton = PushButton()
        self.addWorkspaceButton.setText("Add Workspace")
        self.addWorkspaceButton.setObjectName("addWorkspaceButton")
        self.addWorkspaceButton.setDisabled(True)
        self.closeDialogButton = PrimaryPushButton()
        self.closeDialogButton.setText("Close Dialog")

        self.titleLabel = SubtitleLabel("Manage Workspaces", parent=None)
        self.newWorkspaceLineEdit = LineEdit()
        self.workspaceList = WorkspaceListView()
        self.model = workspaceListModel
        self.workspaceList.setModel(self.model)

        self.model.setSelectionModel(self.workspaceList.selectionModel())

        self.workspaceList.setItemDelegate(RoundedListItemDelegate(self.workspaceList))

        self.__initWidget()

    def __initWidget(self):
        self.__setQss()
        self.__initLayout()

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))

        self.newWorkspaceLineEdit.setPlaceholderText("Enter name of new workspace")

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
        self.buttonGroup.setObjectName("buttonGroup")
        dialog_qss = f"""
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
        setCustomStyleSheet(self, dialog_qss, dialog_qss)

    def __connectSignalsToSlots(self):
        self.closeDialogButton.clicked.connect(lambda: self.close())
        self.addWorkspaceButton.clicked.connect(self.onAddWorkspaceButtonClicked)
        self.deleteWorkspaceButton.clicked.connect(self.onDeleteWorkspaceButtonClicked)

        self.newWorkspaceLineEdit.textChanged.connect(self.onWorkspaceTextChanged)

        self.workspaceList.selectionModel().selectionChanged.connect(self.onWorkspaceSelectionChanged)

        # from: https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/667
        self.workspaceList.selectionModel().currentChanged.connect(self.workspaceList.updateSelectedRows)
        self.model.current_workspace_changed.connect(self.onCurrentWorkspaceChanged)
        self.model.current_workspace_changed.connect(self.spawnInfoBar)
        self.model.current_workspace_deleted.connect(self.onCurrentWorkspaceDeleted)

    def keyPressEvent(self, event: QKeyEvent):
        """
        Override keyPressEvent to ignore escape key so that the dialog doesn't get closed when escape key is pressed
        """
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()

    def showEvent(self, event):
        self.preselect_current_workspace()
        super().showEvent(event)

    def preselect_current_workspace(self):
        current_workspace_id = WorkspaceLookup.get_current_workspace_id()
        logger.debug(f"Current workspace id: {current_workspace_id}")
        for workspace in self.model.workspaces:
            workspace_id = workspace["id"]
            workspace_name = workspace["workspace_name"]
            if workspace_id == current_workspace_id:
                index = self.model.index(
                    self.model.workspaces.index({"id": workspace_id, "workspace_name": workspace_name})
                )
                logger.debug(f"Preselecting workspace in manage workspace dialog: {workspace_name}")
                # self.workspaceList.selectionModel().select(index, QItemSelectionModel.SelectionFlag.Select)
                self.workspaceList.selectionModel().setCurrentIndex(index, QItemSelectionModel.SelectionFlag.Select)

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
        no_of_workspaces = self.model.rowCount()
        if selected_index.isValid() and no_of_workspaces > 1:  # only delete if there is more than one workspace
            self.model.delete_workspace(selected_index.row())
            self.workspaceList.clearSelection()
        elif selected_index.isValid() and no_of_workspaces <= 1:
            InfoBar.warning(
                title="Can't delete the only workspace",
                content="Add another workspace before deleting this one.",
                orient=Qt.Orientation.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=4000,
                parent=self.parent(),
            )

    def onWorkspaceSelectionChanged(self, selected, deselected):
        selected_index = selected.indexes()
        if selected_index:
            selected_index = selected_index[0]
            workspace_name = self.model.data(selected_index, Qt.ItemDataRole.DisplayRole)
            logger.debug(f"Selected workspace: {workspace_name}")

            self.closeDialogButton.setDisabled(False)
            self.model.set_current_workspace_preference()
        else:
            self.closeDialogButton.setDisabled(True)
            # TODO: if app is closed before before selecting a workspace, automatically select a workspace on next start
            #   or if there is no workspace make a sample workspace automatically and set it as the current workspace

    def spawnInfoBar(self):
        workspace_id = WorkspaceLookup.get_current_workspace_id()
        logger.debug(f"Current workspace id: {workspace_id}")
        workspace_name = self.model.get_workspace_name_by_id(workspace_id)

        InfoBar.success(
            title=f"{workspace_name} is selected",
            content="",
            orient=Qt.Orientation.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=4000,
            parent=self.parent(),
        )

    def onCurrentWorkspaceChanged(self):
        logger.debug(f"Current workspace change {WorkspaceLookup.get_current_workspace_id()}")

    def onCurrentWorkspaceDeleted(self):
        logger.debug("Current workspace deleted")


if __name__ == "__main__":
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
