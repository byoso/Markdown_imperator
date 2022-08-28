#! /usr/bin/env python3
# coding: utf-8

import os

from flask import Flask, render_template, request
from database.database import db

from markdown import markdown


app = Flask(
        __name__,
        static_url_path='',
        static_folder='statics',
        template_folder='templates'
            )


@app.route('/')
def index():
    documents = db().model('document').all()
    categories = db().model('category').all()

    context = {
        'docs': documents,
        'cats': categories,
    }
    return render_template('index.html', **context)


@app.route('/edit/<int:doc_id>', methods=['GET', 'POST'])
def edit(doc_id):
    Doc = db().model("document")

    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('text').strip("\n").strip().strip("\T")
        print(content)
        Doc.update(f"id={doc_id}", title=title, content=content)

    doc = Doc.get_id(doc_id)
    doc.render = markdown(doc.content)
    return render_template('edit.html', doc=doc)


if __name__ == "__main__":
    check_db = db()
    check_db.migrate_all()
    app.run(debug=True)
