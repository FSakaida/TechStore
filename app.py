from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def catalogo():
    return render_template("index.html")


@app.route("/carrinho")
def carrinho():
    return render_template("carrinho.html")


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/sucesso")
def sucesso():
    return render_template("sucesso.html")


if __name__ == "__main__":
    app.run(debug=True)
