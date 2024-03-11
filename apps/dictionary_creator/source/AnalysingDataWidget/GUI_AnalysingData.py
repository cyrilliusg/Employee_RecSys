from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from .GUI_Workspace import WorkspaceWidget


class AnalysingDataGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.controller = None

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.label_total = QLabel(self)

        self.label_info = QLabel('<b>Данные о клиенте:</b>', self)

        self.label_department = QLabel(self)
        self.label_unit = QLabel(self)
        self.label_job_name = QLabel(self)
        self.layout.addWidget(self.label_total)
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.layout.addSpacerItem(spacer)
        self.layout.addWidget(self.label_info)
        self.layout.addWidget(self.label_department)
        self.layout.addWidget(self.label_unit)
        self.layout.addWidget(self.label_job_name)
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.layout.addSpacerItem(spacer)
        self.widget_buttons = WorkspaceWidget(self)
        self.layout.addWidget(self.widget_buttons)
        self.widget_buttons.choice.connect(self.user_choice)

        self.button_next = QPushButton('Далее', self)
        self.layout.addWidget(self.button_next)
        self.button_next.clicked.connect(self.next_row)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    def set_label(self, current, total):
        self.label_total.setText(f'Проверено: {current}/{total}')

    def set_new_row(self, department_value, unit_value, job_name_value, values):
        # Дополнительное форматирование для выделения текста из списка values синим цветом
        for value in values:
            if value in department_value:
                department_value = department_value.replace(value, f"<span style='color: blue;'>{value}</span>")
            if value in unit_value:
                unit_value = unit_value.replace(value, f"<span style='color: blue;'>{value}</span>")
            if value in job_name_value:
                job_name_value = job_name_value.replace(value, f"<span style='color: blue;'>{value}</span>")

        # Обновление текста с учетом выделения
        self.label_department.setText(f"<b>Департамент:</b> {department_value}")
        self.label_unit.setText(f"<b>Отдел:</b> {unit_value}")
        self.label_job_name.setText(f"<b>Название должности:</b> {job_name_value}")

        self.widget_buttons.set_label_button_pairs(values)

    def set_controller(self, controller):
        self.controller = controller

    def next_row(self):
        self.controller.handle_request({'code': 1, 'value': None})

    def user_choice(self, value):
        self.controller.handle_request(value)

    def end_scenary(self):
        self.widget_buttons.clear_label_button_pairs()
        self.label_total.setText('Проверка завершена')

    def hide_value(self, value):
        self.widget_buttons.hide_value(value)

    def closeEvent(self, event):
        self.controller.handle_request({'code': 3, 'value': None})
        event.accept()
