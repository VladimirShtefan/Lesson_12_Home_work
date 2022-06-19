from json.decoder import JSONDecodeError

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.datastructures import FileStorage
from loguru import logger

from classes import Post, File, Page

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')


# Создаем вьюшку, для блюпринта
@loader_blueprint.route("/post/", methods=['GET', 'POST'])
def add_post():
    """
        Обработка запросов на странцу с постами
    :return:
    """
    if request.method == 'POST':
        picture: FileStorage = request.files.get('picture')
        text: str = request.form.get('content')
        post = Post(picture, text)
        if post.check_missing_file():
            abort(400)
        if post.check_file_extension():
            post.save_picture()

            picture_name = post.get_picture_name()
            picture_path = f"/uploads/images/{picture_name}"
            content = post.get_content()

            file = File('posts.json')
            try:
                file.write_data_in_file({"pic": picture_path,
                                         "content": content})
            except (FileNotFoundError, JSONDecodeError):
                logger.error("Ошибка загрузки файла")
                abort(413)
            session['picture'] = picture_path
            session['content'] = content

            return redirect(url_for('loader_blueprint.post_uploaded'))
        else:
            flash('Не верный формат файла изображения. Используйте JPG, PNG', 'warning')
            logger.info("Не верный формат изображения")
            return redirect(url_for('loader_blueprint.add_post'))
    back = Page(request.referrer).get_referrer(url_for('main_blueprint.page_index'))
    return render_template('post_form.html', back=back)


@loader_blueprint.route("/uploaded/", methods=['GET'])
def post_uploaded():
    """
        Страница созданного поста
    :return:
    """
    picture = session['picture']
    text = session['content']
    session.pop('picture', None)
    session.pop('content', None)
    back = Page(request.referrer).get_referrer(url_for('loader_blueprint.add_post'))
    return render_template('post_uploaded.html', picture=picture, text=text, back=back)


@loader_blueprint.errorhandler(413)
def file_not_found(e):
    """
        Обработка ошибки
    :param e: класс ошибки от которого наследуемся
    :return:
    """
    return "<h1>Упс что то не так с файлом постов</h1><p>Обратитесь в поддержку</p>", 413


@loader_blueprint.errorhandler(400)
def file_not_found(e):
    """
        Обработка ошибки
    :param e: класс ошибки от которого наследуемся
    :return:
    """
    return "<h1>Не выбрано изображение для загрузки поста</h1>", 400
