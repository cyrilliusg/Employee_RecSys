import sys
from .GUI_FileSelector import FileSelectorGUI
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
import logging
from ..Auxiliary.Worker import Worker
import os
from ..Single_widgets.DialogWidget import DialogWidget


class FileSelectorWidgetController:
    def __init__(self):
        self.view = FileSelectorGUI()
        self.view.set_controller(self)

        self.worker = Worker()
        self.worker.result.connect(self.control_dialog)

        self.view.show()
        self.logger = logging.getLogger(__name__)

    def handle_request(self, request):
        # user_codes = {0: 'Открыть проводник',
        #               1: 'Старт процессинга'}
        print(request)

        if request['code'] == 0:
            self.logger.info("Пользователь кликнул 'открыть проводник'")
            fileName, _ = QFileDialog.getOpenFileName(None, "Выберите файл", "",
                                                      "Excel Files (*.xlsx);;CSV Files (*.csv)")
            if fileName:
                self.view.set_lineedit(fileName)
                return

        if request['code'] == 1:
            params = self.view.get_params()
            self.logger.info(f"Пользователь кликнул Старт. Параметры: {params}")
            # params = {0: 'Путь к файлу',
            #               1: 'Стемминг',
            #               2: 'Стандартная очистка',
            #               3 : 'Конкатенация'}

            self.worker._is_running = True
            self.worker.set_parameters({'parent': '1', 'value': params})
            self.worker.start()  # start the worker thread

        if request['code'] == 2:
            try:
                os.startfile(request['value'])
                self.msgBox.close()
            except Exception as e:
                QMessageBox.warning(None, "Ошибка",
                                    f"Не удалось открыть файл.\nПуть к файлу: {request['value']}\n\n{e}")

    def open_dialog(self, path):
        self.msgBox = DialogWidget()
        self.msgBox.set_controller(self)
        self.msgBox.set_path(path)
        self.msgBox.exec()

    def control_dialog(self, result):
        if result[0] == '1':
            QMessageBox.critical(None, "Ошибка", result[1])
            return
        else:
            self.open_dialog(result[1])


# Запуск приложения
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    app = QApplication(sys.argv)
    controller = FileSelectorWidgetController()
    sys.exit(app.exec())
