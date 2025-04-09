from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout, QGraphicsEllipseItem, QGraphicsItem, \
    QApplication, QGraphicsTextItem

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem
class CustomItem(QGraphicsItem):
    def __init__(self, size=60, color=QColor("skyblue"), label=""):
        super().__init__()
        self.size = size
        self.color = color
        self.label_text = label
        self.radius = self.size * 1.5

        # Текст
        self.text_item = QGraphicsTextItem(self)
        self.text_item.setDefaultTextColor(Qt.black)
        self.text_item.setZValue(1)
        self.set_label(self.label_text)  # Центрируем текст сразу

    def set_label(self, value: str):
        self.label_text = str(value)
        self.text_item.setPlainText(self.label_text)

        # Центрируем по X (сверху от квадрата, на -20 по Y)
        text_rect = self.text_item.boundingRect()
        x = (self.size - text_rect.width()) / 2
        self.text_item.setPos(x, -20)

    def set_radius(self, new_radius: float):
        self.radius = new_radius
        self.prepareGeometryChange()  # Уведомляем сцену, что изменится boundingRect
        self.update()  # Перерисовываем элемент

    def boundingRect(self):
        margin = self.radius - self.size / 2
        return QRectF(-margin, -margin - 20, self.size + 2 * margin, self.size + 2 * margin + 20)

    def delete(self):
        if self.scene():
            self.scene().removeItem(self)
    def paint(self, painter, option, widget=None):
        rect = QRectF(0, 0, self.size, self.size)
        center = rect.center()

        # Круг
        painter.setBrush(QColor(255, 100, 100, 128))
        painter.setPen(QPen(QColor(139, 50, 50), 2))
        painter.drawEllipse(center, self.radius, self.radius)

        # Квадрат
        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(Qt.black, 2))
        painter.drawRect(rect)
    def mouseDoubleClickEvent(self, event):
        # Handle dragging behavior on double click
        if event.button() == Qt.LeftButton and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.is_dragging = True
            self.offset = event.pos()  # Save the offset from the click point

    def mouseMoveEvent(self, event):
        # Move the object when the Ctrl key is held
        if self.is_dragging:
            new_pos = event.scenePos() - self.offset  # Get the scene coordinates
            self.setPos(new_pos)  # Move the object based on the offset
            self.update()  # Update the display

    def mouseReleaseEvent(self, event):
        # Stop dragging when the left mouse button is released
        if event.button() == Qt.LeftButton:
            self.is_dragging = False


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Создаём сцену и представление
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)

        # Пример: добавим прямоугольник
        # rect = self.scene.addRect(0, 0, 100, 50, QPen(Qt.black), QBrush(QColor("lightblue")))
        item = CustomItem(size=100, color=QColor("orange"), label="Взрыв-вспышка на объекте 1")
        item.set_radius(400)
        self.scene.addItem(item)
        # Настраиваем layout
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.setWindowTitle("Graphics View Example")
        self.showMaximized()


def main():
    from PyQt5.QtWidgets import QApplication
    from menu_window import MainMenu
    app = QApplication([])
    menu = Window()
    menu.show()
    app.exec()


if __name__ == '__main__':
    main()