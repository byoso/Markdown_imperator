#! /usr/bin/env python3

import os
import json


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# initial settings
DB_DIR = os.path.expanduser("~/.local/share/Markdown_Imperator")

DB_NAME = "Markdown_Imperator.sqlite3"
DB_FILE = os.path.join(DB_DIR, DB_NAME)


JSON = "settings.json"
JSON_PATH = os.path.join(BASE_DIR, JSON)


class Settings:
    def __init__(self):
        self.get_settings()

    def get_settings(self):
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
        return data


    def save_settings(self, current_db=None):
        old_data = self.get_settings()
        new_data = {}
        # current database
        if current_db is None:
            current_db = old_data['current_db']
        if os.path.exists(os.path.join(DB_DIR, current_db)):
            new_data['current_db'] = current_db
        else:
            new_data['current_db'] = DB_NAME

        with open(JSON_PATH, 'w') as f:
            json.dump(new_data, f)


settings = Settings()
data = settings.get_settings()
print(data)
print(BASE_DIR)

print(settings.get_settings())