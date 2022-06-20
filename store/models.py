import datetime
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class ProductCategory(database.Model):
    __tablename__ = "productcategories"
    id = database.Column(database.Integer, primary_key=True)
    productId = database.Column(database.Integer, database.ForeignKey("products.id"), nullable=False)
    categoryId = database.Column(database.Integer, database.ForeignKey("categories.id"), nullable=False)

    def __repr__(self):
        return f"({self.productId}, {self.categoryId})"


class Category(database.Model):
    __tablename__ = "categories"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False)

    products = database.relationship("Product", secondary=ProductCategory.__table__, back_populates="categories")

    def __repr__(self):
        return self.name


class ProductOrder(database.Model):
    __tablename__ = "productorders"
    id = database.Column(database.Integer, primary_key=True)
    productId = database.Column(database.Integer, database.ForeignKey("products.id"), nullable=False)
    orderId = database.Column(database.Integer, database.ForeignKey("orders.id"), nullable=False)
    requested = database.Column(database.Integer, nullable=False)
    received = database.Column(database.Integer, nullable=False)

    def __repr__(self):
        return f"({self.productId}, {self.orderId}, {self.received}/{self.requested})"


class Product(database.Model):
    __tablename__ = "products"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False)
    quantity = database.Column(database.Integer, nullable=False)
    price = database.Column(database.Float, nullable=False)

    categories = database.relationship("Category", secondary=ProductCategory.__table__, back_populates="products")
    orders = database.relationship("Order", secondary=ProductOrder.__table__, back_populates="products")

    def __repr__(self):
        return f"({self.name}, {self.quantity}, {self.price}, {str(self.categories)}, {str(self.orders)})"


class Order(database.Model):
    __tablename__ = "orders"
    id = database.Column(database.Integer, primary_key=True)
    identity = database.Column(database.String(256), nullable=False)
    price = database.Column(database.Float, nullable=False)
    timestamp = database.Column(database.DateTime, nullable=False, default=datetime.datetime.now())

    products = database.relationship("Product", secondary=ProductOrder.__table__, back_populates="orders")

    def __repr__(self):
        return f"({self.identity}, {self.price}, {self.timestamp})"





