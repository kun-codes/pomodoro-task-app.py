from PySide6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout
from qfluentwidgets import FluentWindow, setCustomStyleSheet
from qfluentwidgets import TitleLabel
from qfluentwidgets.window.fluent_window import FluentWindowBase


class VBoxLayoutInitializer(QWidget):
    """
    A hack to declare self.vBoxLayout in PomodoroFluentWindowBase before FluentWindowBase's parent classes's __init__
    is called
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)  # this line causes the error "QLayout: Attempting to add QLayout "" to
        # MainWindow "", which already has a layout", it can be fixed if I change the line in FluentWindowBase from
        # self.hBoxLayout = QHBoxLayout(self) to self.hBoxLayout = QHBoxLayout()
        # but I don't know how to do it
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)


class PomodoroFluentWindowBase(FluentWindowBase, VBoxLayoutInitializer):
    """ Fluent window base class """

    def __init__(self, parent=None):
        super().__init__(parent=parent)


class PomodoroFluentWindow(PomodoroFluentWindowBase, FluentWindow):
    """ Fluent window """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.bottomBar = QWidget(self)
        self.bottomBarLayout = QHBoxLayout(self.bottomBar)
        self.bottomBarLabel = TitleLabel(self.bottomBar)
        self.bottomBarLabel.setText("Bottom bar")
        self.bottomBarLayout.addWidget(self.bottomBarLabel)

        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.bottomBar)

        self.stackedWidget.setObjectName("stackedWidget")

        self.rightBorder = QWidget(self)
        self.rightBorder.setObjectName("rightBorder")
        self.rightBorder.setFixedWidth(10)
        self.hBoxLayout.addWidget(self.rightBorder)

        qssLight = """
        StackedWidget {
            border-bottom-left-radius: 10px;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            border-right: 1px solid rgba(0, 0, 0, 0.068);
            border-bottom: 1px solid rgba(0, 0, 0, 0.068);
        }
        """
        qssDark = """
        StackedWidget {
            border-bottom-left-radius: 10px;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            border-right: 1px solid rgba(0, 0, 0, 0.18);
            border-bottom: 1px solid rgba(0, 0, 0, 0.18);
        }
        """

        # from: https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/707
        self.style().unpolish(self)
        self.style().polish(self)

        # setCustomStyleSheet(self.stackedWidget, borderQss, borderQss)
        setCustomStyleSheet(self.stackedWidget, qssLight, qssDark)