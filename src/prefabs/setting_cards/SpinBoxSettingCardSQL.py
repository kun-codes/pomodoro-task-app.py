from typing import Union

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from qfluentwidgets import FluentIconBase, SettingCard, SpinBox

from prefabs.config.qconfig_sql import qconfig_custom


class SpinBoxSettingCardSQL(SettingCard):
    """Setting card with a SpinBox"""

    valueChanged = Signal(int)

    def __init__(self, configItem, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        """
        Parameters
        ----------
        configItem: RangeConfigItem
            configuration item operated by the card

        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget
        """
        super().__init__(icon, title, content, parent)
        self.configItem = configItem
        self.spinBox = SpinBox(self)

        self.spinBox.setSingleStep(1)
        self.spinBox.setRange(*configItem.range)
        self.spinBox.setValue(configItem.value)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addSpacing(6)
        self.hBoxLayout.addWidget(self.spinBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        configItem.valueChanged.connect(self.setValue)
        self.spinBox.valueChanged.connect(self.__onValueChanged)

    def __onValueChanged(self, value: int):
        """spin box value changed slot"""
        self.setValue(value)
        self.valueChanged.emit(value)

    def setValue(self, value):
        qconfig_custom.set(self.configItem, value)
        self.spinBox.setValue(value)
