from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, \
    QHBoxLayout, QSpacerItem, QSizePolicy
from ..Single_widgets.LinkLabel import ClickableLabel
from ..Single_widgets.FileOptionsTableWidget import FileOptionsTableWidget


class FileSelectorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.filePathLineEdit.setReadOnly(True)
        self.fileSelectButton.clicked.connect(self.openFileNameDialog)
        self.startButton.clicked.connect(self.start_processing)

        self.controller = None

        self.table_file_params_visible = False

        self.stemmingCheckbox.setChecked(True)
        self.concatenateCheckbox.setChecked(True)
        self.standardCleaningCheckbox.setChecked(True)

    def initUI(self):
        self.main_layout = QVBoxLayout()

        # Группа для выбора файла
        layout = QVBoxLayout()
        self.fileLabel = QLabel('Выберите файл:')
        self.filePathLineEdit = QLineEdit()
        self.fileSelectButton = QPushButton('Обзор...')
        file_hor_layout = QHBoxLayout()
        layout.addWidget(self.fileLabel)
        file_hor_layout.addWidget(self.filePathLineEdit)
        file_hor_layout.addWidget(self.fileSelectButton)
        layout.addLayout(file_hor_layout)
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.main_layout.addSpacerItem(spacer)
        self.main_layout.addLayout(layout)

        # Дополнительные параметры файлв
        self.label_params = ClickableLabel()
        self.label_params.setText('Дополнительные параметры')
        self.label_params.setRole('controller')
        self.label_params.clicked.connect(self.control_table_file_params)
        self.main_layout.addWidget(self.label_params)
        # Дополнительные параметры файлв
        # self.table_file_params = FileOptionsTreeViewWidget()
        self.table_file_params = FileOptionsTableWidget(
            table_items={'Имя результирующей колонки': "По умолчанию: 'combined'",
                         'Диапазон колонок для считывания': 'По умолчанию: весь файл'})

        self.table_file_params.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.main_layout.addWidget(self.table_file_params)
        self.table_file_params.hide()

        # Checkbox для стандартной первичной очистки
        self.standardCleaningCheckbox = QCheckBox('Стандартная первичная очистка')
        self.main_layout.addWidget(self.standardCleaningCheckbox)
        # Checkbox для стемминга
        self.stemmingCheckbox = QCheckBox('Стэмминг')
        self.main_layout.addWidget(self.stemmingCheckbox)
        # Checkbox для конкатенации строк и оставления уникальных
        self.concatenateCheckbox = QCheckBox('Конкатенация колонок и удаление дублирующихся слов')
        self.main_layout.addWidget(self.concatenateCheckbox)
        # Кнопка начать
        self.startButton = QPushButton('Начать')
        self.main_layout.addWidget(self.startButton)
        self.setLayout(self.main_layout)
        self.setWindowTitle('Преобразование данных')
        self.setMinimumSize(450, 400)

    def set_controller(self, controller):
        self.controller = controller

    def get_params(self):

        return {
            '0': {'path': self.filePathLineEdit.text(), **self.table_file_params.get_values()},
            '1': self.stemmingCheckbox.isChecked(),
            '2': self.standardCleaningCheckbox.isChecked(),
            '3': self.concatenateCheckbox.isChecked()
        }

    def set_lineedit(self, value):
        self.filePathLineEdit.setText(value)

    def openFileNameDialog(self):
        self.controller.handle_request({'code': 0, 'value': None})

    def start_processing(self):
        self.controller.handle_request({'code': 1, 'value': None})

    def control_table_file_params(self):
        if self.table_file_params_visible:
            self.table_file_params.hide()
            self.table_file_params_visible = False
        else:
            self.table_file_params.show()
            self.table_file_params_visible = True
