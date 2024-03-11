from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from ..Single_widgets.EditableLabel import EditableLabel
from PyQt6.QtCore import pyqtSignal


class WorkspaceWidget(QWidget):
    choice = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label_button_pairs = {}
        self.pair_layouts = []
        self.user_signals_codes = {'Да': 0, 'Нет': 2}  # от родителя
        self.reference_words = {}

    def set_label_button_pairs(self, words):
        self.clear_label_button_pairs()
        for word in words:
            label = EditableLabel(word)
            self.label_button_pairs[label] = []
            button = QPushButton('Да')
            button.clicked.connect(self.user_choice)
            self.label_button_pairs[label].append(button)
            # Создание горизонтального макета для каждой пары
            h_layout = QHBoxLayout()
            h_layout.addWidget(label)
            h_layout.addWidget(button)
            button = QPushButton('Нет')
            button.clicked.connect(self.user_choice)
            h_layout.addWidget(button)
            self.layout.addLayout(h_layout)
            self.pair_layouts.append(h_layout)
            self.label_button_pairs[label].append(button)

            self.reference_words[label] = word
        print('новая строка')
        print(self.reference_words)
        print(self.label_button_pairs)

    def clear_label_button_pairs(self):
        """
        Удаление всех пар виджетов слов
        """
        while self.pair_layouts:
            h_layout = self.pair_layouts.pop()
            while h_layout.count():
                item = h_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            h_layout.deleteLater()

        self.label_button_pairs = {}
        self.pair_layouts = []
        self.reference_words = {}

    def hide_value(self, text):
        """
        скрывает пару виджетов по значению
        :param value: текст
        """
        print('скрыть')
        print(self.reference_words)
        print(self.label_button_pairs)
        label_obj = self._find_label(text)
        for button in self.label_button_pairs[label_obj]:
            button.hide()

    def _find_label(self, text):
        """
        Ищет объект лейбла в словаре по его тексту
        :param text: текст лейбла
        :return: объект лейбла
        """
        print('find', self.label_button_pairs)
        for k in self.label_button_pairs.keys():
            if text == k.text():
                return k

    def user_choice(self):
        # Определение кнопки, которая была нажата
        pressed_button = self.sender()
        if pressed_button:
            for label, buttons_list in self.label_button_pairs.items():
                for button in buttons_list:
                    if button == pressed_button:
                        self.choice.emit(
                            {'code': self.user_signals_codes[pressed_button.text()],
                             'value': label.text(),
                             'original_value': self.reference_words[label]})
                        return
