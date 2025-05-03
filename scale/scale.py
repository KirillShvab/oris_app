import sys
from PyQt5.QtWidgets import (QGraphicsLineItem,
                             QGraphicsTextItem, QGraphicsRectItem, QGraphicsItemGroup, QGraphicsPolygonItem,
                             QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QPolygonF

SCALE_SIZE = 10  # Размер делений шкалы
LENGTH_OXY = 100  # Сохраненная позиция
LENGTH_SCALE = 50  # м


class CoordinateSystem(QGraphicsItemGroup):
    """Класс для создания системы координат со стрелками на концах"""

    def __init__(self, width=0, height=0, parent=None):
        super().__init__(parent)
        self.width = width
        self.height = height

        self.oxy_length = LENGTH_OXY  # Длина осей
        self.scale_size = SCALE_SIZE  # Размер делений шкалы
        self.length_scale = LENGTH_SCALE
        self.saved_position = QPointF(width, height)  # Сохранённая позиция
        self.init_items()
        self.setFlag(QGraphicsItemGroup.ItemIsMovable, False)  # Запрещаем перемещение
        self.hide_flag = True

    def clear(self):
        for item in self.childItems():
            self.removeFromGroup(item)
            item.setParentItem(None)

    def convert_to_pixels(self,length):
        return length * (self.oxy_length/self.length_scale)
    def init_items(self):
        """Создаёт оси, подписи и шкалу со стрелками"""
        self.clear()
        self.setPos(self.saved_position)  # Устанавливаем сохранённую позицию

        pen = QPen(Qt.black)
        pen.setWidth(2)

        # Основные оси
        axis_x = QGraphicsLineItem(0, self.height, self.oxy_length - 5, self.height)
        axis_y = QGraphicsLineItem(0, self.height, 0, self.height - self.oxy_length + 5)
        axis_x.setPen(pen)
        axis_y.setPen(pen)
        self.addToGroup(axis_x)
        self.addToGroup(axis_y)

        # Стрелки
        arrow_size = 8
        x_arrow = QPolygonF([QPointF(self.oxy_length, self.height),
                             QPointF(self.oxy_length - arrow_size, self.height + arrow_size / 2),
                             QPointF(self.oxy_length - arrow_size, self.height - arrow_size / 2)])
        y_arrow = QPolygonF([QPointF(0, self.height - self.oxy_length),
                             QPointF(-arrow_size / 2, self.height - self.oxy_length + arrow_size),
                             QPointF(arrow_size / 2, self.height - self.oxy_length + arrow_size)])

        x_arrow_item = QGraphicsPolygonItem(x_arrow)
        y_arrow_item = QGraphicsPolygonItem(y_arrow)
        x_arrow_item.setBrush(Qt.black)
        y_arrow_item.setBrush(Qt.black)
        self.addToGroup(x_arrow_item)
        self.addToGroup(y_arrow_item)

        # Отрисовка плашки
        main_rect = QGraphicsRectItem(0, self.height + 5, self.oxy_length, 5)
        main_rect.setBrush(Qt.gray)  # Цвет фона плашки
        self.addToGroup(main_rect)

        # Добавление внутренних прямоугольников
        for i in range(int(self.oxy_length // self.scale_size)):
            rect = QGraphicsRectItem(i * self.scale_size, self.height + 5, self.scale_size, 5)
            rect.setBrush(Qt.black if i % 2 == 0 else Qt.white)
            self.addToGroup(rect)

        self.setPos(self.saved_position)  # Восстанавливаем позицию

    def update_scale(self, new_length):
        """Обновляет шкалу без сброса позиции"""
        self.oxy_length = new_length
        self.init_items()
        self.setPos(self.saved_position)  # Устанавливаем сохранённую позицию

    def update_length(self, new_value):
        self.length_scale = new_value

    def convert_length(self, length_meter):
        """ pixcels = metr / digit_coef_metr"""
        return length_meter / self.length_scale

    def hide(self):
        """Скрывает все элементы системы координат"""
        if self.hide_flag:
            for item in self.childItems():
                item.setVisible(False)

        else:
            for item in self.childItems():
                item.setVisible(True)
        self.hide_flag = not self.hide_flag


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Создаём сцену и представление
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)

        # Пример: добавим прямоугольник
        # rect = self.scene.addRect(0, 0, 100, 50, QPen(Qt.black), QBrush(QColor("lightblue")))
        self.coord_system = CoordinateSystem(width=100, height=100)
        self.scene.addItem(self.coord_system)
        # Настраиваем layout
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.setWindowTitle("Graphics View Example")
        self.showMaximized()


def main():
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    menu = Window()
    menu.show()
    app.exec()


if __name__ == '__main__':
    main()
