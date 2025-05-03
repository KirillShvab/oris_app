from PyQt5.QtGui import QFontMetrics, QFont
from PyQt5.QtWidgets import *
from .ribbon_tab import RibbonTab
# from .gui_scale import gui_scale
from .stylesheets import Stylesheets
from .gui_scale import gui_scale

SCALE = int(gui_scale())


class RibbonToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Stylesheets.get("ribbon"))
        self.setObjectName("ribbonWidget")
        self._ribbon_widget = QTabWidget(self)
        self._ribbon_widget.setMaximumHeight(140 * SCALE)
        self._ribbon_widget.setMinimumHeight(110 * SCALE)
        self.setMovable(False)
        self.addWidget(self._ribbon_widget)

    def add_ribbon_tab(self, name):
        ribbon_tab = RibbonTab(self, name)
        ribbon_tab.setObjectName("tab_" + name)
        self._ribbon_widget.addTab(ribbon_tab, name)
        self._ribbon_widget.setStyleSheet("QTabBar::tab { font-size: 9pt; }")
        tab_font = QFont()
        tab_font.setPointSize(9)  # Увеличиваем шрифт

        self._ribbon_widget.setFont(tab_font)
        fm = QFontMetrics(tab_font)
        tab_height = fm.height() + 9  # Добавляем небольшой отступ
        self._ribbon_widget.setStyleSheet(f"QTabBar::tab {{ height: {tab_height}px; }}")

        return ribbon_tab

    def set_active(self, name):
        self.setCurrentWidget(self.findChild("tab_" + name))
