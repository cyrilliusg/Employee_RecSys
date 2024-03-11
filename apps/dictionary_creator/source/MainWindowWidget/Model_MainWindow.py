import logging
import pandas as pd
from ..Auxiliary.Dataprocessor import DataProcessor
from ..Auxiliary.IO import IO_operations
import sqlite3


class DictionaryModel:
    def __init__(self):
        self.fileName = None
        self.delete_later = False
        self.io = IO_operations()
        self.processor = None
        self.current_process = None

        self.logger = logging.getLogger(__name__)

    def insert_new_work_data(self, df):
        try:
            conn = sqlite3.connect('db//database.db')  # Замените на путь к вашей базе данных
            df.to_sql('work_data', conn, if_exists='replace', index=False)
            self.logger.info(f"Workdata наполнен новыми словами")
            conn.close()
        except Exception as e:
            return ['1', str(e)]
        else:
            return ['0', None]

    def add_work_data(self, params):
        path = params['0']
        colName = params['1']
        result = self.io._process_path(path)
        if result[0] == '1':
            return result
        self.logger.info(f'Этап проверки пути пройден: {result}')
        result = self.io._read_file(*result[1])
        if result[0] == '1':
            return result
        self.logger.info(f'Этап чтения файла пройден: {result}')

        result = self.io._validate_df(df=result[1])
        if result[0] == '1':
            return result
        self.logger.info(f'Этап проверки файла пройден: {result}')

        df = result[1]
        missing_words = self.find_missing_words(df, colName)

        df = df[df[colName].apply(lambda x: any(word in missing_words for word in x.split(' ')))]
        df = df.reset_index(drop=True)

        df = df.rename(columns={colName: 'words'})

        df = df[['department', 'unit', 'job_name', 'words']]

        df.insert(0, 'id', range(len(df)))

        response = self.insert_new_work_data(df)

        return response

    def create(self, params):
        result = self.io._process_path(path=params['0'])
        if result[0] == '1':
            return result
        self.logger.info(f'Этап проверки пути пройден: {result}')
        result = self.io._read_file(*result[1])
        if result[0] == '1':
            return result
        self.logger.info(f'Этап чтения файла пройден: {result}')

        result = self.io._validate_df(df=result[1])
        if result[0] == '1':
            return result
        self.logger.info(f'Этап проверки файла пройден: {result}')

        self.processor = DataProcessor()

        unique_words_sequence = self.processor.get_unique_sequence(df=result[1], column_name=params['1'])

        return self.insert_new_dictionary(unique_words_sequence)

    def insert_new_dictionary(self, unique_words_sequence):
        try:
            conn = sqlite3.connect('db//database.db')  # Замените на путь к вашей базе данных
            cursor = conn.cursor()
            for val in unique_words_sequence:
                cursor.execute('INSERT INTO dictionary(value, source) VALUES(?, ?)', (val, '1'))
            conn.commit()
            cursor.close()
            self.logger.info(f"Словарь dictionary наполнен новыми словами")
            conn.close()
        except Exception as e:
            return ['1', str(e)]
        else:
            return ['0', None]

    def clean_db(self):
        # TODO: здесь нужно нормально обернуть sql запрос
        conn = sqlite3.connect('db//database.db')  # Замените на путь к вашей базе данных
        cursor = conn.cursor()
        cursor.execute("DELETE FROM dictionary")
        cursor.execute("DELETE FROM work_data")
        conn.commit()
        cursor.execute("VACUUM")
        conn.commit()
        cursor.execute("UPDATE settings set last_index = 0")
        cursor.close()
        self.logger.info(f"Словарь dictionary очищен")
        conn.close()

    def emptiness_check(self):
        # TODO: здесь нужно нормально обернуть sql запрос
        try:
            conn = sqlite3.connect('db//database.db')  # Замените на путь к вашей базе данных
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(source) FROM dictionary WHERE source = 1")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            self.logger.info(f"Проверка на наличие значений")
        except Exception as e:
            self.logger.error(f"Ошибка при запросе на наличие значений словаря")
        else:
            if result:
                return result[0]

    def emptiness_check_work_data(self):
        # TODO: здесь нужно нормально обернуть sql запрос
        try:
            conn = sqlite3.connect('db//database.db')  # Замените на путь к вашей базе данных
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(words) FROM work_data")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            self.logger.info(f"Проверка на наличие значений в work_data")
        except Exception as e:
            self.logger.error(f"Ошибка при запросе на наличие значений в work_data")
        else:
            if result:
                return result[0]

    def _uniqueness_check(self, value):
        # TODO: здесь нужно нормально обернуть sql запрос
        try:
            conn = sqlite3.connect('db//database.db')  # Замените на путь к вашей базе данных
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM dictionary WHERE value = ?", (value,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            self.logger.info(f"Проверка значения на уникальность: {value}")
        except Exception as e:
            self.logger.error(f"Ошибка при проверке значения на уникальность: {value}\n {e}")
        else:
            if result:
                return False
            else:
                return True

    def find_missing_words(self, df, colname):
        unique_words = set()
        # Или замена пропущенных значений пустыми строками
        df[colname].str.split(' ').apply(unique_words.update)

        # Шаг 2: Чтение слов из SQLite и создание сета существующих слов
        conn = sqlite3.connect('db//database.db')  # Подключение к вашей базе данных
        existing_words_set = set(pd.read_sql_query("SELECT value FROM dictionary", conn)['value'])

        # Шаг 3: Находим слова, которых нет в таблице dictionary
        missing_words = unique_words - existing_words_set

        return missing_words

    def download_file(self, path):
        print('тут')
        # TODO: здесь нужно нормально обернуть sql запрос
        try:
            conn = sqlite3.connect('db//database.db')  # Замените на путь к вашей базе данных
            pd.read_sql_query('SELECT * FROM dictionary', conn).to_excel(path, index=False)
            conn.close()
            self.logger.info(f"Скачиваем словарь")
        except Exception as e:
            self.logger.error(f"Ошибка при скачивании словаря\n {e}")
            return ['1', str(e)]
        else:
            return ['0', None]

    def dict_len(self):
        # TODO: здесь нужно нормально обернуть sql запрос
        try:
            conn = sqlite3.connect('db//database.db')  # Замените на путь к вашей базе данных
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(source) FROM dictionary")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            self.logger.info(f"Проверка на наличие значений")
        except Exception as e:
            self.logger.error(f"Ошибка при запросе на наличие значений словаря")
        else:
            if result:
                return result[0]
