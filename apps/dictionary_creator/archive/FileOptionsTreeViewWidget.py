from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTreeView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
import sys


class FileOptionsTreeViewWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        # Создание модели и древовидного виджета
        self.model = QStandardItemModel()
        self.tree_view = QTreeView(self)
        self.tree_view.setModel(self.model)
        self.tree_view.clicked.connect(self.on_item_clicked)
        self.layout.addWidget(self.tree_view)

        # Добавление элементов в модель
        self.add_tree_items()

    def add_tree_items(self):
        # Установка заголовков столбцов
        self.model.setHorizontalHeaderLabels(["Параметр", "Значение"])

        # Создание элемента верхнего уровня
        top_item = QStandardItem("Дополнительные параметры файла")
        top_item.setFlags(top_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Сделать нередактируемым
        self.model.appendRow(top_item)

        # Добавление дочерних элементов
        for i in range(3):
            label_item = QStandardItem(f"Параметр {i + 1}")
            label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Сделать нередактируемым
            placeholder_text = f"По умолчанию: параметр {i + 1}"
            value_item = QStandardItem(placeholder_text)  # Текст-подсказка
            top_item.appendRow([label_item, value_item])

        # Настройка ширины столбцов по содержимому
        for column in range(self.model.columnCount()):
            self.tree_view.resizeColumnToContents(column)

    def on_item_clicked(self, index):
        item = self.model.itemFromIndex(index)
        if item.text().startswith("По умолчанию: "):
            item.setText("")

    def get_values(self):
        values = {}
        root_item = self.model.item(0)  # Корневой элемент
        for i in range(root_item.rowCount()):
            param = root_item.child(i, 0).text()  # Получение текста параметра
            value = root_item.child(i, 1).text()  # Получение значения
            if value.startswith("По умолчанию: "):
                value = ""  # Очистить значение, если оно еще содержит текст-подсказку
            values[param] = value
        print(values)  # Вывод или обработка словаря значений



