from PySide6.QtCore import QMimeData, Qt, Signal
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QVBoxLayout,
    QWidget
)
from qfluentwidgets import CardWidget, FluentWindow, FluentIcon

from prefabs.taskCard import TaskCard


class DragTargetIndicator(TaskCard):
    """
    The placeholder box which is showed as a preview while dragging task cards
    """
    def __init__(self, parent=None):
        super().__init__(parent)


# Individual draggable item
class DragItem(TaskCard):
    """
    A draggable task card
    """
    def __init__(self, parent=None, task_name=""):
        super().__init__(parent=parent, task_name=task_name)
        # self.taskLabel.setText(text)
        # Store data separately from display label, but use label for default.
        self.data = self.taskLabel.text()

    def set_data(self, data):
        self.data = data

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            task_label = self.taskLabel.text()
            pixmap = self.grab()
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)
            self.show()  # Show this widget again, if it's dropped outside.


class DragWidget(CardWidget):
    """
    Generic list sorting handler.
    """

    orderChanged = Signal(list)

    def __init__(self, *args, orientation=Qt.Orientation.Vertical, **kwargs):
        super().__init__()
        self.setAcceptDrops(True)

        # Store the orientation for drag checks later.
        self.orientation = orientation

        if self.orientation == Qt.Orientation.Vertical:
            self.blayout = QVBoxLayout()
        else:
            self.blayout = QHBoxLayout()

        # Add the drag target indicator. This is invisible by default,
        # we show it and move it around while the drag is active.
        self._drag_target_indicator = DragTargetIndicator()
        self.blayout.addWidget(self._drag_target_indicator)
        self._drag_target_indicator.hide()

        self.setLayout(self.blayout)

    def dragEnterEvent(self, e):
        e.accept()

    def dragLeaveEvent(self, e):
        self._drag_target_indicator.hide()
        e.accept()

    def dragMoveEvent(self, e):
        # Find the correct location of the drop target, so we can move it there.
        index = self._find_drop_location(e)
        if index is not None:
            # Inserting moves the item if its alreaady in the layout.
            self.blayout.insertWidget(index, self._drag_target_indicator)
            # Hide the item being dragged.
            e.source().hide()
            # Show the target.
            self._drag_target_indicator.show()
        e.accept()

    def dropEvent(self, e):
        widget = e.source()
        # Use drop target location for destination, then remove it.
        self._drag_target_indicator.hide()
        index = self.blayout.indexOf(self._drag_target_indicator)
        if index is not None:
            self.blayout.insertWidget(index, widget)
            self.orderChanged.emit(self.get_item_data())
            widget.show()
            print(widget.parentWidget().objectName())
            self.blayout.activate()
        e.accept()

    def _find_drop_location(self, e):
        pos = e.position()
        spacing = self.blayout.spacing() / 2

        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()

            if self.orientation == Qt.Orientation.Vertical:
                # Drag drop vertically.
                drop_here = (
                        pos.y() >= w.y() - spacing
                        and pos.y() <= w.y() + w.size().height() + spacing
                )
            else:
                # Drag drop horizontally.
                drop_here = (
                        pos.x() >= w.x() - spacing
                        and pos.x() <= w.x() + w.size().width() + spacing
                )

            if drop_here:
                # Drop over this target.
                break

        return n

    def add_item(self, item):
        self.blayout.addWidget(item)

    def get_item_data(self):
        data = []
        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            if w != self._drag_target_indicator:
                # The target indicator has no data.
                data.append(w.data)
        return data


if __name__ == "__main__":
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.drag = DragWidget(orientation=Qt.Orientation.Vertical)
            self.drag.setObjectName("Upper_list")
            for n, l in enumerate(["A1", "B1", "C1", "D1"]):
                item = DragItem(task_name=l)
                item.set_data(n)  # Store the data.
                self.drag.add_item(item)

            self.drag_2 = DragWidget(orientation=Qt.Orientation.Vertical)
            self.drag_2.setObjectName("Lower_list")
            # for n, l in enumerate(["A3", "B3", "C3", "D3"]):
            for n, l in enumerate(["A3", "B3", "C3", "D3"]):
                item = DragItem(task_name=l)
                item.set_data(n)  # Store the data.
                self.drag_2.add_item(item)
            # Print out the changed order.
            self.drag_2.orderChanged.connect(print)

            container = QWidget()
            layout = QVBoxLayout()
            # layout.addStretch(1)
            layout.addWidget(self.drag)
            layout.addStretch(1)
            layout.addWidget(self.drag_2)
            container.setLayout(layout)

            self.setCentralWidget(container)


    class FluentTestWindow(FluentWindow):
        def __init__(self):
            super().__init__()
            self.testInterface = MainWindow()
            self.testInterface.setObjectName("Test Interface")

            self.initNavigation()

        def initNavigation(self):
            # Add sub interface
            self.addSubInterface(self.testInterface, FluentIcon.ADD, 'Tasks')


    app = QApplication([])
    w = FluentTestWindow()
    w.show()

    app.exec()
