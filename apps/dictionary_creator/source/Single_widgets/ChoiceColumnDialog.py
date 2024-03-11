from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QDialog, QHBoxLayout, QComboBox
from PyQt6.QtCore import Qt

class ChoiceColumnDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Вопрос пользователю
        self.label = QLabel(self)
        self.label.setText('Выберите колонку, слова которой будут использованы для словаря:')
        layout.addWidget(self.label)
        h_layout = QHBoxLayout()
        # ComboBox для выбора
        self.combobox = QComboBox(self)
        self.ok = QPushButton(self)
        self.ok.setText('Принять')
        self.ok.clicked.connect(self.accept)
        h_layout.addWidget(self.combobox)
        h_layout.addWidget(self.ok)
        layout.addLayout(h_layout)

        self.setLayout(layout)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    def get_value(self):
        return self.combobox.currentText()

    def set_values(self, text):
        if not isinstance(text, list):
            text = [text]
        self.combobox.addItems(text)
