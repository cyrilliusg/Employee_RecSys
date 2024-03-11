from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QDialog, QHBoxLayout, QLineEdit
from PyQt6.QtCore import pyqtSignal


class DataQuestionWidget(QDialog):
    user_choice_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Вопрос пользователю
        self.label = QLabel(self)

        layout.addWidget(self.label)
        h_layout = QHBoxLayout()
        # ComboBox для выбора
        self.yes = QPushButton(self)
        self.yes.setText('Да')
        self.no = QPushButton(self)
        self.no.setText('Нет')
        self.yes.clicked.connect(self.confirm_choice)
        self.no.clicked.connect(self.confirm_choice)
        h_layout.addWidget(self.yes)
        h_layout.addWidget(self.no)
        layout.addLayout(h_layout)

        self.setLayout(layout)

    def confirm_choice(self):
        btn = self.sender()
        # Отправляем сигнал с выбранным ответом
        self.user_choice_signal.emit({'question': self.question_label.text(), 'value': btn.text() == 'Да'})
        self.close()

    def set_text(self, text):
        self.question_label.setText(text)
