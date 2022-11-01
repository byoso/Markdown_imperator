#! /usr/bin/env python3
# coding: utf-8

import os
import json
import webbrowser
from silly_db.selections import Selection

from flask import (
    flash,
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify)
from database.database import db, create_new_database

from settings import DB_DIR, settings
from helpers import intersection


if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
check_db = db()
check_db.migrate_all()

app = Flask(
        __name__,
        static_folder='statics',
        template_folder='templates'
            )
app.secret_key = "NO SECRET KEY, IT IS A LOCAL APP"



@app.route('/', methods=['GET', 'POST'])
def index():
    filters = []
    selected_documents = Selection()
    if request.method == "POST":
        filters = [int(filter) for filter in request.form.getlist('filters')]

        Category = db().model('category')
        for cat in Category.sil.all():
            if cat.id in filters:
                Category.sil.update(f"id={cat.id}", checked=1)
            else:
                Category.sil.update(f"id={cat.id}", checked=0)

    # filtering documents that are in all the filters selected
    if len(filters) == 0:
        selected_documents = db().model('document').sil.all().order_by('title')
    else:
        results = []
        ids = []
        for id in filters:
            documents = db().select(
                "DISTINCT "
                "document.id "
                "FROM document JOIN cat_doc ON document.id=cat_doc.doc_id "
                f"AND cat_id={id} "
            )
            results.append(documents)
        for result in results:
            ids.append([item.id for item in result.items])
        ids = intersection(*ids)

        sql_ids = ""
        for id in ids:
            sql_ids += f"'{id}',"
        sql_ids = sql_ids[:-1]
        selected_documents = db().select(
            "id, title, content "
            f"FROM document WHERE id IN ({sql_ids}) "
        )

    categories = db().model('category').sil.all().order_by('name')
    context = {
        'docs': selected_documents.order_by('title').jsonify(),
        'categories': categories.jsonify(),
    }
    return render_template('index.html', **context)


@app.route('/edit/<int:doc_id>', methods=['GET', 'POST'])
def edit(doc_id):
    Doc = db().model("document")
    Category = db().model('category')
    Cat_doc = db().model("cat_doc")

    if request.method == "POST":
        categories = json.loads(request.form.get('categories'))
        for category in categories:
            if category[1] == True:
                if not Cat_doc.sil.filter(f"cat_id={category[0]} AND doc_id={doc_id}").exists():
                    Cat_doc.sil.insert(cat_id=category[0], doc_id=doc_id)
            else:
                Cat_doc.sil.delete(f"cat_id={category[0]} AND doc_id={doc_id}")
        title = request.form.get('title')
        content = request.form.get('content').strip("\n").strip()
        Doc.sil.update(f"id={doc_id}", title=title, content=content)
        return jsonify(Doc.sil.get_id(doc_id).jsonify())

    doc = Doc.sil.get_id(doc_id)
    categories = Category.sil.all().order_by("name")
    checked_cats = db().select(f"cat_id FROM cat_doc WHERE doc_id={doc_id}")
    checked_ids = [cat.cat_id for cat in checked_cats]
    for cat in categories:
        if cat.id in checked_ids:
            cat.is_checked = True
        else:
            cat.is_checked = False

    categories = categories.jsonify()

    context = {
        'doc': doc,
        'categories': categories,
    }
    return render_template('edit.html', **context)

@app.route("/print_content/<int:doc_id>")
def print_content(doc_id):
    Document = db().model('document')
    document = Document.sil.get_id(doc_id)

    context = {
        'document': document,
    }
    return render_template('print_content.html', **context)

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
    db().model('cat_doc').sil.delete(f"doc_id={doc_id}")
    return redirect(url_for('index'))


@app.route("/categories", methods=['GET', 'POST'])
def categories():
    if request.method == "POST":
        category_name = request.form.get('category_name')
        Category = db().model('category')
        Category.sil.insert(name=category_name)

    categories = db().model("category").sil.all().order_by('name')
    context = {
        "categories": categories
    }
    return render_template('categories.html', **context)


@app.route("/delete_category/<int:pk>", methods=['GET'])
def delete_category(pk):
    print("delete ", pk)
    Category = db().model('category')
    Cat_doc = db().model('cat_doc')
    Cat_doc.sil.delete(f"cat_id={pk}")
    Category.sil.delete(f"id={pk}")
    return redirect(url_for('categories'))


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/databases/", methods=['GET', 'POST'])
def databases():
    databases = [file for file in os.listdir(DB_DIR) if file.endswith('.sqlite3')]
    current_database = settings.get_settings()['current_db']
    context = {
        'databases': databases,
        'current_database': current_database,
    }
    return render_template("databases.html", **context)


@app.route("/create_database/", methods=['POST'])
def create_database():
    if request.form.get('new_database') == "":
        flash("Can not create a new database without a name")
        return redirect(url_for('databases'))

    new_database = request.form.get('new_database') + ".sqlite3"
    new_database = new_database.replace(" ", "_")
    if os.path.exists(os.path.join(DB_DIR, new_database)):
        flash(f"Impossible: a database called {new_database} already exists !")
    else:
        db = create_new_database(new_database)
        db.migrate_all()
        flash(f"database created: {new_database}")
    return redirect(url_for('databases'))


@app.route("/select_database/", methods=['POST'])
def select_database():
    new_db = request.form.get('selected_database')
    settings.save_settings(current_db=new_db)
    flash(f"Database selected: {new_db}")
    return redirect(url_for('index'))

@app.route("/open_database_folder/", methods=["POST"])
def open_database_folder():
    os.system(f"xdg-open '{DB_DIR}'")
    return redirect(url_for('databases'))


if __name__ == "__main__":
    app.run(debug=True)
