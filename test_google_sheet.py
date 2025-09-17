import zmq
import json
import unittest

class TestGoogleSheetMQ(unittest.TestCase):
    def setUp(self):
        """Set up a new ZMQ socket for each test."""
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:6002")

    def tearDown(self):
        """Close the ZMQ socket after each test."""
        self.socket.close()
        self.context.term()

    def test_status(self):
        """Test the status method."""
        request = {"method": "status", "params": {}}
        self.socket.send_string(json.dumps(request))
        response = json.loads(self.socket.recv_string())
        print("Status result:", response)
        self.assertTrue(response.get("success"))

    def test_find_person(self):
        """Test the find_person method."""
        request = {
            "method": "find_person",
            "params": {"name": "John Doe"}
        }
        self.socket.send_string(json.dumps(request))
        response = json.loads(self.socket.recv_string())
        print("Find person result:", response)
        self.assertTrue(response.get("success"))

    def test_insert_person_success(self):
        """Test successful insertion of a person."""
        request = {
            "method": "insert_person",
            "params": {
                "name": "Test User",
                "age": 99,
                "occupation": "Tester"
            }
        }
        self.socket.send_string(json.dumps(request))
        response = json.loads(self.socket.recv_string())
        print("Insert person result:", response)
        # This will fail if the person already exists, which is expected for subsequent runs.
        # For a robust test, you might add cleanup logic to delete the user.
        self.assertTrue(response.get("success"))

    def test_insert_person_incomplete_fails(self):
        """Test that inserting a person with incomplete data fails gracefully."""
        request = {"method": "insert_person", "params": {"name": "Bob Brown"}}
        self.socket.send_string(json.dumps(request))
        response = json.loads(self.socket.recv_string())
        print("Insert incomplete result:", response)
        self.assertFalse(response.get("success"))

if __name__ == '__main__':
    unittest.main()
