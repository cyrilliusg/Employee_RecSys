import logging
import pandas as pd
import os
from .Dataprocessor import DataProcessor
import re
import openpyxl


class IO_operations:
    def __init__(self):
        self.file_extension = None
        self.file_name = None
        self.df = None
        self.processor = None
        self.params = None
        self.new_file_name = None
        self.o_col = None
        self.usecols = None
        self.logger = logging.getLogger(__name__)

    def main_process(self, params):
        result = self._analyse_params(params)
        if result[0] == '1':
            return result
        self.logger.info(f'Этап проверки параметров пройден: {result}')
        result = self._read_file()
        if result[0] == '1':
            return result
        self.logger.info(f'Этап чтения файла пройден: {result}')
        result = self._validate_df()
        if result[0] == '1':
            return result
        self.logger.info(f'Этап проверки файла пройден: {result}')

        self.processor = DataProcessor()

        if params['2']:
            self.df = self.processor.clean_df(self.df)
            self.logger.info(f'Этап очистки df пройден')

        if params['3']:
            self.df = self.processor.concatenate_df(self.df, self.o_col)
            self.logger.info(f'Этап конкатенации df пройден')

        if params['1']:
            self.df = self.processor.stem_df(self.df, self.o_col)
            self.logger.info(f'Этап стэмминга df пройден')

        return self._save_file()

    def _save_file(self):
        self.new_file_name = self.file_name + '_processed'
        path = self._create_filename(self.new_file_name + '.xlsx')

        try:
            self.df.to_excel(path, index=False)
        except Exception as e:
            return ['1', str(e)]
        self.logger.info(f'Файл сохранён')
        return ['0', path]

    def _create_filename(self, base_path):
        counter = 1
        path = base_path
        while os.path.exists(path):
            path = f"{counter}_{base_path}"
            counter += 1
        return path

    def _analyse_params(self, params):
        # params = {0: {'path': путь к файлу,
        #                   'o_col': 'Имя результирующей колонки',
        #                   'i_col_range': 'Диапазон колонок для считывания'},
        #               1: 'Стемминг',
        #               2: 'Стандартная очистка',
        #               3 : 'Конкатенация'}
        result = self._process_file_options(params['0'])
        self.logger.info(f'Этап проверки пути пройден: {result}')

        if result[0] == '1':
            return result
        if not params['3'] and params['1']:
            return ['1', 'Для Стемминга необходимо выбрать Конкатенацию']

        return ['0', None]

    def _validate_df(self, df):
        df.dropna(axis=0, how='all', inplace=True)

        if df.shape[1] == 0:
            return ['1', 'Нет колонок']
        if df.shape[0] == 0:
            return ['1', 'Нет строк']

        return ['0', df]

    def _read_file(self, file_name, file_extension, usecols=None):
        full_path = file_name + file_extension
        if file_extension == '.csv':
            try:
                df = pd.read_csv(full_path, usecols=usecols)
            except Exception as e:
                return ['1', str(e)]
        else:
            try:
                df = pd.read_excel(full_path, usecols=usecols)
            except Exception as e:
                return ['1', str(e)]

        return ['0', df]

    def _process_file_options(self, options):
        result = self._process_path(options['path'])
        if result[0] == '1':
            return result
        self.o_col = 'combined' if options['o_col'] is None else options['o_col']
        result = self._validate_usecols(options['i_col_range'])
        # можно ещё раз не проверять а просто вернуть
        return result

    def _validate_usecols(self, s):
        if s is not None:
            # Проверка на допустимые символы: только буквы A-Z, запятые и двоеточия, пробелы разрешены только после запятых
            if not re.match(r'^[A-Z](?:\:[A-Z])?(?:,\s?[A-Z](?:\:[A-Z])?)*$', s):
                return ['1', f'В строке {s} неверные символы']

            # Разбиваем строку по запятым с учетом пробелов после запятых
            parts = [part.strip() for part in s.split(',')]

            for part in parts:
                # Если есть диапазон, проверяем его корректность
                if ':' in part:
                    start, end = part.split(':')
                    if ord(start) > ord(end):  # Сравнение по ASCII кодам для букв
                        return ['1', f'Диапазон {part} некорректен']
                # Если нет диапазона, проверяем, что это одиночная буква
                elif not re.match(r'^[A-Z]$', part):
                    return ['1', f'БУква {part} невалидна']
            try:
                s = self._range2cols(s)
            except Exception as e:
                return [1, str(e)]

        return ['0', s]

    def _process_path(self, path):
        if not os.path.isfile(path):
            return ['1', 'Не указан путь']
        file_name, file_extension = os.path.splitext(path)
        if file_extension not in ['.xlsx', '.csv']:
            return ['1', 'Неверное расширение файла']
        if not os.path.exists(path):
            return ['1', 'Неверный путь']

        return ['0', [file_name, file_extension]]

    def _range2cols(self, areas: str) -> list[int]:
        """
        Convert comma separated list of column names and ranges to indices.

        Parameters
        ----------
        areas : str
            A string containing a sequence of column ranges (or areas).

        Returns
        -------
        cols : list
            A list of 0-based column indices.

        Examples
        --------
        >>> self._range2cols('A:E')
        [0, 1, 2, 3, 4]
        >>> self._range2cols('A,C,Z:AB')
        [0, 2, 25, 26, 27]
        """
        cols: list[int] = []

        for rng in areas.split(","):
            if ":" in rng:
                rngs = rng.split(":")
                cols.extend(range(self._excel2num(rngs[0]), self._excel2num(rngs[1]) + 1))
            else:
                cols.append(self._excel2num(rng))

        return cols

    def _excel2num(self, x: str) -> int:
        """
        Convert Excel column name like 'AB' to 0-based column index.

        Parameters
        ----------
        x : str
            The Excel column name to convert to a 0-based column index.

        Returns
        -------
        num : int
            The column index corresponding to the name.

        Raises
        ------
        ValueError
            Part of the Excel column name was invalid.
        """
        index = 0

        for c in x.upper().strip():
            cp = ord(c)

            if cp < ord("A") or cp > ord("Z"):
                raise ValueError(f"Invalid column name: {x}")

            index = index * 26 + cp - ord("A") + 1

        return index - 1

    def get_matching_header_letters(self, path, sheet_name=None, column_list=None):
        # Открываем файл в режиме "только для чтения"
        workbook = openpyxl.load_workbook(path, read_only=True)

        if sheet_name is None:
            # Получаем первый лист
            sheet = workbook.active
        else:
            sheet = workbook[sheet_name]

        # Читаем первую строку (заголовки)
        headers = []
        for cell in next(sheet.iter_rows()):
            if cell.value is not None:  # Проверка, что ячейка не пустая
                headers.append((cell.value, cell.column_letter))
        # Закрываем файл
        workbook.close()
        if column_list is not None:
            # Находим совпадающие заголовки и их буквенные обозначения
            return [header[1] for header in headers if header[0] in column_list]
        else:
            return [header[0] for header in headers]
