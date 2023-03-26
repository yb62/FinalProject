import click

import uvicorn
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from core.user_management import UserManagement
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime

from core.db import *

from models.trips import *
from models.user_base import *
from models.basic_models import *

app = FastAPI()
security = HTTPBasic()
bearer_security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/signup")
def signup(user: UserIn, session=Depends(get_db)) -> ActionSuccessResponse:
    """
        Create a new user account.

        This function creates a new user by adding a record to the `users` table.

        Args:
        - user (UserIn): A model containing the new user's username and password.
        - session (sqlalchemy.orm.session.Session): The SQLAlchemy database session.

        Returns:
        dict: A dictionary containing a success message.

        Raises:
        HTTPException: If the provided username is already taken.
    """
    existing_user = UserManagement.get_user(session, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    UserManagement.create_user(
        session, user.username, user.password, user.full_name)
    return ActionSuccessResponse(success=True)


def authenticate_user(session, username: str, password: str):
    return session.query(User).filter(User.username == username, User.password == password).first()


@app.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security), session=Depends(get_db)):
    """
        Authenticate a user and return an access token.

        This function authenticates a user by checking their username and password against the records in the `users` table.
        If the credentials are valid, it generates and returns a new access token.

        Args:
        - credentials (HTTPBasicCredentials): The username and password provided by the user.
        - session (sqlalchemy.orm.session.Session): The SQLAlchemy database session.

        Returns:
        TokenOut: A model containing the access token and token type.

        Raises:
        HTTPException: If the credentials are invalid.
    """
    user = authenticate_user(
        session, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")
    token = UserManagement.create_access_token(session, user)
    return TokenOut(access_token=token, token_type="bearer")


@app.get("/users/me")
def read_current_user(session=Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(bearer_security)):
    """
        Retrieve the current user's username.

        This function retrieves the current user's username by looking up the user's ID in the `tokens` table,
        then using the ID to look up the user's record in the `users` table.

        Args:
        - session (sqlalchemy.orm.session.Session): The SQLAlchemy database session.

        Returns:
        UserOut: A model containing the current user's username.
    """
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=400, detail="Incorrect authorization type")
    # Look up the user associated with the token
    user = UserManagement.get_current_user(session, credentials.credentials)
    # Verify such user exists
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return UserOut(username=user.username, fullName=user.full_name)

@app.get("/user/{username}")
def read_current_user(username: str, session=Depends(get_db)):
    """
        Retrieve the current user's username.

        This function retrieves the request user details.

        Args:
        - session (sqlalchemy.orm.session.Session): The SQLAlchemy database session.
        - token (str): The access token provided by the user.

        Returns:
        UserOut: A model containing the reqest user details
    """
    user = UserManagement.get_user(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return UserOut(username=user.username, fullName=user.full_name)


@app.post("/trip/create")
def create_trip(tripIn: TripIn, credentials: HTTPAuthorizationCredentials = Depends(bearer_security), session=Depends(get_db)):
    """
        Create a new trip for the authenticated user.

        Args:
        - tripIn (TripIn): The input data for the new trip.
        - credentials (HTTPAuthorizationCredentials): The bearer token for authenticating the user.
        - session (Session): The database session.

        Returns:
        ActionSuccessResponse: A response indicating whether the action was successful.
        
        Raises:
        HTTPException: If there was an error with the authentication or if the user was not found.
    """
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=400, detail="Incorrect authorization type")
    # Look up the user associated with the token
    user = UserManagement.get_current_user(session, credentials.credentials)
    # Verify such user exists
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    # Create the trip object and add it to the database
    trip = Trip(
        start_date=datetime.strptime(tripIn.startDate, "%Y-%m-%d").date(),
        end_date=datetime.strptime(tripIn.endDate, "%Y-%m-%d").date(),
        origin=tripIn.origin,
        destination=tripIn.destination,
        user_id=user.id
    )

    session.add(trip)
    session.commit()

    user_trip_assoc = TripUsers(
        user_id=user.id,
        trip_id=trip.id
    )

    session.add(user_trip_assoc)
    session.commit()

    return ActionSuccessResponse(success=True)


@app.get("/my-trips")
def get_trips(credentials: HTTPAuthorizationCredentials = Depends(bearer_security), session=Depends(get_db)):
    """
        Retrieve trips for the authenticated user.

        This endpoint returns a list of trips associated with the authenticated user. The user is authenticated using a Bearer token, and if the authentication fails, the function raises an HTTPException with status code 400 and the detail message "Incorrect authorization type" or "User not found" if the user is not present in the database.

        Args:
        - credentials (HTTPAuthorizationCredentials): the authentication credentials provided by the client.
        - session (Session): the SQLAlchemy session object used to interact with the database.
        
        Returns:
        - TripsOut: A Pydantic model object containing a list of trips associated with the authenticated user. Each trip is represented as a TripOut object, which contains details about the trip including the participants and events associated with it.
        
        Raises:
        HTTPException(400): If the authentication fails, the user is not found in the database or the user is not associated with any trips.
    """
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=400, detail="Incorrect authorization type")
    # Look up the user associated with the token
    user = UserManagement.get_current_user(session, credentials.credentials)
    # Verify such user exists
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    trips = session.query(Trip).filter(Trip.user_id == user.id)
    return TripsOut(trips=[convert_trip(session, trip) for trip in trips])


@app.get("/all-trips")
def get_trips(credentials: HTTPAuthorizationCredentials = Depends(bearer_security), session=Depends(get_db)):
    """
        Retrieves all trips from the database.

        Args:
        - credentials (HTTPAuthorizationCredentials, optional): The authorization credentials of the user. Defaults to Depends(bearer_security).
        - session (Session, optional): The database session. Defaults to Depends(get_db).
        
        Raises:
        HTTPException: If the credentials scheme is not 'bearer' or the user is not found in the database.
        
        Returns:
        TripsOut: A response model containing a list of TripOut objects representing the retrieved trips.
    """
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=400, detail="Incorrect authorization type")
    # Look up the user associated with the token
    user = UserManagement.get_current_user(session, credentials.credentials)
    # Verify such user exists
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    trips = session.query(Trip)
    return TripsOut(trips=[convert_trip(session, trip) for trip in trips])


@app.get("/trip/{trip_id}")
def get_trips(trip_id: int, credentials: HTTPAuthorizationCredentials = Depends(bearer_security), session=Depends(get_db)):
    """
        This function handles GET requests to retrieve details of a specific trip by its ID.

        Args:
        - trip_id (int): ID of the trip to retrieve details for.
        - credentials (HTTPAuthorizationCredentials, optional): HTTP authorization credentials required for authentication.
        - session (sqlalchemy.orm.Session, optional): Database session object.
        
        Returns:
        TripOut: TripOut object containing the details of the trip, including its participants, events, and basic information.
        
        Raises:
        HTTPException(400): If the authorization type is incorrect or the user is not found.
        HTTPException(404): If the trip with the given ID is not found.
    """
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=400, detail="Incorrect authorization type")

    user = UserManagement.get_current_user(session, credentials.credentials)

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    trip = session.query(Trip).filter(Trip.id == trip_id).first()

    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    return convert_trip(session, trip, user)


@app.post("/trip/add-participant")
def create_trip(participantData: AddTripParticipantPostData, credentials: HTTPAuthorizationCredentials = Depends(bearer_security), session=Depends(get_db)):
    """
        Adds a participant to an existing trip.

        Args:
        - participantData (AddTripParticipantPostData): A data model for the participant to be added to the trip.
        - credentials (HTTPAuthorizationCredentials): The credentials of the user making the request.
        - session: The database session.
        
        Returns:
        An ActionSuccessResponse data model with a success message.

        Raises:
        HTTPException(400): If the authorization type is incorrect or the user is not found.
    """
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=400, detail="Incorrect authorization type")

    user = UserManagement.get_current_user(session, credentials.credentials)

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    user_trip_assoc = TripUsers(
        user_id=user.id,
        trip_id=participantData.trip_id
    )

    session.add(user_trip_assoc)
    session.commit()

    return ActionSuccessResponse(success=True)


@app.post("/trip/remove-participant")
def create_trip(participantData: RemoveTripParticipantPostData, credentials: HTTPAuthorizationCredentials = Depends(bearer_security), session=Depends(get_db)):
    """
        Endpoint to remove a participant from a trip.

        Args:
        - participantData: RemoveTripParticipantPostData - object containing the ID of the trip to remove the participant from
        - credentials: HTTPAuthorizationCredentials - authorization header for user authentication
        - session: Session = Depends(get_db) - database session dependency
        
        Returns:
        ActionSuccessResponse: An object with a boolean indicating the success or failure of the operation.

        Raises:
        HTTPException: An exception is raised if the authorization header is incorrect or if the user is not found.
    """
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=400, detail="Incorrect authorization type")

    user = UserManagement.get_current_user(session, credentials.credentials)

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    allTripUserAssocs = session.query(TripUsers).all()

    user_trip_assocs = (
        session
        .query(TripUsers)
        .filter(
            (TripUsers.user_id == user.id) and
            (TripUsers.trip_id == participantData.trip_id)
        )
        .all()
    )

    for assoc in user_trip_assocs:
        session.delete(assoc)
    session.commit()

    return ActionSuccessResponse(success=True)


@app.post("/trip/add-event")
def create_trip(newEventData: AddTripEventPostData, credentials: HTTPAuthorizationCredentials = Depends(bearer_security), session=Depends(get_db)):
    """
        Adds a new event to the specified trip.

        Args:
        - newEventData (AddTripEventPostData): A Pydantic model representing the new event to be added.
        - credentials (HTTPAuthorizationCredentials): The bearer token representing the user's authorization.
        - session (Session): The SQLAlchemy database session.

        Returns:
        ActionSuccessResponse: A Pydantic model indicating the success or failure of the operation.
        
        Raises:
        HTTPException: If the user is not authorized or is not found in the database.
    """
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=400, detail="Incorrect authorization type")

    user = UserManagement.get_current_user(session, credentials.credentials)

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    event = TripEvent(
        description=newEventData.description,
        time=datetime.strptime(newEventData.time, "%Y-%m-%d").date(),
        trip_id=newEventData.trip_id,
    )

    session.add(event)
    session.commit()

    return ActionSuccessResponse(success=True)


@app.post("/trip/remove-event")
def create_trip(eventData: RemoveTripEventPostData, credentials: HTTPAuthorizationCredentials = Depends(bearer_security), session=Depends(get_db)):
    """
        Remove an event from a trip.

        Args:
        - eventData: RemoveTripEventPostData: An object containing the event ID to remove from the trip.
        - credentials: HTTPAuthorizationCredentials: The authentication credentials of the user making the request.
        - session: sqlalchemy.orm.Session: The database session.
        
        Returns:
        ActionSuccessResponse: An object containing a boolean value indicating whether the action was successful.

        Raises:
        HTTPException: If the user is not authorized or is not found in the database.
    """
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=400, detail="Incorrect authorization type")

    user = UserManagement.get_current_user(session, credentials.credentials)

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    event = (
        session
        .query(TripEvent)
        .filter(
            TripEvent.id == eventData.event_id
        )
        .one()
    )

    session.delete(event)
    session.commit()

    return ActionSuccessResponse(success=True)


@app.delete("/trips/{trip_id}")
def delete_trip(trip_id: int, credentials: HTTPAuthorizationCredentials = Depends(bearer_security), session=Depends(get_db)):
    """
        This function deletes a trip identified by the given trip ID. It requires a valid bearer token for authentication, and the user associated with the token must exist. If the trip ID is not found, it raises an HTTPException with status code 404. If the authentication type is incorrect, it raises an HTTPException with status code 400.

        Args:
        - trip_id (int): ID of the trip to be deleted
        - credentials (HTTPAuthorizationCredentials): HTTP authorization credentials
        - session: SQLAlchemy session dependency
        
        Returns:
        ActionSuccessResponse: An object containing a Boolean value indicating whether the action was successful or not.

        Raises:
        HTTPException: If the user is not authorized or is not found in the database.
    """
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=400, detail="Incorrect authorization type")
    # Look up the user associated with the token
    user = UserManagement.get_current_user(session, credentials.credentials)
    # Verify such user exists
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    trip = session.query(Trip).filter(Trip.id == trip_id).first()
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    session.delete(trip)
    session.commit()

    return ActionSuccessResponse(success=True)


@click.command()
@click.option("--port", default=8000, help="Port to run the server on")
def main(port):
    uvicorn.run(app, port=port)


if __name__ == "__main__":
    main()
