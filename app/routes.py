import datetime

from flask import render_template, request, url_for, session
from werkzeug.utils import redirect
from app import app, db, forms
from app.models import Category, Meal, User, Order, order_meals_table
from sqlalchemy.sql.expression import func


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
    error_msg = ""
    form = forms.RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.clientEmail.data).first()
            if user and user.password_valid(form.clientPassword.data):
                session["user"] = {
                    "id": user.id,
                    "email": user.email
                }
            return redirect(url_for('account'))
        else:
            error_msg = "Не верное имя или пароль"
    return render_template("auth.html", form=form, error_msg=error_msg)


@app.route("/account/")
def account():
    orders = []
    if "user" in session:
        orders_db = Order.query.filter_by(email=session["user"]["email"]).all()
        for order in orders_db:
            order_new = [[order.date.strftime("%d/%m/%Y"), order.sum], []]
            meals_db = Meal.query.filter(Meal.orders.any(id=order.id)).all()
            for meal in meals_db:
                order_new[1].append([meal.title, meal.price])
            orders.append(order_new)
    return render_template("account.html", orders=orders)


@app.route("/addtocart/<int:meal_id>/")
def addtocart(meal_id):
    meal = db.session.query(Meal).get_or_404(meal_id)
    if 'cart' not in session:
        session["cart"] = []
    if 'sum' not in session:
        session["sum"] = 0
    if meal_id not in session["cart"]:
        session["cart"].append(meal_id)
        session["sum"] += int(meal.price)
    return redirect(url_for('cart'))


@app.route("/cart/")
def cart():
    form = forms.OrderForm()
    delete_id = 0
    if 'cart' not in session:
        session["cart"] = []
    if 'sum' not in session:
        session["sum"] = 0
    if 'delete_id' in session:
        delete_id = session.pop("delete_id")
    cart_rows = []
    cart_sum = 0
    for meal_id in session["cart"]:
        meal = db.session.query(Meal).get_or_404(meal_id)
        cart_rows.append([meal.title, meal.price, meal.id])
        cart_sum += meal.price
    session["sum"] = cart_sum
    return render_template("cart.html", cart_rows=cart_rows, delete_id=delete_id, form=form)


@app.route("/deletefromcart/<int:meal_id>/")
def deletefromcart(meal_id):
    if 'cart' not in session:
        session["cart"] = []
    if 'sum' not in session:
        session["sum"] = 0
    session["cart"].remove(meal_id)
    session["delete_id"] = meal_id
    return redirect(url_for('cart'))


@app.route("/register/", methods=["GET", "POST"])
def register():
    error_msg = ""
    form = forms.RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = db.session.query(User).filter_by(email=form.clientEmail.data).first()
            if user:
                error_msg = "Пользователь с указанным именем уже существует"
                return render_template("register.html", error_msg=error_msg)
            user_new = User()
            user_new.email = form.clientEmail.data
            user_new.password = form.clientPassword.data
            db.session.add(user_new)
            db.session.commit()
            session["user"] = {
                "id": user_new.id,
                "email": user_new.email
            }
            return redirect(url_for('cart'))
    return render_template("register.html", form=form, error_msg=error_msg)


@app.route("/logout/")
def logout():
    session.pop("user")
    return redirect(url_for('auth'))


@app.route("/ordered/", methods=["POST"])
def ordered():
    form = forms.OrderForm()
    if form.validate_on_submit():
        order = Order()
        user = db.session.query(User).filter_by(email=form.clientEmail.data).first()
        order.email = form.clientEmail.data
        if user:
            order.user = user
        order.date = datetime.date.today()
        order.address = form.clientAddress.data
        order.sum = session["sum"]
        order.phone = form.clientPhone.data
        order.status = "Готовится"
        for meal_id in session["cart"]:
            meal = db.session.query(Meal).get(meal_id)
            order.meals.append(meal)
        db.session.add(order)
        db.session.commit()
        return render_template("ordered.html")
    return redirect(url_for('cart'), form=form)
