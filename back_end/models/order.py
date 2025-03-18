from datetime import datetime
from . import db

class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(255))
    product_type = db.Column(db.String(255))
    product_name = db.Column(db.String(255))
    product_id = db.Column(db.Integer)
    order_time = db.Column(db.String(255), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    prize = db.Column(db.String(255))
    status = db.Column(db.Integer, default=1)
    quantity = db.Column(db.Integer)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(255))