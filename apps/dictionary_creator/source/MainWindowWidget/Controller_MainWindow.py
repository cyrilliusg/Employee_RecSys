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
from ..DictionaryViewWidget.GUI_DictionaryView import DictionaryView_GUI
from ..Single_widgets.DialogWidget import DialogWidget
import os


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
        self.dictionary_view_widget = None

        self.view.set_dict_len_label(self.model.dict_len())
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
            self.create_scenario()

        if request['code'] == 1:
            self.model.current_process = '1'
            self.edit_scenario()

        if request['code'] == 2:
            self.dictionary_view_widget = DictionaryView_GUI('db//database.db')
            self.dictionary_view_widget.show()

        if request['code'] == 3:
            self.delete_scenario()

        if request['code'] == 4:
            self.download_scenario()

        if request['code'] == 5:
            self.file_selector_widget = FileSelectorWidgetController()

        if request['code'] == 6:
            self.manual_window = InstructionWindow()
            self.manual_window.show()

        if request['code'] == 7:
            self.about()

        if request['code'] == 8:
            try:
                os.startfile(request['value'])
                self.msgBox.close()
            except Exception as e:
                QMessageBox.warning(None, "Ошибка",
                                    f"Не удалось открыть файл.\nПуть к файлу: {request['value']}\n\n{e}")

    def download_scenario(self):
        if self.model.emptiness_check() == 0:
            QMessageBox.information(None, 'Статус', 'Пустой словарь. Загрузите данные')
            return
        # Открываем диалоговое окно для сохранения файла
        fileName, _ = QFileDialog.getSaveFileName(None, "Сохранить файл", "",
                                                  "Excel Files (*.xlsx)")
        if fileName:
            # Если пользователь не указал расширение файла, добавляем его
            if not fileName.endswith('.xlsx'):
                fileName += '.xlsx'

            self.model.fileName = fileName
            self.worker.set_parameters({'parent': '3', 'value': fileName})
            self.worker.result.connect(self.control_dialog)
            self.worker._is_running = True
            self.worker.start()  # Запуск рабочего потока

    def control_dialog(self, result):
        if result[0] == '1':
            QMessageBox.critical(None, "Ошибка", result[1])
            return
        else:
            # Здесь вы можете добавить логику для сохранения файла по выбранному пути
            self.msgBox = DialogWidget()
            self.msgBox.set_parent('8')
            self.msgBox.set_controller(self)
            self.msgBox.set_path(self.model.fileName)
            self.msgBox.exec()

    def edit_scenario(self):
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

    def delete_scenario(self):
        if self.model.emptiness_check() == 0:
            QMessageBox.information(None, 'Статус', 'Пустой словарь.')
            return
        result = QMessageBox.question(None, "Вопрос", "Вы уверены, что хотите удалить словарь?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if result == QMessageBox.StandardButton.Yes:
            self.model.clean_db()  # Производим удаление
            self.view.set_dict_len_label(self.model.dict_len())  # Обновляем интерфейс
            QMessageBox.information(None, 'Статус', 'Успешно!')

    def create_scenario(self):
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
                self.create_scenario()
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
                self.view.set_dict_len_label(self.model.dict_len())
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
                    self.view.set_dict_len_label(self.model.dict_len())
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
