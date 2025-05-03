from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QToolBar, QLabel, QAction


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(100)

        # Создаем вкладки
        tab1 = QWidget()
        self.addTab(tab1, "Карта")
        tab2 = QWidget()
        self.addTab(tab2, "Расчет")
        tab3 = QWidget()
        self.addTab(tab3, "Данные")

        # Основной тулбар с тремя кнопками
        toolbar1 = QToolBar("Основной тулбар", self)
        toolbar1.setIconSize(QSize(40, 40))  # Изменение размера иконок
        toolbar1.setFixedHeight(40)



        action1 = QAction(QIcon("img/toolbar_icons/coordinates__toolbar.png"), "Система координат", self)
        action2 = QAction(QIcon("img/scale.png"), "Шкала масштаба", self)
        action3 = QAction(QIcon("img/grid.png"), "Сетка", self)
        action4 = QAction(QIcon("img/wind_rose.png"), "Роза ветров", self)


        toolbar1.addAction(action1)
        toolbar1.addAction(action2)
        toolbar1.addAction(action3)
        toolbar1.addAction(action4)

        toolbar3 = QToolBar("Основной тулбар", self)
        toolbar3.setIconSize(QSize(40, 40))  # Изменение размера иконок
        toolbar3.setFixedHeight(40)
        action5 = QAction(QIcon("img/report.png"), "Отчет по событиям", self)

        toolbar3.addAction(action5)

        # Устанавливаем макет для первой вкладки
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(toolbar1)
        tab3_layout = QVBoxLayout()
        tab3_layout.addWidget(toolbar3)
        tab3.setLayout(tab3_layout)
        tab1.setLayout(tab1_layout)

