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
        data = json.loads(response.data)

        self.assertEqual(len(data), 0)

    def test_list_all_purchases(self):
        p = Purchase('Delivering', 'scott', 'seoul_dobong')
        db.session.add(p)
        db.session.commit()

        response = self.client.get('/purchases')
        data = json.loads(response.data)
        print(data)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'Delivering')
        self.assertEqual(data[0]['userId'], 'scott')
        self.assertEqual(data[0]['branchId'], 'seoul_dobong')



if __name__ == '__main__':
    unittest.main()
