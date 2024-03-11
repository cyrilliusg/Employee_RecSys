from PyQt6.QtWidgets import QLabel, QMessageBox


class DialogWidget(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = None
        self.parent = 2
        self.setWindowTitle("Уведомление")
        self.setText(
            "Обработка произведена успешно!")
        self.setIcon(QMessageBox.Icon.Information)

        # Создаем QLabel с гиперссылкой
        self.label = QLabel('<a href="link">открыть папку с файлом</a>')
        self.label.setOpenExternalLinks(False)  # Важно! Для обработки кликов внутри приложения

        # Добавляем QLabel в QMessageBox
        self.layout().addWidget(self.label)

    def set_path(self, filepath):
        self.label.linkActivated.connect(lambda: self.open_file(filepath))

    def set_controller(self, controller):
        self.controller = controller

    def open_file(self, path):
        self.controller.handle_request({'code': self.parent, 'value': path})

    def set_parent(self, parent):
        self.parent = parent
