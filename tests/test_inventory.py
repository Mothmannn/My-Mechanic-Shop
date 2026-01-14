
from app import create_app
from app.models import Inventory, db
import unittest

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.inventory = Inventory(part_name= "test_part", price= 99.99)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.inventory)
            db.session.commit()
            self.inventory_id = self.inventory.id
        self.client = self.app.test_client()

    def test_create_inventory(self):
        inventory_payload = {
            "part_name": "Brake Pad",
            "price": 49.99
        }

        response = self.client.post("/inventory/", json=inventory_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['part_name'], "Brake Pad")

    # def test_invalid_creation(self):
    #     invalid_payload = {
    #         "part_name": "",
    #         "price": -10.0
    #     }

    #     response = self.client.post("/inventory/", json=invalid_payload)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn("part_name", response.json)
    #     self.assertIn("price", response.json)

    def test_update_part(self):
        update_payload = {
            "part_name": "Updated Part Name",
            "price": 79.99
        }

        part_id = self.inventory_id
        response = self.client.put(f'/inventory/{part_id}', json=update_payload)
        if response.status_code != 200:
            print("Response JSON:", response.json)
        self.assertEqual(response.status_code, 200, msg=response.get_data(as_text=True))
        self.assertEqual(response.json['part_name'], "Updated Part Name")
        self.assertEqual(response.json['price'], 79.99)