from PyQt6.QtWidgets import QVBoxLayout, QWidget, QApplication, QTableView, QHeaderView
import sys
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtGui import QStandardItemModel, QStandardItem


class DictionaryView_GUI(QWidget):
    def __init__(self, db_path):
        super().__init__()

        self.db_path = db_path
        self.layout = QVBoxLayout(self)

        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)
        self.setLayout(self.layout)

        self.setWindowTitle('Просмотр словаря')
        self.showMaximized()
        self.db = None
        self.initialize_db()
        self.display_data()
        self.table_settings()

    def table_settings(self):
        # Растягиваем столбцы, чтобы они занимали все доступное горизонтальное пространство
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.resizeColumnsToContents()

    def initialize_db(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.db_path)  # Замените на путь к вашей базе данных
        if not self.db.open():
            print("Cannot open database")
            return False
        return True

    def display_data(self):
        query = QSqlQuery(self.db)
        query.exec("SELECT value, source FROM dictionary")

        # Создаем модель для отображения данных
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Эталонный словарь', 'Добавленное слово', 'Отклоненное слово'])

        # Словарь для хранения значений по категориям
        data = {'1': [], '0': [], '2': []}
        while query.next():
            value = query.value(0)
            source = query.value(1)
            data[str(source)].append(value)

        # Наибольшее количество элементов в категории для определения количества строк
        max_len = max(len(data[key]) for key in data)
        # Добавляем данные в модель
        for row in range(max_len):
            for col, key in enumerate(['1', '0', '2']):  # Явно указываем порядок ключей
                try:
                    item = QStandardItem(data[key][row])
                except IndexError:
                    item = QStandardItem("")  # Пустая ячейка, если данных нет
                model.setItem(row, col, item)

        self.table_view.setModel(model)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = DictionaryView_GUI()
    mainWindow.show()
    sys.exit(app.exec())
