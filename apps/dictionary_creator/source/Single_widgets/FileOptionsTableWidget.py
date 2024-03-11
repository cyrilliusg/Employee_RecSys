from PyQt6.QtWidgets import QStyledItemDelegate, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt


class PlaceholderDelegate(QStyledItemDelegate):
    def __init__(self, placeholder_text, parent=None):
        super().__init__(parent)
        self.placeholder_text = placeholder_text

    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            editor.setPlaceholderText(self.placeholder_text)
        return editor


class FileOptionsTableWidget(QTableWidget):
    def __init__(self, table_items=None):
        super().__init__()
        # . Для своего выбора указать в формате "A:C, E:G" и т.п.
        self.table_items = table_items
        self.items_sys_names = {'Имя результирующей колонки': 'o_col',
                                'Диапазон колонок для считывания': 'i_col_range'}

        # Создание таблицы
        self.setColumnCount(2)  # Две колонки
        self.setHorizontalHeaderLabels(["Параметр", "Значение"])
        self.verticalHeader().setVisible(False)  # Скрыть индексы строк
        self.setShowGrid(False)  # Скрыть линии разделения ячеек

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Добавление элементов в таблицу
        self.add_table_items()

    def add_table_items(self):
        self.setRowCount(2)  # Установить количество строк

        # Добавление данных в каждую строку
        for k, v in self.table_items.items():
            index = list(self.table_items.keys()).index(k)
            # Параметр
            param_item = QTableWidgetItem(k)
            param_item.setFlags(param_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Сделать ячейку нередактируемой
            self.setItem(index, 0, param_item)

            # Значение с вспомогательным текстом
            placeholder_text = v
            value_item = QTableWidgetItem("")
            self.setItem(index, 1, value_item)
            self.setItemDelegateForRow(index, PlaceholderDelegate(placeholder_text, self))

        # Настройка ширины столбцов по содержимому
        self.resizeColumnsToContents()

    def get_values(self):
        values = {}
        for i in range(self.rowCount()):
            param = self.item(i, 0).text()  # Получение текста параметра
            value = self.item(i, 1).text()  # Получение значения
            if value == '':
                value = None
            values[self.items_sys_names[param]] = value
        return values
