# -*- coding: utf-8 -*-

import json
import unittest
from unittest import mock
from unittest.mock import ANY, call

from database import db, Purchase
from flask_testing import TestCase

import app as subject
from delegate.exceptions import IntegrationException


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

    @staticmethod
    def request_body_to_insert():
        return {
            'userId': 'scott',
            'branchId': 'seoul_dobong',
            'details': [
                {
                    'productId': 'product_first',
                    'count': 1
                }, {
                    'productId': 'product_second',
                    'count': 2
                }
            ]
        }

    @mock.patch('delegate.branch.get')
    @mock.patch('delegate.product.get')
    def test_insert_new_purchases(self, mock_product_get, mock_branch_get):
        mock_branch_get.return_value = {
            'id': 'seoul_dobong'
        }
        mock_product_get.side_effect = [{
            'id': 'product_first'
        }, {
            'id': 'product_second'
        }, {
            'id': 'product_third'
        }]

        data = self.request_body_to_insert()

        response = self.client.put('/purchases',
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'OK')
        self.assertEqual(response_data['purchaseId'], 1)

        mock_branch_get.assert_called_with('seoul_dobong', ANY)
        mock_product_get.assert_has_calls([call('product_first', ANY), call('product_second', ANY)])

    @mock.patch('delegate.branch.get')
    def test_insert_new_purchases_with_branch_api_error(self, mock_branch_get):
        mock_branch_get.side_effect = IntegrationException("Something wrong")

        data = {
            'userId': 'scott',
            'branchId': 'seoul_dobong'
        }

        response = self.client.put('/purchases',
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assert500(response)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'Something wrong with Branch API. Please contact Administrator')

    @mock.patch('delegate.branch.get')
    def test_insert_new_purchases_with_invalid_branch_id(self, mock_branch_get):
        mock_branch_get.return_value = None

        data = self.request_body_to_insert()

        response = self.client.put('/purchases',
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assert400(response)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'Invalid branch id')

    @mock.patch('delegate.branch.get')
    @mock.patch('delegate.product.get')
    def test_insert_new_purchases_with_product_api_error(self, mock_product_get, mock_branch_get):
        mock_branch_get.return_value = {'id': 'seoul_dobong'}
        mock_product_get.side_effect = IntegrationException("Something wrong")

        data = self.request_body_to_insert()

        response = self.client.put('/purchases',
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assert500(response)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'Something wrong with Product API. Please contact Administrator')

    @mock.patch('delegate.branch.get')
    @mock.patch('delegate.product.get')
    def test_insert_new_purchases_with_invalid_product_id(self, mock_product_get, mock_branch_get):
        mock_branch_get.return_value = {'id': 'seoul_dobong'}
        mock_product_get.return_value = None

        data = self.request_body_to_insert()

        response = self.client.put('/purchases',
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assert400(response)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'Invalid product id')

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
