from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QListView, QStyleOptionViewItem, QStyle
from qfluentwidgets import TableItemDelegate, isDarkTheme, themeColor


class RoundedListItemDelegate(TableItemDelegate):
    """ Round List item delegate """

    def __init__(self, parent: QListView):
        super().__init__(parent)

    def _drawBackground(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        painter.save()
        rect = option.rect.adjusted(1, 1, -1, -1)  # Adjust to fit within the background
        if option.state & QStyle.State_Selected:
            painter.setBrush(option.palette.highlight())
        else:
            painter.setBrush(QColor(255, 255, 255, 13 if isDarkTheme() else 170))
        if isDarkTheme():
            painter.setPen(QColor(0, 0, 0, 48))
        else:
            painter.setPen(QColor(0, 0, 0, 12))
        painter.drawRoundedRect(rect, 5, 5)
        painter.restore()

    def _drawIndicator(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        if option.state & QStyle.State_Selected:
            rect = option.rect.adjusted(1, 1, -1, -1)  # Adjust to fit within the background
            painter.setPen(QPen(themeColor(), 2))  # Set pen with theme color and width 2
            painter.drawRoundedRect(rect, 5, 5)  # Draw rounded rectangle border
