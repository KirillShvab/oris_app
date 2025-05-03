from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QBrush, QColor, QTextCharFormat
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout, QGraphicsEllipseItem, QGraphicsItem, \
    QApplication, QGraphicsTextItem, QMenu, QAction

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem


class DangerItem(QGraphicsItem):
    def __init__(self, size=60, x=0, y=0, color=QColor("skyblue"), label=""):
        super().__init__()
        self.fire_radius = 0
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.size = size
        self.color = color
        self.label_text = label
        self.radius = self.size + 50
        self.setPos(x, y)
        self.has_focus = False  # Новый флаг
        self.is_visible = False  # Флаг видимости

        self.text_item = QGraphicsTextItem(self)
        self.text_item.setDefaultTextColor(Qt.black)
        self.text_item.setZValue(1)

        format = QTextCharFormat()
        format.setBackground(QBrush(QColor(255, 255, 255, 128)))
        cursor = self.text_item.textCursor()
        cursor.select(cursor.Document)
        cursor.mergeCharFormat(format)
        self.text_item.setTextCursor(cursor)

        self.set_label(self.label_text)

        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)

    def set_label(self, value: str):
        self.label_text = str(value)
        self.text_item.setPlainText(self.label_text)

        text_rect = self.text_item.boundingRect()
        x = (self.size - text_rect.width()) / 2
        self.text_item.setPos(x, -20)

    def unhide(self, show: bool):
        # Меняем состояние видимости круга
        self.is_visible = show
        self.update()  # Перерисовываем объект после изменения состояния

    def set_radius(self, new_radius: float):
        # Пример: вместо изменения радиуса меняем его видимость
        self.is_visible = True  # Переключаем видимость
        self.radius = new_radius
        self.update()  # Перерисовываем объект после изменения

    def boundingRect(self):
        margin = self.radius - self.size / 2
        return QRectF(-margin, -margin - 20, self.size + 2 * margin, self.size + 2 * margin + 20)

    def delete(self):
        if self.scene():
            self.scene().removeItem(self)

    def paint(self, painter, option, widget=None):
        rect = QRectF(0, 0, self.size, self.size)

        # Отрисовка основной фигуры (квадрат)
        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(Qt.black, 2))
        painter.drawRect(rect)

        if self.is_visible:

            # Отрисовка полупрозрачного красного круга, если он видим
            circle_rect = QRectF(
                (self.size - self.radius) / 2,
                (self.size - self.radius) / 2,
                self.radius,
                self.radius
            )
            painter.setBrush(QColor(255, 0, 0, 50))  # Полупрозрачная красная заливка
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(circle_rect)

        # Отрисовка рамки, если есть фокус
        if self.has_focus:
            focus_rect = rect.adjusted(-20, -20, 20, 20)

            pen = QPen(QColor(255, 0, 0), 2, Qt.DashLine)
            painter.setPen(pen)

            painter.setBrush(QColor(255, 0, 0, 10))  # Полупрозрачная красная заливка
            painter.drawRect(focus_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Сброс фокуса у других DangerItem на сцене
            for item in self.scene().items():
                if isinstance(item, DangerItem) and item is not self:
                    item.has_focus = False
                    item.update()

            # Установка фокуса на текущий объект
            self.has_focus = True
            self.update()
            event.accept()
        else:
            super().mousePressEvent(event)
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.is_dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            new_pos = event.scenePos() - self.offset
            self.setPos(new_pos)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False

    def contextMenuEvent(self, event):
        menu = QMenu()
        toggle_label_action = QAction("Скрыть наименование" if self.text_item.isVisible() else "Показать наименование")
        delete_action = QAction("Удалить объект")
        menu.addAction(toggle_label_action)
        menu.addAction(delete_action)
        action = menu.exec_(event.screenPos())

        if action == toggle_label_action:
            self.text_item.setVisible(not self.text_item.isVisible())
        elif action == delete_action:
            self.delete()




class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Создаём сцену и представление
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)

        # Пример: добавим прямоугольник
        # rect = self.scene.addRect(0, 0, 100, 50, QPen(Qt.black), QBrush(QColor("lightblue")))
        item = DangerItem(size=100, color=QColor("orange"), label="Взрыв-вспышка на объекте 1")

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
