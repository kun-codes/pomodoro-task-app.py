from typing import Union

from PySide6.QtGui import QIcon
from qfluentwidgets import RangeSettingCard, FluentIconBase
from prefabs.config.qconfig_sql import qconfig_custom

class RangeSettingCardSQL(RangeSettingCard):
    def __init__(self, configItem, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(configItem, icon, title, content, parent)
        # todo: improve performance when changing the value of the slider

    def setValue(self, value):
        qconfig_custom.set(self.configItem, value)
        self.valueLabel.setNum(value)
        self.valueLabel.adjustSize()
        self.slider.setValue(value)
