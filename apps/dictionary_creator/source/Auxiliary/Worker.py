from PyQt6.QtCore import QThread, pyqtSignal
from ..FileSelectorWidget.Model_FileSelector import FileSelectorModel
from ..AnalysingDataWidget.Model_AnalysingData import AnalysingDataModel
from ..Auxiliary.IO import IO_operations
from ..MainWindowWidget.Model_MainWindow import DictionaryModel


class Worker(QThread):
    info = pyqtSignal(int)
    result = pyqtSignal(list)
    column = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.model = None
        self.parent = None  # 0 - окно обработки данных, 1 - окно обработки эксель файла, 2 - виджет выбора колонки
        self.params = None
        self._is_running = True

    def stop(self):
        self._is_running = False

    def run(self):
        while self._is_running:
            if self.parent == '0':  # 0 - окно обработки данных
                self.model = AnalysingDataModel()
                new_index = self.model.find_next_index(self.params['curr'], self.params['max'])
                self.info.emit(new_index)
            elif self.parent == '1':  # 1 - окно обработки эксель файла
                self.model = FileSelectorModel()
                result = self.model.main_process(self.params)
                self.result.emit(result)
            elif self.parent == '2':  # 2 - виджет выбора колонки
                self.model = IO_operations()
                self.column.emit(self.model.get_matching_header_letters(self.params))
            elif self.parent == '3':  # 2 - виджет выбора колонки
                self.model = DictionaryModel()
                print('тут')
                self.result.emit(self.model.download_file(self.params))
            self.stop()
            return

    def set_parameters(self, request):
        self.parent = request['parent']
        self.params = request['value']
