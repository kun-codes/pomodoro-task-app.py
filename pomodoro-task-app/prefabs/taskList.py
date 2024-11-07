from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QAbstractItemView, QListView
from qfluentwidgets import ListView, LineEdit, ListItemDelegate
from prefabs.roundedListItemDelegate import RoundedListItemDelegateDisplayTime
from ui_py.ui_tasks_list_view import Ui_TaskView
from prefabs.taskListItemDelegate import TaskListItemDelegate


class TaskList(ListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAutoScroll(True)

        self._mousePressedOnItem = False

        self.entered.disconnect()  # see mouseMoveEvent method's docstring

        self.setItemDelegate(TaskListItemDelegate(self))

    def edit(self, index, trigger, event):
        """
        Override the edit method to show lineedit which is pre-filled with the task name
        """
        if trigger == QAbstractItemView.DoubleClicked:
            task_name = self.model().data(index, Qt.DisplayRole)
            editor = LineEdit(self)
            editor.setProperty("transparent", False)
            editor.setText(task_name)
            self.setIndexWidget(index, editor)
            editor.setFocus()
            editor.editingFinished.connect(lambda: self.commitData(editor))
            return True
        return super().edit(index, trigger, event)

    def commitData(self, editor):
        index = self.currentIndex()
        self.model().setData(index, editor.text(), Qt.DisplayRole)
        self.setIndexWidget(index, None)

    def mousePressEvent(self, e):
        """
        This method modifies the behaviour of ListView according to which items are selected when mouse is pressed on
        them.
        Items are selected in TaskList when mouse is clicked (pressed and released) on them
        """
        if e.button() == Qt.LeftButton or self._isSelectRightClickedRow:
            return QListView.mousePressEvent(self, e)

        # to select the row on which mouse is clicked
        index = self.indexAt(e.pos())
        if index.isValid():
            self._mousePressedOnItem = True
        else:
            self._mousePressedOnItem = False

        QWidget.mousePressEvent(self, e)

    def mouseReleaseEvent(self, e):
        """
        This method modifies the behaviour of ListView according to which items are selected when mouse is pressed on
        them.
        Items are selected in TaskList when mouse is clicked (pressed and released) on them
        """
        # I don't know if I have to keep the below two lines
        QListView.mouseReleaseEvent(self, e)
        self.updateSelectedRows()

        # to select the row on which mouse is clicked
        if self._mousePressedOnItem:
            index = self.indexAt(e.pos())
            if index.isValid():
                self._setPressedRow(index.row())
                # self.updateSelectedRows()

        self._mousePressedOnItem = False
        super().mouseReleaseEvent(e)

    def dropEvent(self, e):
        """
        This method is called when an item is dropped onto a TaskList. This will go through a while loop till it finds
        TaskView class's object and then set the pressed row of both todoTasksList and completedTasksList to -1. This
        is done to overcome bugs in the original code in qfluentwidgets where the pressed row was not getting reset
        when an item was dropped.
        """
        parent_view = self.parentWidget()
        while parent_view is not None:
            if isinstance(parent_view, Ui_TaskView):  # using Ui_TaskView because view.subinterfaces.tasks_view.TaskList
                # is a child class of Ui_TaskView and it cannot be imported here due to circular import

                parent_view.todoTasksList._setPressedRow(-1)
                parent_view.completedTasksList._setPressedRow(-1)
                parent_view.todoTasksList._setHoverRow(-1)
                parent_view.completedTasksList._setHoverRow(-1)
                parent_view.todoTasksList.viewport().update()
                parent_view.completedTasksList.viewport().update()
                break
            parent_view = parent_view.parentWidget()
        super().dropEvent(e)

    def mouseMoveEvent(self, e):
        """
        This method is called when mouse is moved over the TaskList. This will set the hover row of the delegate to the
        row over which mouse is hovering. This is done because in qfluentwidgets if mouse is moved away from an already
        hovered row to empty space of TaskList such that it doesn't cross any other row, the hovered row is not reset

        Also for the same reason self.entered signal has been disconnected in __init__ method
        """

        index = self.indexAt(e.pos())
        new_hover_row = index.row() if index.isValid() else -1
        if new_hover_row != self.delegate.hoverRow:
            self._setHoverRow(new_hover_row)
        super().mouseMoveEvent(e)

    def _setHoverRow(self, row: int):
        delegate = self.itemDelegate()
        if isinstance(delegate, ListItemDelegate):
            delegate.setHoverRow(row)
            self.viewport().update()
