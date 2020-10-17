from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from typing import *

app: Flask = Flask(__name__)
# указываем настройку какую БД будем использовать
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
db: SQLAlchemy = SQLAlchemy(app=app)


# класс представляющий поля таблицы из БД
class Item(db.Model):
    # autoincrement and primary key id
    id: db = db.Column(db.Integer, primary_key=True)
    # title  not null
    title: db = db.Column(db.String(100), nullable=False)
    # price not null
    price: db = db.Column(db.Integer, nullable=False)
    # isActive default value = True
    isActive = db.Column(db.Boolean, nullable=True)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/about")
def about() -> str:
    return render_template("about.html")


@app.route("/create")
def create() -> str:
    return render_template("create.html")


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
