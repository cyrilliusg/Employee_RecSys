import sys
from .GUI_AnalysingData import AnalysingDataGUI
from .Model_AnalysingData import AnalysingDataModel
from PyQt6.QtWidgets import QApplication
import logging
from ..Auxiliary.Worker import Worker


class AnalysingDataController:
    def __init__(self):
        self.view = AnalysingDataGUI()
        self.view.set_controller(self)

        self.model = AnalysingDataModel()

        self.worker = Worker()
        self.worker.info.connect(self.next_scenary_pt)

        self.next_scenary()

        self.view.show()
        self.logger = logging.getLogger(__name__)

    def handle_request(self, request):
        # user_codes = {0: 'Выбор значения',
        #               1: 'Далее',
        #               2: 'Отклонение значения',
        #               3: 'Закрытие окна (запись индекса)'}
        print(request)

        if request['code'] == 0 or request['code'] == 2:
            # Выводим лог
            if request['code'] == 0:
                self.logger.info(f"Пользователь решил добавить {request['value']} в список")
            else:
                self.logger.info(f"Пользователь решил скрыть {request['value']}")

            model_response = self.model.add_to_reference(request)
            if model_response == '1':
                self.next_scenary()
            else:
                self.hide_value(request['value'])
        if request['code'] == 1:
            self.logger.info("Пользователь кликнул Далее")
            # что значат эти две строчки кода?
            if len(self.view.widget_buttons.label_button_pairs) != 0:
                self.model.current_index += 1
            self.next_scenary()

        if request['code'] == 3:
            self.model.set_new_index(self.model.current_index)

    def next_scenary(self):
        # если не достигнут конец списка
        self.model.current_checked_value = 0
        self.worker._is_running = True
        self.worker.set_parameters(
            {'parent': '0', 'value': {'curr': self.model.current_index,
                                    'max': self.model.max_index}})
        self.worker.start()  # start the worker thread

    def next_job(self, index):
        row, new_words = self.model.next_job(index)
        self.model.length_of_current_sample = len(new_words)
        self.view.set_new_row(row['department'], row['unit'], row['job_name'], new_words)
        self.view.set_label(index, self.model.max_index)

    def hide_value(self, value):
        self.view.hide_value(value)

    def show(self):
        self.view.show()

    def next_scenary_pt(self, new_actual_index):
        if new_actual_index != self.model.max_index:
            self.next_job(new_actual_index)
            self.model.current_index = new_actual_index
        else:
            # если следующего индекса нет, то конец
            self.view.end_scenary()


# Запуск приложения
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    app = QApplication(sys.argv)
    controller = AnalysingDataController()
    sys.exit(app.exec())
