from PyQt5.QtWidgets import QApplication


def gui_scale():
    # Получаем первый экран
    screens = QApplication.screens()
    if screens:
        screen = screens[0]  # выбираем первый экран
        dpi = screen.logicalDotsPerInch()
        return int(dpi / 96)
    return 1  # Возвращаем 1, если экранов нет