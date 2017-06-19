# -*- coding: utf-8 -*-

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    quantities = db.relationship('PurchaseQuantity')
    status = db.Column(db.String)
    user_id = db.Column(db.String)

    def __init__(self, status, user_id):
        self.status = status
        self.user_id = user_id

    def __repr__(self):
        return '<Purchase by {} at {}>'.format(self.user, self.created_at)

    def serialize(self):
        return {
            'id': self.id,
            'quantities': [pq.serialize() for pq in self.quantities],
            'status': self.status,
            'userId': self.user_id,
        }


class PurchaseQuantity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    product_id = db.Column(db.Integer)
    count = db.Column(db.Integer)

    def __init__(self, product_id, count):
        self.product_id = product_id
        self.count = count

    def __repr__(self):
        return '<PQ: {} products, which id= {}>'.format(self.count, self.product_id)

    def serialize(self):
        return {
            'productId': self.product_id,
            'count': self.count,
        }
