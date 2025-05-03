from PyQt5 import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *

from .gui_scale import gui_scale
from .stylesheets import Stylesheets

SCALE = gui_scale()


class RibbonButton(QToolButton):
    def __init__(self, parent, action, is_large):
        super().__init__(parent)

        self._actionOwner = action
        self.update_button_status_from_action()
        self.clicked.connect(self._actionOwner.trigger)
        self._actionOwner.changed.connect(self.update_button_status_from_action)

        # TODO сделать стилизацию через словарь
        if is_large:
            self.setMaximumWidth(80 * SCALE)
            self.setMinimumWidth(50 * SCALE)
            self.setMinimumHeight(75 * SCALE)
            self.setMaximumHeight(80 * SCALE)
            self.setStyleSheet(Stylesheets.get("ribbonButton"))
            self.setToolButtonStyle(3)
            self.setIconSize(QSize(32 * SCALE, 32 * SCALE))
        else:
            self.setToolButtonStyle(2)
            self.setMaximumWidth(120 * SCALE)
            self.setIconSize(QSize(16 * SCALE, 16 * SCALE))
            self.setStyleSheet(Stylesheets.get("ribbonSmallButton"))

    def update_button_status_from_action(self):
        self.setText(self._actionOwner.text())
        self.setStatusTip(self._actionOwner.statusTip())
        self.setToolTip(self._actionOwner.toolTip())
        self.setIcon(self._actionOwner.icon())
        self.setEnabled(self._actionOwner.isEnabled())
        self.setCheckable(self._actionOwner.isCheckable())
        self.setChecked(self._actionOwner.isChecked())
