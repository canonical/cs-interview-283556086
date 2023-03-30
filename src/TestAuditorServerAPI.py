import unittest
import uuid

import requests
import json
import sqlite3

# Initialize the database connection
conn = sqlite3.connect(':memory:')
conn.execute('''CREATE TABLE IF NOT EXISTS events
                 (id TEXT PRIMARY KEY, timestamp TEXT, event_type TEXT, user_id TEXT, data TEXT)''')
conn.commit()


class TestAuditorServerAPI(unittest.TestCase):
    def insert_test_events(self):
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()

        # Insert test events into the database
        events = [
            {
                'id': str(uuid.uuid4()),
                'timestamp': '2022-01-01T00:00:00Z',
                'event_type': 'customer_created',
                'user_id': '123',
                'name': 'Daniel Mendoza',
                'data': json.dumps({'email': 'daniel@canonical.com'})
            }
        ]

        for event in events:
            cursor.execute('INSERT INTO events (id, timestamp, event_type, user_id, data) VALUES (?, ?, ?, ?, ?)',
                           (event['id'], event['timestamp'], event['event_type'], event['user_id'], event['data']))

        conn.commit()

    def setUp(self):
        self.base_url = 'http://localhost:8000'
        self.api_key = 'api_key'

        # Remove any existing events table
        conn = sqlite3.connect('events.db')
        conn.execute('''DROP TABLE IF EXISTS events''')
        conn.commit()

        # Create a new events table
        conn.execute('''CREATE TABLE events
                         (id TEXT PRIMARY KEY, timestamp TEXT, event_type TEXT, user_id TEXT, data TEXT)''')
        conn.commit()

        # Insert some test events into the database
        self.insert_test_events()

    def tearDown(self):
        conn.execute('DELETE FROM events')
        conn.commit()

    def test_post_event(self):
        headers = {'Content-type': 'application/json', 'X-API-Key': self.api_key}
        data = {'event_type': 'customer_created', 'user_id': '124', 'name': 'Arturo Hernandez', 'email': 'arturo@canonical.com'}
        response = requests.post(f'{self.base_url}/events', headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertIn('id', response_body)

    def test_get_events_by_user_id(self):
        headers = {'Content-type': 'application/json', 'X-API-Key': self.api_key}
        user_id = '123'
        response = requests.get(f'{self.base_url}/events?user_id={user_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        events = json.loads(response.content)
        self.assertGreater(len(events), 0)

    def test_get_events_by_user_id_and_event_type(self):
        headers = {'Content-type': 'application/json', 'X-API-Key': self.api_key}
        user_id = '123'
        event_type = 'customer_created'
        response = requests.get(f'{self.base_url}/events?user_id={user_id}&event_type={event_type}', headers=headers)
        self.assertEqual(response.status_code, 200)
        events = json.loads(response.content)
        self.assertGreater(len(events), 0)


if __name__ == '__main__':
    unittest.main()
