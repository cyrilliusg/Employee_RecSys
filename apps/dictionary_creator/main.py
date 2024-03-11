from source.MainWindowWidget.Controller_MainWindow import MainWindowController
from PyQt6.QtWidgets import QApplication
import sys
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    app = QApplication(sys.argv)
    controller = MainWindowController()
    sys.exit(app.exec())
