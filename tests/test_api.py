# -*- coding: utf-8 -*-

import json
import unittest

from database import db, Purchase
from flask_testing import TestCase

import app as subject


class ApiTest(TestCase):
    def create_app(self):
        app = subject.app
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        subject.db.init_app(app)
        return app

    def setUp(self):
        subject.db.create_all()

    def tearDown(self):
        subject.db.session.remove()
        subject.db.drop_all()

    def test_list_all_purchases_with_no_purchase(self):
        response = self.client.get('/purchases')
        response_data = json.loads(response.data)

        self.assertEqual(len(response_data), 0)

    def test_list_all_purchases(self):
        p = Purchase('Delivering', 'scott', 'seoul_dobong')
        db.session.add(p)
        db.session.commit()

        response = self.client.get('/purchases')
        response_data = json.loads(response.data)

        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['status'], 'Delivering')
        self.assertEqual(response_data[0]['userId'], 'scott')
        self.assertEqual(response_data[0]['branchId'], 'seoul_dobong')

    def test_insert_new_purchases_with_empty_request(self):
        response = self.client.put('/purchases')
        self.assert400(response)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'Invalid request')

    def test_insert_new_purchases_with_missing_key(self):
        data = {'uuuuuserIddd': 'scott'}

        response = self.client.put('/purchases',
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assert400(response)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'Invalid request')

    def test_insert_new_purchases(self):
        data = {
            'userId': 'scott',
            'branchId': 'seoul_dobong'
        }

        response = self.client.put('/purchases',
                                   data=json.dumps(data),
                                   content_type='application/json')

        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'OK')
        self.assertEqual(response_data['purchaseId'], 1)

    def test_get_purchase_with_inexistent_record(self):
        response = self.client.get('/purchases/777')
        self.assert404(response)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'Not found')

    def test_get_purchase(self):
        p = Purchase('Delivering', 'scott', 'seoul_dobong')
        db.session.add(p)
        db.session.commit()

        self.assertEqual(p.id, 1)

        response = self.client.get('/purchases/1')
        self.assert200(response)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'Delivering')
        self.assertEqual(response_data['userId'], 'scott')
        self.assertEqual(response_data['branchId'], 'seoul_dobong')


if __name__ == '__main__':
    unittest.main()
