from PyQt5.QtWidgets import QAction
from .icons import Icons


class ActionGroup:
    def __init__(self, parent, definitions):
        self._definitions = definitions
        for attr_name, icon_name, text in definitions:
            action = QAction(Icons.get_icon(icon_name), text, parent)
            setattr(self, attr_name, action)

    def __str__(self):
        result = f"Описание группы действий в {self.__class__.__name__}:\n"
        for attr_name, icon_name, text in self._definitions:
            action = getattr(self, attr_name)
            result += f"  ▸ {attr_name}:\n"
            result += f"     - Картинка: {Icons.get_path_icon(icon_name)}\n"
            result += f"     - Название: {action.text()}\n"
        return result


class Actions:
    def __init__(self, parent=None):
        super().__init__()

        self.display = ActionGroup(parent, [
            ("COORD", "coord", "Координаты"),
            ("SCALEBAR", "scale", "Шкала"),
            ("WINDROSE", "windrose", "Компас"),
            ("GRID", "grid", "Сетка"),
        ])
        self.objects = ActionGroup(parent, [
            ("FLAMMABLE_SUBSTANCE", "flummable_substance", "ГГ, ЛВЖ"),
        ])

        self.methods = ActionGroup(parent, [
            ("EXPLOUSION_FLASH", "explousion_flash", "Взрыв\nвспышка"),
        ])
