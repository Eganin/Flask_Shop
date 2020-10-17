from flask import Flask, render_template
from typing import *

app: Flask = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/about")
def about() -> str:
    return render_template("about.html")


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
