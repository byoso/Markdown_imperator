#! /usr/bin/env python3
# coding: utf-8

import os

from flask import Flask, render_template
from silly_db.db import DB
# from database.database import db


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


def db_build():
    db = DB(
        base=BASE_DIR,
        file="database/MD_imperator_db.sqlite3",
        migrations_dir="database/migrations")
    db.migrate_all()
    return db


@app.route('/')
def hello():
    db = db_build()
    Cat = db.model('cat')

    cats = Cat.all()

    context = {
        'name': "Marie",
        'cats': cats,
    }
    return render_template('index.html', **context)


if __name__ == "__main__":
    app.run(debug=True)
