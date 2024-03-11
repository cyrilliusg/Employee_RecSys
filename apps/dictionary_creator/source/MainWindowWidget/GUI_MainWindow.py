from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QWidget, QPushButton
from PyQt6.QtGui import QAction
from ..Single_widgets.LinkLabel import ClickableLabel


class MainWidget_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.controller = None
        self.button_create.clicked.connect(self.create)
        self.button_edit.clicked.connect(self.edit)
        self.button_read.clicked.connect(self.read)
        self.button_download.clicked.connect(self.download)
        self.delete_memory_label.clicked.connect(self.delete)
        self.process_file.triggered.connect(self.open_process_file)
        self.manual.triggered.connect(self.open_manual)
        self.about_programm.triggered.connect(self.open_about_programm)

    def initUI(self):
        central_widget = QWidget()  # Центральный виджет для QMainWindow
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # Группа для выбора файла
        header_layout = QHBoxLayout()
        self.total_words_label = QLabel('Слов в словаре: 0')
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.delete_memory_label = ClickableLabel()
        self.delete_memory_label.setRole('controller')
        self.delete_memory_label.setText('Очистить память')
        header_layout.addWidget(self.total_words_label)
        header_layout.addSpacerItem(spacer)
        header_layout.addWidget(self.delete_memory_label)
        self.main_layout.addLayout(header_layout)
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.main_layout.addSpacerItem(spacer)

        self.button_create = QPushButton(self)
        self.button_create.setText('Создать')
        self.main_layout.addWidget(self.button_create)

        self.button_edit = QPushButton(self)
        self.button_edit.setText('Редактировать')
        self.main_layout.addWidget(self.button_edit)

        self.button_read = QPushButton(self)
        self.button_read.setText('Просмотреть')
        self.main_layout.addWidget(self.button_read)

        self.button_download = QPushButton(self)
        self.button_download.setText('Скачать')
        self.main_layout.addWidget(self.button_download)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("Инструменты")
        referenceMenu = menuBar.addMenu("Справка")

        # Создаем действия (с обработчиками, если нужно)
        self.process_file = QAction("Обработка данных", self)
        fileMenu.addAction(self.process_file)
        self.manual = QAction("Инструкция по работе", self)
        referenceMenu.addAction(self.manual)
        self.about_programm = QAction("О программе", self)
        referenceMenu.addAction(self.about_programm)

        self.setWindowTitle('Управление словарём')
        self.setMinimumSize(350, 250)

    def set_controller(self, controller):
        self.controller = controller

    def create(self):
        self.controller.handle_request({'code': 0, 'value': None})

    def edit(self):
        self.controller.handle_request({'code': 1, 'value': None})

    def read(self):
        self.controller.handle_request({'code': 2, 'value': None})

    def delete(self):
        self.controller.handle_request({'code': 3, 'value': None})

    def download(self):
        self.controller.handle_request({'code': 4, 'value': None})

    def open_process_file(self):
        self.controller.handle_request({'code': 5, 'value': None})

    def set_dict_len_label(self, value):
        self.total_words_label.setText(f'Слов в словаре: {value}')

    def open_manual(self):
        self.controller.handle_request({'code': 6, 'value': None})

    def open_about_programm(self):
        self.controller.handle_request({'code': 7, 'value': None})
