from map.graphicsview import GraphicsView
from .ribbon_button import RibbonButton
from .ribbon_toolbar import *
from .ribbon_actions import Actions


class Ribbon(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # -------------      ribbon       -----------------

        self.init_ribbon()

    def init_ribbon(self):
        self.actions = Actions()
        self._ribbon = RibbonToolBar(self)
        self.addToolBar(self._ribbon)
        #-----------------ОСНОВНОЕ--------------------
        home_tab = self._ribbon.add_ribbon_tab("Основное")
        file_pane = home_tab.add_ribbon_pane("Дисплей")
        file_pane.add_ribbon_widget(RibbonButton(self, self.actions.display.COORD, True))
        file_pane.add_ribbon_widget(RibbonButton(self, self.actions.display.SCALEBAR, True))
        file_pane.add_ribbon_widget(RibbonButton(self, self.actions.display.WINDROSE, True))
        file_pane.add_ribbon_widget(RibbonButton(self, self.actions.display.GRID, True))

        self.actions.display.COORD.triggered.connect(self.hide_coord)
        self.actions.display.SCALEBAR.triggered.connect(self.scale_map)

        home_tab.add_spacer()

        # -----------------ПРОЕКТ_____________________
        project_tab = self._ribbon.add_ribbon_tab("Проект")
        info_panel = project_tab.add_ribbon_pane("Объекты")
        info_panel.add_ribbon_widget(RibbonButton(self, self.actions.objects.FLAMMABLE_SUBSTANCE, True))

        self.actions.objects.FLAMMABLE_SUBSTANCE.triggered.connect(self.handle_flammable_substance)
        # ------------------РАСЧЕТ--------------------
        about_tab = self._ribbon.add_ribbon_tab("Расчет")
        info_panel = about_tab.add_ribbon_pane("Модуль")
        info_panel.add_ribbon_widget(RibbonButton(self, self.actions.methods.EXPLOUSION_FLASH, True))
        self.actions.methods.EXPLOUSION_FLASH.triggered.connect(self.calc_fire_flash_radius)

    def __event_connection(self):
        pass


