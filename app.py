# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from database import db, Purchase

import config
from delegate import branch, product
from delegate.exceptions import IntegrationException

app = Flask(__name__)
CORS(app)  # TODO Avoid this later!


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
    if not json or 'userId' not in json or 'branchId' not in json:
        return jsonify({
            'status': 'Invalid request'
        }), 400

    # Check branch
    branch_id = json['branchId']
    try:
        if not branch.get(branch_id, config.get_branch_api_endpoint()):
            return jsonify({
                'status': 'Invalid branch id'
            }), 400
    except IntegrationException:
        return jsonify({
            'status': 'Something wrong with Branch API. Please contact Administrator'
        }), 500

    # Check products
    product_ids = [d['productId'] for d in json['details']]
    try:
        for product_id in product_ids:
            if not product.get(product_id, config.get_product_api_endpoint()):
                return jsonify({
                    'status': 'Invalid product id'
                }), 400
    except IntegrationException:
        return jsonify({
            'status': 'Something wrong with Product API. Please contact Administrator'
        }), 500

    p = Purchase(status='Preparing', user_id=json['userId'], branch_id=branch_id)
    db.session.add(p)
    db.session.commit()
    return jsonify({
        'status': 'OK',
        'purchaseId': p.id
    }), 201


@app.route('/purchases/<purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    p = Purchase.query.filter(Purchase.id == purchase_id).first()
    if not p:
        return jsonify({
            'status': 'Not found'
        }), 404

    return jsonify(p.serialize()), 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./development.db'

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=port)
