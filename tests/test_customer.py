from datetime import datetime
from app import create_app
from app.models import Customer, db
import unittest

from app.utils.util import encode_token

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.customer = Customer(name="test_user", email="setup_user@example.com", phone='123-456-7890' , password='test')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
            self.token = encode_token(1)
        self.client = self.app.test_client()

    def test_create_customer(self):
        customer_payload = {
            "name": "Test User",
            "email": "test@email.com",
            "phone": "123-456-7899",
            "password": "securepassword"
        }

        response = self.client.post("/customers/", json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Test User")

    # def test_invalid_creation(self):
    #     invalid_payload = {
    #         "name": "",
    #         "email": "not-an-email",
    #         "phone": "123",
    #         "password": ""
    #     }

    #     response = self.client.post("/customers/", json=invalid_payload)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn("name", response.json)
    #     self.assertIn("email", response.json)
    #     self.assertIn("phone", response.json)
    #     self.assertIn("password", response.json)

    def test_login_customer(self):
        credentials = {
            "email": "setup_user@example.com",
            "password": "test"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
    
    def test_update_customer(self):
        update_payload = {
            "name": "Peter",
            "email": "setup_user@example.com",
            "phone": "123-456-7890",
            "password": ""
        }
        headers = {'Authorization': "Bearer " + self.token}

        response = self.client.put('/customers/', json=update_payload, headers=headers)
        if response.status_code != 200:
            print("Response JSON:", response.json)
        self.assertEqual(response.status_code, 200, msg=response.get_data(as_text=True))
        self.assertEqual(response.json['name'], 'Peter') 
        self.assertEqual(response.json['email'], 'setup_user@example.com')