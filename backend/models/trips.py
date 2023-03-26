from typing import List, Optional
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.user_base import *
from pydantic import BaseModel
from datetime import date

class Trip(Base):
    """
        This table / model is responsible for
        storing basic trip metadata about a trip.
    """
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True)
    start_date = Column(Date)
    end_date = Column(Date)
    origin = Column(String)
    destination = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))


class TripUsers(Base):
    """
        This table / model is responsible for
        storing the relationship of going to the trip
        between users and trips. 
    """
    __tablename__ = "trip_users"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete='CASCADE'))


class TripEvent(Base):
    __tablename__ = 'trip_event'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    time = Column(String)
    trip_id = Column(Integer, ForeignKey('trips.id', ondelete='CASCADE'))

class AddTripEventPostData(BaseModel): 
    description: str
    time: str 
    trip_id: int 

class RemoveTripEventPostData(BaseModel): 
    event_id: int 

class TripEventGetData(BaseModel):
    description: str 
    time: str 
    id: int

class AddTripParticipantPostData(BaseModel):
    trip_id: str 

class RemoveTripParticipantPostData(BaseModel):
    trip_id: str 

class TripIn(BaseModel):
    startDate: str
    endDate: str
    origin: str
    destination: str


class TripOut(BaseModel):
    id: int
    users: List[UserOut]
    events: List[TripEventGetData]
    isCurrentUserInParticipants: bool
    startDate: date
    endDate: date
    origin: str
    destination: str


class TripsOut(BaseModel):
    trips: List[TripOut]


def convert_trip(session, trip: Trip, currentUser: Optional[User] = None) -> TripOut:
    """
        Converts a Trip object to a TripOut object, which includes the trip details along with its participants and events.

        Args:
        session: SQLAlchemy session object.
        trip: A Trip object to be converted.
        currentUser: An optional User object representing the current user. If provided, it is used to determine if the current user is in the list of participants.

        Returns:
        A TripOut object with the trip details and its associated participants and events.
    """
    participants = convert_trip_participants(session, trip)
    return TripOut(
        users=participants,
        events=convert_trip_events(session, trip),
        isCurrentUserInParticipants=any(
            participant.username == (currentUser.username if currentUser is not None else None) 
            for participant in participants
        ),
        id=trip.id,
        startDate=trip.start_date,
        endDate=trip.end_date,
        origin=trip.origin,
        destination=trip.destination,
    )


def convert_trip_participants(session, trip: Trip) -> List[UserOut]:
    """
        Converts the participants associated with a given trip to a list of UserOut objects.

        Args:
            session: A SQLAlchemy session object used for database operations.
            trip: A Trip object representing the trip for which to retrieve participants.

        Returns:
            A list of UserOut objects representing the participants associated with the given trip.
    """
    users = (
        session.query(User)
        .join(TripUsers)
        .filter(
            TripUsers.trip_id == trip.id
        )
        .all()
    )

    return [convert_user(user) for user in users];

def convert_trip_event(trip_event: TripEvent) -> TripEventGetData:
    """
        Converts a TripEvent object to TripEventGetData object.

        Args:
        trip_event (TripEvent): A TripEvent object to convert.

        Returns:
        TripEventGetData: A TripEventGetData object containing the converted data.
    """
    return TripEventGetData(
        description=trip_event.description,
        time=trip_event.time,
        id=trip_event.id
    )

def convert_trip_events(session, trip: Trip) -> List[TripEventGetData]:
    """
        Converts a list of TripEvent objects to a list of TripEventGetData objects.

        Args:
        session: A SQLAlchemy session object.
        trip: A Trip object representing the trip for which the events are being converted.

        Returns:
        A list of TripEventGetData objects representing the events for the given trip, ordered by time.
    """
    trip_events = (
        session.query(TripEvent)
        .filter(
            TripEvent.trip_id == trip.id
        )
        .order_by(TripEvent.time.asc())
        .all()
    )

    return [convert_trip_event(trip_event) for trip_event in trip_events]