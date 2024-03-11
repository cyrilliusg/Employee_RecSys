import pandas as pd
import re
import nltk
from nltk.stem.snowball import SnowballStemmer


class DataProcessor:
    def __init__(self):
        self.stemmer = None

    def _clean_text(self, text):
        if pd.isnull(text):
            return ""  # Если текст отсутствует (NaN), возвращаем пустую строку
        if isinstance(text, int):
            return ""
        if text.isdigit():
            return ""
        text = text.lower()  # Приведение всех символов к нижнему регистру
        text = text.strip()  # Удаление пробельных символов с начала и конца строки

        # Замена всех последовательностей небуквенно-цифровых символов на один пробел
        text = re.sub(r'[^\w\s]+', ' ', text)

        # Удаление лишних пробелов, оставляя только один пробел между словами
        text = ' '.join(text.split())
        return text

    def _unique_words(self, row):
        unique_words = []
        seen = set()
        for col in row.index:
            words = str(row[col]).split()
            for word in words:
                if word not in seen:
                    seen.add(word)
                    unique_words.append(word)
        return ' '.join(unique_words)

    def _stem_sentence(self, sentence):
        words = nltk.word_tokenize(sentence, language="russian")
        stemmed_words = [self.stemmer.stem(word) for word in words]
        return ' '.join(stemmed_words)

    def clean_df(self, df):
        """
        форматирует сырые данные для обучения
        :param df: (Dataframe) df сырых данных
        :param extension:(str) расширение файла
        :return: абсолютный путь к файлу с очищенными данными
        """

        for col in df.columns:  # ['department', 'unit', 'job_name']
            df[col] = df[col].apply(self._clean_text)

        df = df.drop_duplicates()  # subset=['department', 'unit', 'job_name']

        return df

    def concatenate_df(self, df, col_name):
        """
        создаёт новую колонку combined на основании уникальных слов из всех текущих колонок
        """
        # Применяем функцию к каждой строке DataFrame
        df[col_name] = df.apply(self._unique_words, axis=1)  # [['department', 'unit', 'job_name']]
        return df

    def stem_df(self, df, col_name):
        """
        Обрабатывает колонку combined в df и создает новую stemmed
        :param df:
        :return:
        """
        self.stemmer = SnowballStemmer("russian")
        # Применяем функцию к каждой строке в колонке 'combined'
        df['stemmed'] = df[col_name].apply(self._stem_sentence)
        df = df.rename(columns={col_name: 'before_stemmed', 'stemmed': col_name})

        return df

    def get_unique_sequence(self, df, column_name):
        unique_sequence = []
        seen = set()
        for row in df[column_name]:
            words = row.split()
            for word in words:
                if word not in seen:
                    seen.add(word)
                    unique_sequence.append(word)
        return unique_sequence

    def unique_words_in_row(self, row):
        unique_words = []
        seen = set()
        for word in row.split():
            if word not in seen:
                seen.add(word)
                unique_words.append(word)
        return ' '.join(unique_words)

        return df
