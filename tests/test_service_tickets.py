from app import create_app
from app.models import Customer, Mechanic, Service, db
import unittest
from app.utils.util import encode_token

class TestService(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.service_tickets = Service(VIN = "1HGCM82633A123456", service_date = "2023-10-01", service_desc = "Oil Change", mechanics = [], inventory = [])
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            customer = Customer(name="cust", email="cust@example.com", phone="111-111-1111", password="test")
            mechanic = Mechanic(name="Mech", email="mech@example.com", phone="222-222-2222", salary=50000.0)
            db.session.add_all([customer, mechanic])
            db.session.commit()

            self.customer_id = customer.id
            # generate token for the customer (token_required uses this)
            self.token = encode_token(self.customer_id)
        self.client = self.app.test_client()

    # def test_create_service_tickets(self):
    #     payload = {
    #         "VIN": "1HGCM82633A654321",
    #         "service_date": "2023-11-01",
    #         "service_desc": "Tire Rotation",
    #         "mechanics": [],
    #         "inventory": []
    #     }

    #     headers = {"Authorization": "Bearer " + self.token}
    #     resp = self.client.post("/service-tickets/", json=payload, headers=headers)
    #     self.assertEqual(resp.status_code, 201, msg=resp.get_data(as_text=True))
    #     self.assertEqual(resp.json.get("VIN"), payload["VIN"])
    #     self.assertEqual(resp.json.get("service_desc"), payload["service_desc"])

    # def test_invalid_creation(self):
    #     invalid_payload = {
    #         "VIN": "",
    #         "service_date": "invalid-date",
    #         "service_desc": "",
    #     }

    #     headers = {"Authorization": "Bearer " + self.token}
    #     resp = self.client.post("/service-tickets/", json=invalid_payload, headers=headers)
    #     if resp.status_code != 400:
    #         print("RESP BODY:", resp.get_data(as_text=True))
    #     self.assertEqual(resp.status_code, 400)
        
    #     self.assertIsInstance(resp.json, dict)
    #     self.assertIn("service_date", resp.json)
    #     self.assertTrue(len(resp.json["service_date"]) > 0)
    #     self.assertIn("VIN", resp.json)
    #     self.assertTrue(len(resp.json["VIN"]) > 0)
    #     self.assertIn("service_desc", resp.json)
    #     self.assertTrue(len(resp.json["service_desc"]) > 0)

        # assert no Service was created in the database
        with self.app.app_context():
            count = db.session.query(Service).count()
        self.assertEqual(count, 0)

        #testing