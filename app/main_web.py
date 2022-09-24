#! /usr/bin/env python3
# coding: utf-8

import os
import webbrowser

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify)
from database.database import db

from settings import DB_DIR


app = Flask(
        __name__,
        static_url_path='',
        static_folder='statics',
        template_folder='templates'
            )


@app.route('/external_link/', methods=['POST'])
def external_link(url):
    webbrowser.open(url, new=2)



@app.route('/')
def index():
    documents = db().model('document').sil.all().order_by('title')
    categories = db().model('category').sil.all().order_by('name')

    context = {
        'docs': documents.jsonify(),
        'categories': categories,
    }
    return render_template('index.html', **context)


@app.route('/edit/<int:doc_id>', methods=['GET', 'POST'])
def edit(doc_id):
    Doc = db().model("document")

    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content').strip("\n").strip()
        Doc.sil.update(f"id={doc_id}", title=title, content=content)
        return jsonify(Doc.sil.get_id(doc_id).jsonify())
    doc = Doc.sil.get_id(doc_id)
    context = {
        'doc': doc,
    }
    return render_template('edit.html', **context)


@app.route("/new_file")
def new_file():
    Doc = db().model('document')
    Doc.sil.insert(title="Untitled", content="")
    id = Doc.sil.all()[-1].id
    doc = Doc.sil.get_id(id)
    return redirect(url_for('edit', doc_id=doc.id))


@app.route("/delete/<int:doc_id>")
def delete_doc(doc_id):
    db().model("document").sil.delete(f"id={doc_id}")
    return redirect(url_for('index'))


@app.route("/categories", methods=['GET', 'POST'])
def categories():
    if request.method == "POST":
        category_name = request.form.get('category_name')
        Category = db().model('category')
        Category.sil.insert(name=category_name)

    categories = db().model("category").sil.all().order_by('name').jsonify()
    context = {
        "categories": categories
    }
    return render_template('categories.html', **context)


@app.route("/delete_category/<int:pk>", methods=['GET'])
def delete_category(pk):
    print("delete ", pk)
    Category = db().model('category')
    Category.sil.delete(f"id={pk}")
    return redirect(url_for('categories'))


if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
check_db = db()
check_db.migrate_all()


if __name__ == "__main__":
    app.run(debug=True)
