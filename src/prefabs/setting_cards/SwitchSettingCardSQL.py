from typing import Union

from PySide6.QtGui import QIcon
from qfluentwidgets import FluentIconBase, SwitchSettingCard

from prefabs.config.config_item_sql import ConfigItemSQL
from prefabs.config.qconfig_sql import qconfig_custom


class SwitchSettingCardSQL(SwitchSettingCard):
    def __init__(
        self,
        icon: Union[str, QIcon, FluentIconBase],
        title,
        content=None,
        configItem: ConfigItemSQL = None,
        parent=None,
    ):
        super().__init__(icon, title, content, configItem, parent)
        if configItem:
            self.setValue(qconfig_custom.get(configItem))
            configItem.valueChanged.connect(self.setValue)

        qconfig_custom.get(configItem)

    def setValue(self, isChecked: bool):
        if self.configItem:
            qconfig_custom.set(self.configItem, isChecked)

        self.switchButton.setChecked(isChecked)
        self.switchButton.setText(self.tr("On") if isChecked else self.tr("Off"))
