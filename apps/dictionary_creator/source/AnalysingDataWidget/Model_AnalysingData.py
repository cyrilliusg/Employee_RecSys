import logging
import sqlite3
import pandas as pd


class AnalysingDataModel:
    def __init__(self):
        # Подключение к базе данных SQLite
        conn = sqlite3.connect('db//database.db')
        self.df = pd.read_sql_query('select * from work_data', conn)
        self.df = self.df.fillna('')
        conn.close()
        # Преобразование строки, представляющей список, обратно в список
        self.df['words'] = self.df['words'].apply(lambda x: x.split())
        self.current_index = self.get_last_index()
        self.length_of_current_sample = 0
        self.current_checked_value = 0
        self.max_index = len(self.df)

        self.logger = logging.getLogger(__name__)

    def add_to_reference(self, response):
        """
        Это общий публичный метод по записи действия пользователя. он будет управлять логикой модели
        :param response: действие пользователя
        :return: код действия в зависимости от текущего индекса проверки: скрыть лейбл или следующее слово
        """
        edit_response = False  # по умолчанию False
        # текст из лейбла проверяем на валидность и получаемый спличенный список слов
        words = self._validate_new_value(response['value'])
        if not words:
            self.logger.error(f'Произошла ошибка при обновлении значения {response['value']} на {words}')
            return False
        for word in words:  # Для каждого слова
            is_unique_response = self._uniqueness_check(word)  # проверяем уникальность
            if is_unique_response:  # если новое
                temp_response = self._insert_operation(word, response['code'])  # То вносим
            if is_unique_response and not edit_response:  # если уникальное и не было проверки статуса вносимости
                edit_response = edit_response + temp_response  # то делаем True
        # если хотя бы одно значение удачно внеслось и среди них нет изначального
        if edit_response and response['original_value'] not in words:
            # то изначальное значение было ошибочным и его скрываем чтобы более не появлялось
            self._insert_operation(response['original_value'], '2')
        # если был удачный внос данных
        if edit_response:
            self.current_checked_value += 1
            # если прошлись по всем строкам в должности
            if self.current_checked_value == self.length_of_current_sample:
                return '1'  # next_scenary
            else:
                return '0'  # hide_value
        else:
            return edit_response  # TODO: здесь нужно прописать нормальную логику получения ошибки

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
                self.logger.info(f"Проверка не пройдена")
                return False
            else:
                self.logger.info(f"Проверка пройдена")
                return True

    def _insert_operation(self, value, code):
        # TODO: здесь нужно нормально обернуть sql запрос
        try:
            conn = sqlite3.connect('db//database.db')  # Замените на путь к вашей базе данных
            cursor = conn.cursor()
            cursor.execute("INSERT INTO dictionary (value, source, work_data_id) VALUES (?, ?, ?)",
                           (value, code, self.current_index))
            conn.commit()
            cursor.close()
            self.logger.info(f"Внесено новое значение {value}")
            conn.close()
        except Exception as e:
            self.logger.error(f"Ошибка при внесении нового значения: {value}\n {e}")
        else:
            return True

    def _update_operation(self, response):
        # TODO: здесь нужно нормально обернуть sql запрос
        try:
            conn = sqlite3.connect('db//database.db')  # Замените на путь к вашей базе данных
            cursor = conn.cursor()
            cursor.execute("UPDATE dictionary SET value = ?, source = ? WHERE value = ?",
                           (response['value'], '4', response['original_value']))
            conn.commit()
            cursor.close()
            self.logger.info(f"Произведено обновление значения: {response['original_value']}, на: {response['value']} ")
            conn.close()
        except Exception as e:
            self.logger.error(
                f"Ошибка при обновлении значения: {response['original_value']} на: {response['value']}\n {e}")
            return False
        else:
            return True

    def get_new_words_in_row(self, row):
        # TODO: здесь нужно нормально обернуть sql запрос
        conn = sqlite3.connect('db//database.db')  # Замените на путь к вашей базе данных
        # self.logger.info(f"Запрос на проверку уникальных слов из списка")
        cursor = conn.cursor()
        result = [word for word in row if
                  not cursor.execute("SELECT 1 FROM dictionary WHERE value = ?", (word,)).fetchone()]
        cursor.close()
        conn.close()
        return result

    def find_next_index(self, current_index, max_index):
        """
        ищет первую не пустую строку от текущего переданного индекса строки
        :param current_index:
        :param max_index:
        :return:
        """
        while current_index != max_index:
            row = self.df.iloc[current_index]
            new_words = self.get_new_words_in_row(row['words'])
            if not new_words:
                current_index += 1
            else:
                break
        return current_index

    def next_job(self, index):
        row = self.df.iloc[index]
        new_words = set(self.get_new_words_in_row(row['words']))
        return [row, new_words]

    def get_last_index(self):
        # TODO: здесь нужно нормально обернуть sql запрос
        conn = sqlite3.connect('db//database.db')  # Замените на путь к вашей базе данных
        cursor = conn.cursor()
        result = cursor.execute("SELECT last_index FROM settings").fetchone()[0]
        cursor.close()
        conn.close()
        return result

    def set_new_index(self, index):
        # TODO: здесь нужно нормально обернуть sql запрос
        conn = sqlite3.connect('db//database.db')  # Замените на путь к вашей базе данных
        cursor = conn.cursor()
        cursor.execute("UPDATE settings SET last_index = ?", (index,))
        conn.commit()
        cursor.close()
        self.logger.info(f"Установлен новый крайний индекс: {index}")
        conn.close()

    def _validate_new_value(self, row):
        if not isinstance(row, str):
            return None
        if row == '':
            return None

        words = row.split()

        return [word for word in words if word != '']
