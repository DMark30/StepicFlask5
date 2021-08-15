from flask import render_template, request, url_for
from werkzeug.utils import redirect

from app import app, db
from app.models import Category, Meal
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import lazyload


@app.route("/")
def index_page():
    categories = db.session.query(Category).order_by(Category.title).all()
    categories_show = {}
    for cat in categories:
        categories_show[cat.title] = []
        meals = db.session.query(Meal).filter(Meal.category_id == cat.id).order_by(func.random()).limit(3)
        for meal in meals:
            categories_show[cat.title].append([meal.picture, meal.title, meal.description, meal.id])
    return render_template("main.html", categories=categories_show)


@app.route("/auth/", methods=["GET", "POST"])
def auth_page():
    if request.method == 'POST':
        return redirect(url_for('account'))
    else:
        return render_template("auth.html")


@app.route("/account/")
def account_page():
    return render_template("account.html")
