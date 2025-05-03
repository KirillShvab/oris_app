from pathlib import Path


class Stylesheets:
    """
    Класс для управления стилями Qt, загружая их по требованию.

    Позволяет получать стили по имени без предварительной загрузки всех файлов.
    """

    _stylesheet_paths = {
        "main": "Ribbon/stylesheets/main.css",
        "ribbon": "Ribbon/stylesheets/ribbon.css",
        "ribbonPane": "Ribbon/stylesheets/ribbonPane.css",
        "ribbonButton": "Ribbon/stylesheets/ribbonButton.css",
        "ribbonSmallButton": "Ribbon/stylesheets/ribbonSmallButton.css",
    }

    @staticmethod
    def _read_file(path: str) -> str:
        """
        Читает содержимое файла стиля.

        Args:
            path (str): Путь к файлу стиля.

        Returns:
            str: Содержимое файла или пустая строка в случае ошибки.
        """
        try:
            return Path(path).read_text(encoding="utf-8")
        except Exception as e:
            print(f"Failed to read stylesheet '{path}': {e}")
            return ""

    @classmethod
    def get(cls, name: str) -> str:
        """
        Получает стиль по имени, загружая его при первом запросе.

        Args:
            name (str): Имя стиля, соответствующее ключу в `_stylesheet_paths`.

        Returns:
            str: Содержимое файла стиля или пустая строка, если стиль не найден.
        """
        path = cls._stylesheet_paths.get(name)
        if path:
            return cls._read_file(path)
        print(f"Stylesheet '{name}' not found.")
        return ""
