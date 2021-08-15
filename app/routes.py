from flask import render_template, request, url_for, session
from werkzeug.utils import redirect

from app import app, db
from app.models import Category, Meal
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import lazyload


@app.route("/")
def index():
    categories = db.session.query(Category).order_by(Category.title).all()
    categories_show = {}
    for cat in categories:
        categories_show[cat.title] = []
        meals = db.session.query(Meal).filter(Meal.category_id == cat.id).order_by(func.random()).limit(3)
        for meal in meals:
            categories_show[cat.title].append([meal.picture, meal.title, meal.description, meal.id])
    return render_template("main.html", categories=categories_show)


@app.route("/auth/", methods=["GET", "POST"])
def auth():
    if request.method == 'POST':
        return redirect(url_for('account'))
    else:
        return render_template("auth.html")


@app.route("/account/")
def account():
    return render_template("account.html")


@app.route("/addtocart/<int:meal_id>/")
def addtocart(meal_id):
    meal = db.session.query(Meal).get_or_404(meal_id)
    if 'cart' not in session:
        session["cart"] = []
    if 'sum' not in session:
        session["sum"] = 0
    if meal_id not in session["cart"]:
        session["cart"].append(meal_id)
        session["sum"] += meal.price
    return redirect(url_for('cart'))


@app.route("/cart/")
def cart():
    delete_id = 0
    if 'cart' not in session:
        session["cart"] = []
    if 'sum' not in session:
        session["sum"] = 0
    if 'delete_id' in session:
        delete_id = session.pop("delete_id")
    cart_rows = []
    for meal_id in session["cart"]:
        meal = db.session.query(Meal).get_or_404(meal_id)
        cart_rows.append([meal.title, meal.price, meal.id])
    return render_template("cart.html", cart_rows=cart_rows, delete_id=delete_id)


@app.route("/deletefromcart/<int:meal_id>/")
def deletefromcart(meal_id):
    if 'cart' not in session:
        session["cart"] = []
    if 'sum' not in session:
        session["sum"] = 0
    session["cart"].pop(meal_id)
    session["delete_id"] = meal_id
    return redirect(url_for('cart'))
