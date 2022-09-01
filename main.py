#! /usr/bin/env python3
# coding: utf-8

import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify)
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
        'docs': documents.jsonify(),
        'cats': categories,
    }
    return render_template('index.html', **context)


@app.route('/edit/<int:doc_id>', methods=['GET', 'POST'])
def edit(doc_id):
    Doc = db().model("document")

    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content').strip("\n").strip()
        Doc.update(f"id={doc_id}", title=title, content=content)
        return jsonify(Doc.get_id(doc_id).jsonify())
    doc = Doc.get_id(doc_id)
    doc.render = markdown(doc.content)
    return render_template('edit.html', doc=doc)


@app.route("/new_file")
def new_file():
    Doc = db().model('document')
    Doc.insert(title="Untitled", content="")
    id = Doc.all()[-1].id
    doc = Doc.get_id(id)
    return redirect(url_for('edit', doc_id=doc.id))


@app.route("/delete/<int:doc_id>")
def delete_doc(doc_id):
    db().model("document").delete(f"id={doc_id}")
    return redirect(url_for('index'))


if __name__ == "__main__":
    check_db = db()
    check_db.migrate_all()
    app.run(debug=True)
