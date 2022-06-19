import json
import os.path

from werkzeug.datastructures import FileStorage
from werkzeug.local import LocalProxy

from path import Path


class Post:
    def __init__(self, picture: FileStorage, content: str):
        self.picture = picture
        self.content = content

    def get_picture_name(self) -> str:
        """

        :return: имя файла с загружаемым изображением
        """
        return self.picture.filename

    def check_file_extension(self) -> bool:
        """
            Проверка разрещения файла
        :return: True/False результат проверки
        """
        file_extension: str = self.picture.mimetype
        if file_extension in {'image/jpg', 'image/png'}:
            return True
        return False

    def check_missing_file(self) -> bool:
        if str(self.picture).split("'")[1] == '':
            return True
        return False

    def save_picture(self):
        """
            Функция для сохранения изображения на сервер
        :return: None
        """
        filename: str = self.picture.filename
        path = Path
        if not os.path.exists(path.UPLOADS_PATH):
            os.mkdir(f'{path.CURRENT_PATH}/uploads')
            os.mkdir(path.UPLOADS_PATH)
        self.picture.save(f"{path.UPLOADS_PATH}{filename}")

    def get_content(self) -> str:
        return self.content


class File:
    def __init__(self, file_path: str):
        if os.path.exists(file_path):
            self.file_path = file_path
        else:
            self.file_path = 'posts.json'

    def load_file(self) -> list[dict]:
        """

        :return: список с словарями (постами)
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def write_data_in_file(self, data: dict) -> None:
        """
            Функция для записи списка с словарями (постами) в фаил
        :param data: запись которую необходимо добавить
        :return: None
        """
        data_json: list[dict] = self.load_file()
        data_json.append(data)
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data_json, file, indent=2, ensure_ascii=False)

    def search_word_in_content(self, user_text: str) -> list[dict]:
        """

        :param user_text: искомое слово
        :return: список с постами в которых содержится искомое слово
        """
        list_by_search_text: list[dict] = []
        if user_text:
            for post in self.load_file():
                if user_text.lower() in post['content'].lower():
                    list_by_search_text.append(post)
        if list_by_search_text:
            return list_by_search_text


class Page:
    def __init__(self, request: LocalProxy):
        self.request = request

    def get_referrer(self, path: str):
        if self.request:
            return self.request
        return path
