# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify
from database import db, Purchase

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/purchases', methods=['GET'])
def list_all_purchases():
    purchases = Purchase.query.all()
    serialized = [p.serialize() for p in purchases]

    return jsonify(serialized)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./development.db'

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=port)
