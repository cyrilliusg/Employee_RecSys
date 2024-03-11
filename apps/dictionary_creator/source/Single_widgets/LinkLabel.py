from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, pyqtSignal


class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # Сигнал, который будет испускаться при клике

    def __init__(self, parent=None, ):
        super().__init__(parent)
        self.setTextFormat(Qt.TextFormat.RichText)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.setOpenExternalLinks(True)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()  # Испускаем сигнал при клике левой кнопкой мыши
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        # Изменение курсора на вид указателя, как у ссылок
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Возвращение курсора к стандартному виду
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)

    def setRole(self, role):
        if role == 'hyperlink':
            self.setStyleSheet("color: blue; text-decoration: underline;")
        elif role == 'controller':
            self.setStyleSheet("color: black; text-decoration: underline; font: bold;")
