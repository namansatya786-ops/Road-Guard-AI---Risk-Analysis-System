import unittest

from app import app


class RoadGuardApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ROADGUARD", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertEqual(body["status"], "online")
        self.assertIn("model_loaded", body)

    def test_invalid_prediction_payload(self):
        response = self.client.post("/api/predict", json={
            "weather": "Unknown",
            "road": "Urban",
            "traffic": "Low",
            "time": "Morning",
            "condition": "Good",
            "speed": 40,
            "visibility": 10,
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_valid_prediction_payload(self):
        response = self.client.post("/api/predict", json={
            "weather": "Fog",
            "road": "Intersection",
            "traffic": "High",
            "time": "Night",
            "condition": "Damaged",
            "speed": 100,
            "visibility": 1,
        })
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertIn(body["risk_level"], ("Low", "Medium", "High"))
        self.assertGreaterEqual(body["confidence"], 0)
        self.assertLessEqual(body["confidence"], 100)


if __name__ == "__main__":
    unittest.main()
