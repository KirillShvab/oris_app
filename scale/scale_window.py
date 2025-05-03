from PyQt5.QtWidgets import QVBoxLayout, QLabel, QSpinBox, QWidget


class ScaleWindow(QWidget):
    def __init__(self, graphics_view):
        super().__init__()
        self.graphics_view = graphics_view
        # Создаем вертикальный слой
        layout = QVBoxLayout()

        # Создаем QLabel
        self.label = QLabel("Выберите длину шага шкалы")
        self.label_metr = QLabel("Выберите длину м.")
        # Создаем QSpinBox и настраиваем его
        self.spinbox = QSpinBox()
        self.spinbox.setMaximumWidth(60)
        self.spinbox.setRange(1, 200)
        self.spinbox.setSingleStep(1)
        self.spinbox.setValue(100)

        self.spinbox_metr = QSpinBox()
        self.spinbox_metr.setMaximumWidth(60)

        self.spinbox_metr.setRange(1, 500)
        self.spinbox_metr.setSingleStep(1)
        self.spinbox_metr.setValue(50)

        # Подключаем обработчик события изменения значения
        self.spinbox.valueChanged.connect(self.on_spinbox_value_changed)

        # Добавляем виджеты в слой
        layout.addWidget(self.label)
        layout.addWidget(self.spinbox)
        layout.addWidget(self.label_metr)
        layout.addWidget(self.spinbox_metr)
        # Устанавливаем слой в качестве основного
        self.setLayout(layout)

    def on_spinbox_value_changed(self, value):
        print(f"SpinBox changed: {value}")
        # Можно также обновить текст на метке, например:
        self.graphics_view.coord_system.update_scale(value)

    def on_spinbox_value_changed_length(self, value):
        self.graphics_view.coord_system.update_length(value)


def main():
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    menu = ScaleWindow()
    menu.show()
    app.exec()


if __name__ == '__main__':
    main()
