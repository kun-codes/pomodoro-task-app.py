from PySide6.QtCore import QModelIndex, QRect, Qt
from PySide6.QtGui import QColor, QFontMetrics, QPainter
from PySide6.QtWidgets import QListView, QStyledItemDelegate, QStyleOptionViewItem, QWidget
from qfluentwidgets import ListItemDelegate, isDarkTheme

from models.task_list_model import TaskListModel
from utils.time_conversion import convert_ms_to_hh_mm_ss


class TaskListItemDelegate(ListItemDelegate):
    """List item delegate"""

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
            theme_color.setAlpha(
                alpha + alpha_boost if alpha != 0 else 17 + alpha_boost
            )  # increasing alpha to make it more visible
            # 17 because the alpha of a selected row is 17
            painter.setBrush(theme_color)
        else:
            painter.setBrush(QColor(c, c, c, alpha))

        self._drawBackground(painter, option, index)

        # draw indicator
        if (
            index.row() in self.selectedRows
            and index.column() == 0
            and self.parent().horizontalScrollBar().value() == 0
        ):
            self._drawIndicator(painter, option, index)

        if index.data(Qt.CheckStateRole) is not None:
            self._drawCheckBox(painter, option, index)

        painter.setPen(Qt.GlobalColor.white if isDark else Qt.GlobalColor.black)
        font_metrics = QFontMetrics(option.font)

        elapsed_time_ms = index.data(TaskListModel.ElapsedTimeRole)
        target_time_ms = index.data(TaskListModel.TargetTimeRole)

        ehh, emm, ess = convert_ms_to_hh_mm_ss(elapsed_time_ms)
        thh, tmm, tss = convert_ms_to_hh_mm_ss(target_time_ms)

        time_text = f"{ehh:02d}:{emm:02d}:{ess:02d} / {thh:02d}:{tmm:02d}:{tss:02d}"
        time_text_width = font_metrics.horizontalAdvance(time_text)
        hello_world_x = option.rect.right() - time_text_width - 10
        hello_world_rect = QRect(hello_world_x, option.rect.top(), time_text_width, option.rect.height())
        painter.drawText(hello_world_rect, Qt.AlignRight | Qt.AlignVCenter, time_text)

        painter.restore()

        # reduce option.rect from the right by the width of the time text
        option.rect.adjust(0, 0, -time_text_width - 10, 0)
        QStyledItemDelegate.paint(self, painter, option, index)  # manually calling parent class paint method to avoid
        # multiple calls to _drawBackground and _drawIndicator

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        rect = option.rect
        y = rect.y() + (rect.height() - editor.height()) // 2
        x, w = max(5, rect.x()), rect.width() - 5  # breadth of indicator drawn is 3, arbitrarily set to 5

        editor.setGeometry(x, y, w, rect.height())
