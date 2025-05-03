from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction, QMessageBox, QFileDialog


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        #-----------------ФАЙЛ---------------------
        self.filemenu_menu = QMenu("Файл")
        self.addMenu(self.filemenu_menu)

        #TODO прописать открытие картинки
        self.new_file = QAction(QIcon("img/create__menubar.png"),"Создать...", self)
        self.new_file.setShortcut("Ctrl+N")
        self.new_file.triggered.connect(self.create_new_file)
        self.filemenu_menu.addAction(self.new_file)

        #TODO прописать открытие самого проекта
        self.open_file = QAction(QIcon("img/openfile__menubar.png"), "Открыть...", self)
        self.open_file.setShortcut("Ctrl+O")
        self.open_file.triggered.connect(self.open_file_dialog)
        self.filemenu_menu.addAction(self.open_file)

        #TODO Сохранение проекта или картинки?
        self.save_file = QAction(QIcon("img/save__menubar.png"), "Сохранить", self)
        self.save_file.setShortcut("Ctrl+S")
        self.save_file.triggered.connect(self.saving_file)
        self.filemenu_menu.addAction(self.save_file)

        #TODO Сохранение проекта или картинки?.
        self.saveas_file = QAction("Сохранить как...", self)
        self.saveas_file.setShortcut("Ctrl+S")
        self.saveas_file.triggered.connect(self.saving_file)
        self.filemenu_menu.addAction(self.saveas_file)

        self.filemenu_menu.addSeparator()

        #TODO Настройки прописать как виджет
        self.settings_file = QAction(QIcon("img/settings__menubar.png"), "Настройки", self)
        self.settings_file.triggered.connect(self.saving_file)
        self.filemenu_menu.addAction(self.settings_file)

        self.filemenu_menu.addSeparator()
        #TODO добавить предупреждение перед выходом
        exit_action = QAction("Выход", self)
        # exit_action.triggered.connect(parent.close)  # Закрывает приложение
        self.filemenu_menu.addAction(exit_action)

        #-----------------ВИД---------------------
        self.view_menu = QMenu("Вид")
        self.addMenu(self.view_menu)

        # -----------------Помощь---------------------
        self.help_menu = QMenu("Помощь")
        self.addMenu(self.help_menu)



    def create_new_file(self):
        print("Создание нового файла...")

    def open_file_dialog(self):
        try:
            options = QFileDialog.Options()
            self.file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Выберите изображение",
                "",
                "Изображения (*.png *.jpg *.jpeg *.bmp *.gif);;Все файлы (*)",
                options=options
            )

            if not self.file_path:  # Если файл не выбран
                print("Файл не выбран")
                return

            print(f"Выбран файл: {self.file_path}")

            parent = self.parent()  # Получаем родительский объект (MainWindow)
            if parent is None:
                print("Ошибка: не удалось получить родительский объект")
                return

            if hasattr(parent, "graphics_view"):
                try:
                    parent.graphics_view.set_image(self.file_path)
                except Exception as e:
                    print(f"Ошибка при установке изображения: {e}")
            else:
                print("Ошибка: объект graphics_view не найден у родителя")

        except Exception as e:
            print(f"Ошибка при открытии файла: {e}")

    def saving_file(self):
        self.parent().graphics_view.save_image()

