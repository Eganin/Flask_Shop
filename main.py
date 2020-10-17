from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout
from typing import *

app: Flask = Flask(__name__)
# указываем настройку какую БД будем использовать
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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

    def __repr__(self) -> str:
        return f"Запись : {self.title}"


@app.route("/")
def index() -> str:
    # получаем все данные из таблицы Item с сортировкой по цене
    items: Item = Item.query.order_by(Item.price).all()
    # отправляем данные на страницу
    return render_template("index.html", data=items)


@app.route("/about")
def about() -> str:
    return render_template("about.html")


# на данной странице отслеживаем запросы POST
@app.route("/create", methods=["POST", "GET"])
def create() -> str:
    if request.method == "POST":
        # получаем отправленные данные
        title: str = request.form["title"]
        price: str = request.form["price"]

        # запись в бд
        item: Item = Item(title=title, price=price)

        try:
            # сохраняем запись в БД
            db.session.add(item)
            db.session.commit()
            # делаем переадресацию на главную страницу
            return redirect("/")
        except:
            return "ERROR"
    else:
        return render_template("create.html")


# отследивание динамического URI
@app.route("/buy/<int:id>")
def item_buy(id: int):
    # получаем item по id
    item: Item = Item.query.get(id)

    # всзимодействуем с  API для оплаты
    api: Api = Api(merchant_id=1396424,
                   secret_key="test")
    checkout: Checkout = Checkout(api=api)
    data: Dict[str, str] = {
        "currency": "RUB",
        "amount": str(item.price) + "00"
    }

    # url покупки товара
    url: str = checkout.url(data).get("checkout_url")

    return redirect(url)


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
