# Final Project -- "Travel Buddies"
## Collaborative Trip Planning Web-Application

## Developer Setup

### Backend

1. `python -m venv env`
2. `source env/bin/activate`
3. `pip install -r ./backend/requirements.txt`
4. `cd backend`
5. `python main.py`

This would start up the python webserver on the `8000` port. A port can be overriden if `--port` argument is provided.

### Frontend

1. `cd frontend`
2. `npm i`
3. ☕️ (while installing)
4. `npm start`

This would start up the UI on the `3000` port and would expect the backend it needs to talk to be on the `8000` port.