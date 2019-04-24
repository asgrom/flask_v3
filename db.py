import sqlite3

from flask import current_app, g
import click
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Очистить существующие данные и создать новые таблицы"""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Однако, поскольку вы используете фабричную функцию, этот экземпляр недоступен
     при написании функций. Вместо этого напишите функцию, которая принимает приложение
     и выполняет регистрацию.

     app.teardown_appcontext() говорит Flask вызвать эту функцию при очистке после
     возврата ответа.
     app.cli.add_command() добавляет новую команду, которую можно вызвать с помощью
     flask команды.
     """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
