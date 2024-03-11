from PyQt6.QtWidgets import QLabel, QFrame, QLineEdit
from PyQt6.QtCore import pyqtSignal


class EditableLabel(QLabel):
    value_changed = pyqtSignal(str)

    def __init__(self, text=None):
        super().__init__(text)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.setStyleSheet("background-color: lightblue;")
        self.setToolTip("<html><head/><body><p>Кликните 2 раза для редактирования</p></body></html>")

    def mouseDoubleClickEvent(self, event):
        self.edit = QLineEdit(self.text())
        self.edit.editingFinished.connect(self.finish_editing)
        self.edit.focusOutEvent = self.focus_out_event
        print(self.parent().layout)
        self.parent().layout.replaceWidget(self, self.edit)
        self.edit.setFocus()

    def focus_out_event(self, event):
        self.finish_editing()

    def finish_editing(self):
        self.setText(self.edit.text())
        self.parent().layout.replaceWidget(self.edit, self)
        self.edit.deleteLater()
        self.value_changed.emit(self.edit.text())
