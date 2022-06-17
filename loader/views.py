from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.datastructures import FileStorage
from json.decoder import JSONDecodeError

from classes import Post, File

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
                abort(413)
            session['picture'] = picture_path
            session['content'] = content

            return redirect(url_for('.post_uploaded'))
        else:
            flash('Не верный формат файла изображения. Используйте JPG, PNG', 'warning')
            return redirect(url_for('.add_post'))
    return render_template('post_form.html')


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
    return render_template('post_uploaded.html', picture=picture, text=text)


@loader_blueprint.errorhandler(413)
def file_not_found(e):
    """
        Обработка ошибки
    :param e: класс ошибки от которого наследуемся
    :return:
    """
    return "<h1>Упс что то не так с файлом постов</h1><p>Обратитесь в поддержку</p>", 413
