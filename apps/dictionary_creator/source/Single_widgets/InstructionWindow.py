from PyQt6.QtWidgets import QApplication, QTextBrowser


class InstructionWindow(QTextBrowser):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        self.setHtml("""
            <h1>Инструкция</h1>
            <p>Место для инструкции</p>
        """)


"""
            <p>Это пример инструкции для моего приложения.</p>
            <ul>
                <li>Шаг 1: Сделайте это</li>
                <li>Шаг 2: Сделайте то</li>
            </ul>
            <p><a href="http://example.com">Больше информации</a></p>
"""

if __name__ == '__main__':
    app = QApplication([])
    main_window = InstructionWindow()
    main_window.show()
    app.exec_()
