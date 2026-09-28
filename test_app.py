import json
import os
import sys
import unittest
from unittest.mock import patch

# isort: skip_file

# Ensure the local project directory is searched first to avoid namespace collisions.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import app as local_app

class FlaskInventoryTestSuite(unittest.TestCase):

    def setUp(self):
        self.client = local_app.flask_app.test_client()
        self.client.testing = True
        
        # Inject explicit mock records directly into runtime database array memory space
        local_app.inventory = [
            {
                "id": 1,
                "product_name": "Organic Almond Milk",
                "brands": "Silk",
                "ingredients_text": "Filtered water, almonds, cane sugar, sea salt",
                "quantity": 50
            }
        ]

    def test_get_all_endpoint(self):
        res = self.client.get('/api/inventory')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Organic Almond Milk", res.data)

    def test_get_individual_endpoint(self):
        res = self.client.get('/api/inventory/1')
        self.assertEqual(res.status_code, 200)
        payload = json.loads(res.data)
        self.assertEqual(payload["brands"], "Silk")

    def test_post_creation_endpoint(self):
        mock_data = {"product_name": "Apples", "brands": "Organic", "quantity": 100}
        res = self.client.post('/api/inventory', json=mock_data)
        self.assertEqual(res.status_code, 201)
        payload = json.loads(res.data)
        self.assertEqual(payload["id"], 2)

    def test_patch_mutation_endpoint(self):
        mutation_fields = {"quantity": 125, "brands": "Silk-Premium"}
        res = self.client.patch('/api/inventory/1', json=mutation_fields)
        self.assertEqual(res.status_code, 200)
        payload = json.loads(res.data)
        self.assertEqual(payload["quantity"], 125)
        self.assertEqual(payload["brands"], "Silk-Premium")

    def test_delete_destruction_endpoint(self):
        res = self.client.delete('/api/inventory/1')
        self.assertEqual(res.status_code, 200)
        
        check_res = self.client.get('/api/inventory/1')
        self.assertEqual(check_res.status_code, 404)

    @patch('app.requests.get')
    def test_external_openfoodfacts_route_mocked(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 1,
            "product": {
                "product_name": "Test Rice",
                "brands": "Test Brand",
                "ingredients_text": "Rice Flour"
            }
        }

        res = self.client.get('/api/external/737628064502')
        self.assertEqual(res.status_code, 200)
        payload = json.loads(res.data)
        self.assertEqual(payload["product"]["product_name"], "Test Rice")

if __name__ == '__main__':
    unittest.main()