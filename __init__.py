import os

from flask import Flask


def create_app(test_config=None):
    """Создание и конфигурирование приложения"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        # DEBUG=True
    )

    if test_config is None:
        # Загрузка файла конфигурации если он существует
        # app.config.from_json('config.json', silent=True)
        app.config.from_pyfile('flaskr.py', silent=True)
        # app.config.from_envvar('FLASKR_CONFIG', silent=True)
        print(app.config)
    else:
        app.config.from_mapping(test_config)

    # убедиться что папка экземпляра существует
    try:
        os.makedirs(app.instance_path)
        print('mkdir')
    except OSError as e:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
