from PyQt5.QtCore import Qt, QPoint, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPen, QColor, QCursor, QImage
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem, QFileDialog
from danger_object import DangerItem
from scale.scale import CoordinateSystem


class GraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.X = 0  # X coord of img
        self.Y = 0  # Y coord of img
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.image_item = None  # Хранит изображение
        self.setAlignment(Qt.AlignCenter)  # Выравнивание по центру
        self.setRenderHint(QPainter.Antialiasing)

        self.selecting_position = False  # Флаг для активации выбора
        # Параметры масштабирования

        self._zoom = 1.0
        self._zoom_step = 0.1
        self._zoom_min = 0.5
        self._zoom_max = 2.0

        self._panning = False
        self._pan_start = QPoint()

    def set_image(self, path):
        """Загружает изображение из файла и добавляет его в сцену."""
        pixmap = QPixmap(path)  # Загружаем изображение
        if pixmap.isNull():
            print("Ошибка: не удалось загрузить изображение!")
            return

        if self.image_item:
            self.scene.removeItem(self.image_item)  # Удаляем предыдущее изображение

        self.image_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.image_item)


        # Автомасштабирование, чтобы изображение поместилось
        self.fitInView(self.image_item, Qt.KeepAspectRatio)
        if self.image_item:
            rect = self.image_item.boundingRect()
            # Левая нижняя точка (в координатах изображения)
            bottom_left = rect.bottomLeft()
            self.X, self.Y = rect.topRight().x(), rect.bottomLeft().y()
            self.coord_system = CoordinateSystem(width=self.X, height=self.Y)
            self.scene.addItem(self.coord_system)

    def enable_point_selection(self):
        self.selecting_position = True
        self.setCursor(QCursor(Qt.PointingHandCursor))

    @classmethod
    def coord_convert(cls, x, y):
        return x, cls.Y - y

    def save_image(self):
        # Открываем диалоговое окно для выбора места сохранения
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить изображение", "Проект", "PNG файлы (*.png);;Все файлы (*.*)"
        )
        # Если пользователь выбрал путь для сохранения
        if file_path:
            image = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
            painter = QPainter(image)
            painter.setRenderHint(QPainter.Antialiasing)
            self.scene.render(painter)
            painter.end()

            # Сохраняем изображение в выбранный файл
            if not image.save(file_path):
                print("Ошибка: не удалось сохранить изображение!")
            else:
                print(f"Изображение успешно сохранено в {file_path}")


    def add_item(self, coordinates=(0, 0)):
        x, y = coordinates
        size = min(self.X,self.Y)//40
        item = DangerItem(size=size, x=x-size/2, y=y-size/2, color=QColor("orange"), label="Взрыв-вспышка на объекте 1")
        self.scene.addItem(item)

    def get_focused_danger_item(self):
        """Возвращает DangerItem, который сейчас в фокусе, если такой есть."""
        item = self.scene.focusItem()
        if isinstance(item, DangerItem):
            return item
        return None
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier:
            self._panning = True
            self.setCursor(Qt.ClosedHandCursor)
            self._pan_start = event.pos()
        elif self.selecting_position and event.button() == Qt.LeftButton:
            scene_pos = self.mapToScene(event.pos())
            x, y = scene_pos.x(), scene_pos.y()
            self.add_item((x, y))
            self.setCursor(QCursor(Qt.ArrowCursor))
            self.selecting_position = False
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._panning:
            delta = self._pan_start - event.pos()
            self._pan_start = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + delta.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._panning and event.button() == Qt.LeftButton:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        angle_delta = event.angleDelta().y()
        if angle_delta > 0 and self._zoom < self._zoom_max:
            zoom_factor = 1 + self._zoom_step
        elif angle_delta < 0 and self._zoom > self._zoom_min:
            zoom_factor = 1 - self._zoom_step
        else:
            return
        self._zoom *= zoom_factor
        self.scale(zoom_factor, zoom_factor)