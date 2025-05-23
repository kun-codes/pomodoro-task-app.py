from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView
from qfluentwidgets import LineEdit, ListView


class WorkspaceListView(ListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_editor = None

    def edit(self, index, trigger, event):
        """Handle inline editing of workspace name"""
        if trigger == QAbstractItemView.DoubleClicked:
            workspace_name = self.model().data(index, Qt.DisplayRole)

            editor = LineEdit(self)
            editor.setProperty("transparent", False)
            editor.setText(workspace_name)
            editor.selectAll()
            editor.editingFinished.connect(lambda: self.commitData(editor))
            editor.setCursorPosition(0)
            editor.setObjectName("editor")
            self.setIndexWidget(index, editor)
            editor.setFocus()

            self.current_editor = editor
            return True
        return super().edit(index, trigger, event)

    def commitData(self, editor):
        """Save edited workspace name"""
        index = self.currentIndex()
        self.model().setData(index, editor.text(), Qt.EditRole)
        self.current_editor = None
        self.setIndexWidget(index, None)
