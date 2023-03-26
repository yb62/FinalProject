import unittest
from main import app
from models.user_base import *
from core.db import *
from fastapi.testclient import TestClient

class TestLoginAndSignUpFlows(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        # Delete the record from the tokens table
        session = get_db(is_test=True)
        session.query(Token).delete()
        session.query(User).delete()
        session.commit()
        session.close()

    def test_login(self):
        # Test successful login
        credentials = {"username": "testuser", "password": "testpass"}
        response = self.client.post("/login", auth=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertIn("token_type", response.json())

        # Test incorrect password
        credentials = {"username": "testuser", "password": "wrongpass"}
        response = self.client.post("/login", auth=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.json())

        # Test non-existent username
        credentials = {"username": "wronguser", "password": "testpass"}
        response = self.client.post("/login", auth=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.json())

    def test_signup(self):
        # Test successful signup
        user = {"username": "testuser2", "password": "testpass2"}
        response = self.client.post("/signup", json=user)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        
        # Test duplicate username
        user = {"username": "testuser2", "password": "testpass2"}
        response = self.client.post("/signup", json=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())

    def test_read_current_user(self):
        # Test valid token
        response = self.client.get("/users/me", headers={"Authorization": "Bearer valid_token"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.json())
        
        # Test invalid token
        response = self.client.get("/users/me", headers={"Authorization": "Bearer invalid_token"})
        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.json())

if __name__ == "__main__":
    unittest.main()