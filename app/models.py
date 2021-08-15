from app import db

order_meals_table = db.Table('order_meals',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
    db.Column('meal_id', db.Integer, db.ForeignKey('meals.id')),
    db.Column('count', db.Integer),
    db.Column('sum', db.Float(2))
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100))
    orders = db.relationship('Order', back_populates='user')

    def __repr__(self):
        return '<User {} ({})>'.format(self.email, self.id)


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float(2), nullable=False)
    picture = db.Column(db.String(250))
    description = db.Column(db.String(2000))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='meals')
    orders = db.relationship("Order", secondary=order_meals_table, back_populates="meals")

    def __repr__(self):
        return '<Meal {} ({})>'.format(self.title, self.id)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    meals = db.relationship('Meal', back_populates='category')

    def __repr__(self):
        return '<Category {} ({})>'.format(self.title, self.id)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    sum = db.Column(db.Float(2), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='orders')
    meals = db.relationship("Meal", secondary=order_meals_table, back_populates="orders")

    def __repr__(self):
        return '<Order {} ({})>'.format(self.date, self.id)