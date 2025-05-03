from PyQt5.QtWidgets import QApplication

from menu_window import MainMenu

if __name__ == '__main__':
    app = QApplication([])
    menu = MainMenu()
    menu.show()
    app.exec()