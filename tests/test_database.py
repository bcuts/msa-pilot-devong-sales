# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from freezegun import freeze_time

from flask_testing import TestCase

import app as subject
from database import db, Purchase


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

    @freeze_time("2017-01-02 03:04:05")
    def test_insert_purchase(self):
        p = Purchase('Delivering', 'scott', 'seoul_dobong')
        db.session.add(p)
        db.session.commit()

        purchases = Purchase.query.all()
        self.assertEqual(len(purchases), 1)
        self.assertEqual(purchases[0].status, 'Delivering')
        self.assertEqual(purchases[0].branch_id, 'seoul_dobong')
        self.assertEqual(purchases[0].user_id, 'scott')
        self.assertEqual(purchases[0].created_at, datetime(2017, 1, 2, 3, 4, 5))



if __name__ == '__main__':
    unittest.main()
