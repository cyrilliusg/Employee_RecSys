from ..MainWindowWidget.GUI_MainWindow import MainWidget_GUI
from ..MainWindowWidget.Model_MainWindow import DictionaryModel
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QDialog
import logging
from ..Auxiliary.Worker import Worker
from ..FileSelectorWidget.Controller_FileSelector import FileSelectorWidgetController
from ..Single_widgets.DataQuestionWidget import DataQuestionWidget
from ..AnalysingDataWidget.Controller_AnalysingData import AnalysingDataController
from ..Single_widgets.InstructionWindow import InstructionWindow
from ..Single_widgets.ChoiceColumnDialog import ChoiceColumnDialog


class MainWindowController:
    def __init__(self):
        self.view = MainWidget_GUI()
        self.view.set_controller(self)
        self.model = DictionaryModel()
        self.worker = Worker()
        self.worker.column.connect(self.set_columns)

        self.file_selector_widget = None
        self.analysing_data_widget = None
        self.dialog_question_file = None
        self.dialog_choise_column = None

        self.view.set_dict_len_label(self.model.emptiness_check())
        self.view.show()
        self.logger = logging.getLogger(__name__)

        self.question_clear = 'В памяти уже имеются данные. При создании нового словаря старые данные сотрутся. Вы уверены?'
        self.question_data = 'У вас уже есть обработанные данные?'

    def handle_request(self, request):
        # 0 - создать словарь
        # 1 - отредактировать словарь
        # 2 - читать словарь
        # 3 - удалить словарь
        # 4 - скачать словарь
        # 5 - открыть обработчик данных
        # 6 - открыть инструкцию
        # 7 - открыть о программе

        print(request)

        if request['code'] == 0:
            self.logger.info("Пользователь кликнул 'создать'")
            self.model.current_process = '0'
            self.create_scenary()

        if request['code'] == 1:
            self.model.current_process = '1'
            self.edit_scenary()

        if request['code'] == 2:
            QMessageBox.information(None, 'Статус', 'Просмотр словаря в разработке.')
            return

        if request['code'] == 3:
            self.delete_scenary()

        if request['code'] == 5:
            self.file_selector_widget = FileSelectorWidgetController()

        if request['code'] == 6:
            self.manual_window = InstructionWindow()
            self.manual_window.show()

        if request['code'] == 7:
            self.about()

    def edit_scenary(self):
        if self.model.emptiness_check() == 0:
            QMessageBox.information(None, 'Статус', 'Пустой словарь. Загрузите данные')
            self.model.current_process = None
            return

        if self.model.emptiness_check_work_data() == 0:
            result = QMessageBox.information(None, "Уведомление", "Не обнаружено данных для наполнения. Выберите файл.",
                                             QMessageBox.StandardButton.Yes)
            if result == QMessageBox.StandardButton.Yes:
                fileName, _ = QFileDialog.getOpenFileName(None, "Выберите файл", "",
                                                          "Excel Files (*.xlsx);;CSV Files (*.csv)")
                if fileName:
                    self.model.fileName = fileName
                    self.worker.set_parameters({'parent': '2', 'value': fileName})
                    self.worker._is_running = True
                    self.worker.start()  # Запуск рабочего потока
                else:
                    self.model.current_process = None
            else:
                self.model.current_process = None
            return

        self.analysing_data_widget = AnalysingDataController()

    def delete_scenary(self):
        if self.model.emptiness_check() == 0:
            QMessageBox.information(None, 'Статус', 'Пустой словарь.')
            return
        result = QMessageBox.question(None, "Вопрос", "Вы уверены, что хотите удалить словарь?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if result == QMessageBox.StandardButton.Yes:
            self.model.clean_db()  # Производим удаление
            self.view.set_dict_len_label(self.model.emptiness_check())  # Обновляем интерфейс
            QMessageBox.information(None, 'Статус', 'Успешно!')

    def create_scenary(self):
        self.dialog_question_file = DataQuestionWidget()
        self.dialog_question_file.user_choice_signal.connect(self.dialog_question_file_control)
        if self.model.emptiness_check() != 0 and not self.model.delete_later:
            self.dialog_question_file.set_text(self.question_clear)
        else:
            self.dialog_question_file.set_text(self.question_data)

        self.dialog_question_file.show()

    def dialog_question_file_control(self, response):
        # блок для сценария когда очистка
        if response['question'] == self.question_clear:
            if response['value']:
                self.model.delete_later = True
                self.create_scenary()
                return
            else:
                self.model.current_process = None
                self.dialog_question_file.close()
                return

        # основной блок: файл имеется - true or false
        if not response['value']:
            self.model.current_process = None
            self.model.delete_later = False
            self.dialog_question_file.close()
            self.file_selector_widget = FileSelectorWidgetController()  # значит файл есть и открыть проводник
            return
        else:
            fileName, _ = QFileDialog.getOpenFileName(None, "Выберите файл", "",
                                                      "Excel Files (*.xlsx);;CSV Files (*.csv)")
            if fileName != '':
                self.model.clean_db()
                self.view.set_dict_len_label(self.model.emptiness_check())
                self.model.fileName = fileName
                self.worker.set_parameters({'parent': '2', 'value': fileName})
                self.worker._is_running = True
                self.worker.start()  # start the worker thread
            else:
                self.model.current_process = None
                self.model.delete_later = False
                self.dialog_question_file.close()

    def set_columns(self, columns):
        self.dialog_choise_column = ChoiceColumnDialog()
        self.dialog_choise_column.set_values(columns)
        self.dialog_choise_column.show()
        if self.dialog_choise_column.exec() == QDialog.DialogCode.Accepted:
            colName = self.dialog_choise_column.get_value()

            # если процесс создания 0
            if self.model.current_process == '0':
                result = self.model.create({'0': self.model.fileName, '1': colName})
                if result[0] == '0':
                    QMessageBox.information(None, "Уведомление", "Словарь создан!")
                    self.view.set_dict_len_label(self.model.emptiness_check())
                else:
                    QMessageBox.warning(None, "Уведомление", f"Произошла ошибка!\n{result[1]}")
            # если процесс редактирования 1
            elif self.model.current_process == '1':
                result = self.model.add_work_data({'0': self.model.fileName, '1': colName})
                if result[0] == '0':
                    QMessageBox.information(None, "Уведомление", "Данные добавлены!")
                    self.analysing_data_widget = AnalysingDataController()
                else:
                    QMessageBox.warning(None, "Уведомление", f"Произошла ошибка!\n{result[1]}")
        self.model.current_process = None
        self.model.delete_later = False
        self.dialog_choise_column.close()
        return

    def about(self):
        QMessageBox.about(None, "О программе",
                          "ReTeam Platform<br>"
                          "Версия: 1.0.0<br>"
                          "Автор: RosExpert<br>"
                          "<a href='https://rosexpert.ru'>Официальный сайт</a>")
