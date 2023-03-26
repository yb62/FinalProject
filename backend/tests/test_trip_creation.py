import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user_base import Base, User
from main import app
from datetime import date
from models.trips import Trip, TripUsers

client = TestClient(app)

class TripCreationTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test user for authentication
        self.engine = create_engine("sqlite:///test_mydatabase.db")
        sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        Base.metadata.create_all(bind=self.engine)
        self.user = User(
            email="testuser@example.com",
            hashed_password="password123",
            username="testuser",
        )
        self.db = sessionLocal()
        self.db.add(self.user)
        self.db.commit()

    def tearDown(self):
        # Remove the test user and any created trips after each test
        self.db.delete(self.user)
        self.db.query(Trip).delete()
        self.db.commit()

    def test_create_trip(self):
        # Log in as the test user
        response = client.post(
            "/auth/login",
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data={
                "username": "testuser",
                "password": "password123"
            }
        )
        access_token = response.json()["access_token"]

        # Create a new trip using the access token
        trip_data = {
            "startDate": "2023-04-01",
            "endDate": "2023-04-05",
            "origin": "San Francisco",
            "destination": "Los Angeles"
        }
        response = client.post(
            "/trip/create",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            json=trip_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})

        # Verify that the trip was created correctly
        trip = self.db.query(Trip).first()
        self.assertIsNotNone(trip)
        self.assertEqual(trip.start_date, date(2023, 4, 1))
        self.assertEqual(trip.end_date, date(2023, 4, 5))
        self.assertEqual(trip.origin, "San Francisco")
        self.assertEqual(trip.destination, "Los Angeles")
        self.assertEqual(trip.user_id, self.user.id)

        # Verify that the test user is associated with the trip
        user_trip_assoc = self.db.query(TripUsers).filter(TripUsers.trip_id == trip.id).first()
        self.assertIsNotNone(user_trip_assoc)
        self.assertEqual(user_trip_assoc.user_id, self.user.id)
