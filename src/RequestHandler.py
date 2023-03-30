import sqlite3
import uuid
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

# Initialize the database connection
conn = sqlite3.connect('events.db')
conn.execute('''CREATE TABLE IF NOT EXISTS events
                 (id TEXT PRIMARY KEY, timestamp TEXT, event_type TEXT, user_id TEXT, data TEXT)''')
conn.commit()

# HTTP request handler
class RequestHandler(BaseHTTPRequestHandler):

    # Set response headers
    def set_headers(self, status_code):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    # Get query params from request URL
    def get_query_params(self):
        query_components = parse_qs(urlparse(self.path).query)
        return {k: v[0] for k, v in query_components.items()}

    # Authenticate the request
    def authenticate_request(self):
        # Check for a valid API key in the request headers
        if 'X-API-Key' in self.headers and self.headers['X-API-Key'] == 'api_key':
            return True
        else:
            return False

    # Handle GET requests
    def do_GET(self):
        # Authenticate the request
        if not self.authenticate_request():
            self.set_headers(401)
            self.wfile.write(bytes(json.dumps({'message': 'Authentication required.'}), 'utf-8'))
            return

        # Get query parameters
        query_params = self.get_query_params()

        # Construct the SQL query
        sql_query = 'SELECT * FROM events WHERE user_id = ?'
        params = (query_params['user_id'],)

        if 'event_type' in query_params:
            sql_query += ' AND event_type = ?'
            params += (query_params['event_type'],)

        for key, value in query_params.items():
            if key not in ('event_type', 'user_id'):
                sql_query += f" AND data->>'$.{key}' = ?"
                params += (value,)

        # Execute the SQL query
        cursor = conn.execute(sql_query, params)
        events = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

        # Return the response
        self.set_headers(200)
        self.wfile.write(bytes(json.dumps(events), 'utf-8'))

    # Handle POST requests
    def do_POST(self):
        # Authenticate the request
        if not self.authenticate_request():
            self.set_headers(401)
            self.wfile.write(bytes(json.dumps({'message': 'Authentication required.'}), 'utf-8'))
            return

        # Read the request body
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        # Parse the request body
        try:
            event = json.loads(body)
        except:
            self.set_headers(400)
            self.wfile.write(bytes(json.dumps({'message': 'Invalid request body.'}), 'utf-8'))
            return

        # Validate the event
        required_fields = ['event_type', 'user_id']
        for field in required_fields:
            if field not in event:
                self.set_headers(400)
                self.wfile.write(bytes(json.dumps({'message': f"Missing field '{field}' in request body."}), 'utf-8'))
                return

        # Generate a new event ID
        event_id = str(uuid.uuid4())

        # Insert the event into the database
        timestamp = str(datetime.utcnow())
        user_id = event['user_id']
        event_type = event['event_type']
        data = json.dumps({k: v for k, v in event.items() if k not in ('user_id', 'event_type')})
        conn.execute('INSERT INTO events (id, timestamp, event_type, user_id, data) VALUES (?, ?, ?, ?, ?)', (event_id, timestamp, event_type, user_id, data))
        conn.commit()

        # Return the response
        response_body = {'message': 'Event recorded successfully.', 'id': event_id}
        self.set_headers(200)
        self.wfile.write(bytes(json.dumps(response_body), 'utf-8'))
