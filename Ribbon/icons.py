from PyQt5.QtGui import QIcon


class Icons:
    _icons = {
        #
        "logo": "Ribbon/icons/logo.png",
        # ----
        "scale": "Ribbon/icons/scalebar.png",
        "coord": "Ribbon/icons/coordinate.png",
        "windrose": "Ribbon/icons/windrose.png",
        "grid": "Ribbon/icons/grid.png",
        # ----
        "explousion_flash": "Ribbon/icons/explosion-flash.png",
        "flummable_substance": "Ribbon/icons/lvg-ll.png",
        # ----
        "default": "Ribbon/icons/not-found.png"

    }

    @classmethod
    def get_icon(cls, name: str) -> QIcon:
        """Возвращает QIcon по ключу или иконку по умолчанию"""
        path = cls._icons.get(name, cls._icons["default"])
        return QIcon(path)

    @classmethod
    def get_path_icon(cls, name: str):
        return cls._icons.get(name, None)
