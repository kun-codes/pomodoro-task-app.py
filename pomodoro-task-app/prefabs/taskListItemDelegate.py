from PySide6.QtCore import Qt, QModelIndex, QMargins
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QListView, QStyledItemDelegate, QStyleOptionViewItem
from qfluentwidgets import ListItemDelegate, isDarkTheme, themeColor


class TaskListItemDelegate(ListItemDelegate):
    """ List item delegate """

    def __init__(self, parent: QListView):
        super().__init__(parent)

    def paint(self, painter, option, index):
        # I had to copy-paste the method from TableItemDelegate
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing)

        # set clipping rect of painter to avoid painting outside the borders
        painter.setClipping(True)
        painter.setClipRect(option.rect)

        # call original paint method where option.rect is adjusted to account for border
        option.rect.adjust(0, self.margin, 0, -self.margin)

        # draw highlight background
        isHover = self.hoverRow == index.row()
        isPressed = self.pressedRow == index.row()
        isAlternate = index.row() % 2 == 0 and self.parent().alternatingRowColors()
        isDark = isDarkTheme()

        c = 255 if isDark else 0
        alpha = 0

        if index.row() not in self.selectedRows:
            if isPressed:
                alpha = 9 if isDark else 6
            elif isHover:
                alpha = 12
            elif isAlternate:
                alpha = 5
        else:
            if isPressed:
                alpha = 15 if isDark else 9
            elif isHover:
                alpha = 25
            else:
                alpha = 17

        if index.data(Qt.ItemDataRole.BackgroundRole):
            theme_color: QColor = index.data(Qt.ItemDataRole.BackgroundRole)
            alpha_boost = 45 if isDark else 30
            theme_color.setAlpha(alpha + alpha_boost if alpha != 0 else 17 + alpha_boost)  # increasing alpha to make it more visible
            # 17 because the alpha of a selected row is 17
            painter.setBrush(theme_color)
        else:
            painter.setBrush(QColor(c, c, c, alpha))

        self._drawBackground(painter, option, index)

        # draw indicator
        if index.row() in self.selectedRows and index.column() == 0 and self.parent().horizontalScrollBar().value() == 0:
            self._drawIndicator(painter, option, index)

        if index.data(Qt.CheckStateRole) is not None:
            self._drawCheckBox(painter, option, index)

        painter.restore()
        QStyledItemDelegate.paint(self, painter, option, index)  # manually calling parent class paint method to avoid
        # multiple calls to _drawBackground and _drawIndicator
