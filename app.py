# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, request
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


@app.route('/purchases', methods=['POST', 'PUT'])
def insert_new_purchases():
    json = request.get_json(silent=True)
    if not json or not 'userId' in json or not 'branchId' in json:
        return jsonify({
            'status': 'Invalid request'
        }), 400

    p = Purchase(status='Preparing', user_id=json['userId'], branch_id=json['branchId'])
    db.session.add(p)
    db.session.commit()
    return jsonify({
        'status': 'OK',
        'purchaseId': p.id
    }), 201


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./development.db'

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=port)
