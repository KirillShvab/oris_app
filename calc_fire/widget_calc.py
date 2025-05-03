from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout, QLabel, QSpacerItem, QComboBox, \
    QDoubleSpinBox, QGroupBox, QPushButton, QTextEdit

from calc_fire.fire_radius import calculate_flash_fire_radius
from calc_fire.radius_nkpr import rho_temperature, calculate_nkpr_zone
from calc_fire import nkpr_dict
from danger_object import DangerItem


class FireRadiusWindow(QWidget):
    def __init__(self, item :DangerItem,convert_to_pixels):
        super().__init__()
        self._item = item
        self.convert_to_pixels = convert_to_pixels
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        groupbox = QGroupBox("Взрыв-вспышка")
        groupbox.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
            }
        """)
        groupbox_substance = QGroupBox("")
        groupbox_condition = QGroupBox("Условия аварии")
        groupbox_condition.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
            }
        """)
        self.setWindowTitle("Расчет")
        self.setFixedSize(500,500)

        groupbox_layer = QVBoxLayout()
        groupbox_substance_layer = QVBoxLayout()
        groupbox_condition_layer = QVBoxLayout()
        groupbox.setLayout(groupbox_layer)
        groupbox_substance.setLayout(groupbox_substance_layer)
        groupbox_condition.setLayout(groupbox_condition_layer)
        groupbox_condition_layer.addWidget(groupbox_condition)
        groupbox_layer.addWidget(groupbox_substance)
        groupbox_layer.addWidget(groupbox_condition)

        # substance_layer = QVBoxLayout()

        # Слой вещества
        substance_label = QLabel("Вещество")
        self.substance_combobox = QComboBox()
        self.substance_combobox.setMaximumWidth(200)
        self.substance_combobox.addItems(nkpr_dict.keys())


        groupbox_substance_layer.addWidget(substance_label)
        groupbox_substance_layer.addWidget(self.substance_combobox)

        # НКПР
        nkpr_label = QLabel("НКПР")
        self.nkpr_doublespin = QDoubleSpinBox()
        self.nkpr_doublespin.setMaximumWidth(100)
        self.nkpr_doublespin.setRange(0.00, 100)
        self.nkpr_doublespin.setSingleStep(0.01)
        self.nkpr_doublespin.setValue(nkpr_dict.get('Пропан').get('nkpr',0))


        groupbox_substance_layer.addWidget(nkpr_label)
        groupbox_substance_layer.addWidget(self.nkpr_doublespin)



        molar_mass_label = QLabel("Молярная масса")
        self.molar_mass_doublespin = QDoubleSpinBox()
        self.molar_mass_doublespin.setMaximumWidth(100)
        self.molar_mass_doublespin.setRange(0.00, 1000)
        self.molar_mass_doublespin.setSingleStep(0.01)
        self.molar_mass_doublespin.setValue(nkpr_dict.get('Пропан').get('molar_mass',0))

        groupbox_substance_layer.addWidget(molar_mass_label)
        groupbox_substance_layer.addWidget(self.molar_mass_doublespin)
        # Условия аварии
        mass_label = QLabel("Масса вещества")
        self.mass_doublespin = QDoubleSpinBox()
        self.mass_doublespin.setMaximumWidth(100)
        self.mass_doublespin.setRange(0.00, 1000000000)
        self.mass_doublespin.setSingleStep(0.1)
        self.mass_doublespin.setValue(2000)

        groupbox_condition_layer.addWidget(mass_label)
        groupbox_condition_layer.addWidget(self.mass_doublespin)

        temperature_label = QLabel("Температура среды")
        self.temperature_doublespin = QDoubleSpinBox()
        self.temperature_doublespin.setMaximumWidth(100)
        self.temperature_doublespin.setRange(0.00, 20000)
        self.temperature_doublespin.setSingleStep(0.1)
        self.temperature_doublespin.setValue(25)
        groupbox_condition_layer.addWidget(temperature_label)
        groupbox_condition_layer.addWidget(self.temperature_doublespin)

        groupbox_layer.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_calc = QPushButton("Рассчитать")
        button_calc.clicked.connect(self.show_calc)
        button_calc.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb(255, 180, 50),
                    stop:1 rgb(255, 140, 0)
                );
                color: black;
                border: 2px solid rgb(180, 100, 0);
                border-radius: 5px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb(255, 200, 80),
                    stop:1 rgb(255, 160, 20)
                );
            }
            QPushButton:pressed {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb(200, 110, 0),
                    stop:1 rgb(160, 80, 0)
                );
                padding-top: 7px; /* эффект нажатия вниз */
                padding-bottom: 5px;
            }
        """)
        button_apply = QPushButton("Применить")
        button_apply.clicked.connect(self.apply_calc)
        button_apply.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb(76, 220, 133),
                    stop:1 rgb(39, 174, 96)
                );
                color: black;
                border: 2px solid rgb(32, 142, 79);
                border-radius: 5px;
                padding: 6px 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb(96, 235, 150),
                    stop:1 rgb(46, 204, 113)
                );
            }
            QPushButton:pressed {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb(33, 140, 87),
                    stop:1 rgb(22, 110, 65)
                );
                padding-top: 7px;
                padding-bottom: 5px;
            }
        """)
        groupbox_layer.addWidget(button_calc)
        groupbox_layer.addWidget(button_apply)

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(groupbox)
        main_layout.addWidget(self.text_edit)

        self.substance_combobox.currentTextChanged.connect(self.update_substance_data)

        self.setLayout(main_layout)

    def update_substance_data(self, substance_name):
        data = nkpr_dict.get(substance_name, {})
        self.nkpr_doublespin.setValue(data.get('nkpr', 0))
        self.molar_mass_doublespin.setValue(data.get('molar_mass', 0))

    def show_calc(self):

        molar_mass = self.molar_mass_doublespin.value()
        mass = self.mass_doublespin.value()
        temperature = self.temperature_doublespin.value()
        rho = rho_temperature(molar_mass, temperature)

        # Рассчитываем НКПР для зоны
        nkpr = self.nkpr_doublespin.value()
        self.r_nkpr = calculate_nkpr_zone(mass, rho, nkpr)

        self.r_f = calculate_flash_fire_radius(self.r_nkpr[0])
        output = \
output = f"""
<pre>
{'-'*30}
Расчёт взрыв-вспышки
{'-'*30}
НКПР:              {nkpr:.2f}
Температура:       {temperature:.2f}
Молярная масса:    {molar_mass:.2f}
Плотность:         {rho:.2f}
Масса:             {mass:.2f}
{'_'*30}
R_НКПР (радиус):   {self.r_nkpr[0]:.2f} м
Z_НКПР (высота):   {self.r_nkpr[1]:.2f} м
R_F (радиус):      {self.r_f:.2f} м
{'_'*30}

</pre>

"""
        self.text_edit.append(output)
    def apply_calc(self):
        self._item.set_radius(self.convert_to_pixels(self.r_f))

def main():
    from PyQt5.QtWidgets import QApplication
    from menu_window import MainMenu
    app = QApplication([])
    menu = FireRadiusWindow()
    menu.show()
    app.exec()


if __name__ == '__main__':
    main()

