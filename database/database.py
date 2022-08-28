#! /usr/bin/env python3
# coding: utf-8


import os
from silly_db.db import DB


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def db():
    db = DB(
        base=BASE_DIR,
        file="MD_imperator_db.sqlite3",
        migrations_dir="migrations")
    return db
