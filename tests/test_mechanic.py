
from app import create_app
from app.models import Mechanic, db
import unittest

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanic(name="test_user", email="setup_user@example.com", phone='123-456-7890', salary=1000.0)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "Test User",
            "email": "test@email.com",
            "phone": "123-456-7899",
            "salary": 1500.0
        }

        response = self.client.post("/mechanics/", json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Test User")

    # def test_invalid_creation(self):
    #     invalid_payload = {
    #         "name": "",
    #         "email": "not-an-email",
    #         "phone": "123",
    #         "salary": -500.0
    #     }

    #     response = self.client.post("/mechanics/", json=invalid_payload)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn("name", response.json)
    #     self.assertIn("email", response.json)
    #     self.assertIn("phone", response.json)