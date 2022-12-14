#! /usr/bin/env python3
# coding: utf-8


import os
from silly_db.db import DB

from settings import DB_DIR, Settings


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
current_db = Settings().get_settings()['current_db']

def db(file=None):
    if file == None:
        db = DB(
            base=BASE_DIR,
            file=os.path.join(DB_DIR, Settings().get_settings()['current_db']),
            migrations_dir="migrations")
    else:
        db = DB(
            base=BASE_DIR,
            file=file,
            migrations_dir="migrations")
    return db

def create_new_database(new_db_name):
    db = DB(
        base=BASE_DIR,
        file=os.path.join(DB_DIR, new_db_name),
        migrations_dir="migrations"
    )
    return db
