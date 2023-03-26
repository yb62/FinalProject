import json
from unittest import TestCase
from fastapi.testclient import TestClient
from main import app
from models.user_base import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.trips import Trip
from datetime import date

class TestMyTrips(TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up a temporary test database
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()
        # Create a test user to authenticate the requests
        cls.user = User(username="test_user")
        cls.session.add(cls.user)
        cls.session.commit()
        cls.token = "test_token"

    @classmethod
    def tearDownClass(cls):
        # Clean up the temporary test database
        cls.session.close()
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        self.client = TestClient(app)

    def test_create_trip(self):
        # Send a POST request to the create_trip endpoint with a valid trip payload
        trip_payload = {
            "startDate": "2023-04-01",
            "endDate": "2023-04-10",
            "origin": "New York",
            "destination": "Los Angeles"
        }
        response = self.client.post(
            "/trip/create",
            headers={"Authorization": f"Bearer {self.token}"},
            json=trip_payload
        )
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Check that the response body is a JSON object with a "success" key set to True
        self.assertEqual(response.json(), {"success": True})
        # Check that a new trip was added to the database
        trips = self.session.query(Trip).all()
        self.assertEqual(len(trips), 1)
        self.assertEqual(trips[0].start_date, date(2023, 4, 1))
        self.assertEqual(trips[0].end_date, date(2023, 4, 10))
        self.assertEqual(trips[0].origin, "New York")
        self.assertEqual(trips[0].destination, "Los Angeles")
        self.assertEqual(trips[0].user_id, self.user.id)

    def test_get_trips(self):
        # Add some test trips to the database
        trip1 = Trip(start_date=date(2023, 4, 1), end_date=date(2023, 4, 10), origin="New York", destination="Los Angeles", user_id=self.user.id)
        self.session.add(trip1)
        self.session.commit()
        # Send a GET request to the get_trips endpoint with a valid authorization header
        response = self.client.get(
            "/my-trips",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        trips = response["trips"]
        expected_response = {
            "trips": [
                {
                    "id": trip1.id,
                    "users": [],
                    "events": [],
                    "isCurrentUserInParticipants": True,
                    "startDate": "2023-04-01",
                    "endDate": "2023-04-10",
                    "origin": "New York",
                    "destination": "Los Angeles",
                },
            ],
        }
        self.assertEqual(response.json(), expected_response)

