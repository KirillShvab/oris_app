from PyQt5.QtWidgets import QMainWindow, QWidget
from Ribbon import Icons, Ribbon
from calc_fire.widget_calc import FireRadiusWindow
from map.graphicsview import GraphicsView
from menu.menubar import MenuBar
from scale.scale_window import ScaleWindow

SOFTWARE_TITLE = "ОРИС"


class MainMenu(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(SOFTWARE_TITLE)
        self.setWindowIcon(Icons.get_icon("logo"))
        self.setDockNestingEnabled(True)
        self.centralWidget()
        self.setMenuBar(MenuBar(self))
        ribbon = Ribbon.init_ribbon(self)
        self.graphics_view = GraphicsView(self)

        self.setCentralWidget(self.graphics_view)
        self.showMaximized()

    def handle_flammable_substance(self):
        self.graphics_view.enable_point_selection()

    def hide_coord(self):
        self.graphics_view.coord_system.hide()

    def scale_map(self):
        print(self.graphics_view.get_focused_danger_item())

        self.scale_windosw = ScaleWindow(self.graphics_view)
        self.scale_windosw.show()

    def calc_fire_flash_radius(self):
        danger_object = self.graphics_view.get_focused_danger_item()
        if danger_object:
            self.window = FireRadiusWindow(danger_object,self.graphics_view.coord_system.convert_to_pixels)
            self.window.show()


