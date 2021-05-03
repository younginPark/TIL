import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import psycopg2
import psycopg2.extras

def get_db():
    if 'db' not in g:
        global conn
        conn_string = "host='localhost' dbname ='flaskr' user='postgres' password='admin1234'"
        #conn = psycopg2.connect(conn_string)
        conn = psycopg2.connect(conn_string, cursor_factory=psycopg2.extras.DictCursor)
        g.db = conn.cursor()
        # g.db = sqlite3.connect(
        #     current_app.config['DATABASE'],
        #     detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.row_factory = sqlite3.Row
    return g.db, conn

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db, conn = get_db()

    db.execute("DROP TABLE users")
    conn.commit()
    db.execute("DROP TABLE posts")
    conn.commit()

    db.execute(
        'CREATE TABLE "posts" ('
        '"id" SERIAL PRIMARY KEY,'
        '"author_id" INT NOT NULL,'
        '"created" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
        '"title" TEXT NOT NULL,'
        '"body" TEXT NOT NULL,'
        'FOREIGN KEY (author_id) REFERENCES "users" (id))'
    )
    conn.commit()
    db.execute(
        'CREATE TABLE "users" ('
        '"id" SERIAL PRIMARY KEY,'
        '"username" TEXT UNIQUE NOT NULL,'
        '"password" TEXT NOT NULL)'
    )
    conn.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)