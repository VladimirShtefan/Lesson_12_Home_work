from json.decoder import JSONDecodeError

from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, abort
from loguru import logger

from classes import File

# создаем новый блюпринт
main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')


# Создаем вьюшку, для блюпринта
@main_blueprint.route("/", methods=['GET'])
@main_blueprint.route("/index/", methods=['GET'])
def page_index():
    """
        Стартовая страница
    :return:
    """
    return render_template('index.html')


@main_blueprint.route("/search", methods=['GET'])
def search_text():
    """
        Обработка запроса поиска слова
    :return:
    """
    s: str = request.args.get('s')
    file = File('posts.json')
    try:
        posts: list[dict] = file.search_word_in_content(s)
    except (FileNotFoundError, JSONDecodeError):
        logger.error("Ошибка загрузки файла")
        abort(413)
    if posts is not None:
        return render_template('post_list.html', posts=posts, user_text=s)
    flash('По вашему запросу ничего не найдено, введите другой запрос', 'warning')
    logger.info("Запрос в базе не найден")
    return redirect(url_for('.page_index'))


@main_blueprint.route("/uploads/<path:path>", methods=['GET'])
def static_dir(path):
    """
        Указываем область для обращения к файлам
    :param path: путь
    :return:
    """
    return send_from_directory("uploads", path)


@main_blueprint.errorhandler(413)
def file_not_found(e):
    """
        Обработка ошибки
    :param e: класс ошибки от которого наследуемся
    :return:
    """
    return "<h1>Упс что то не так с файлом постов</h1><p>Обратитесь в поддержку</p>", 413
