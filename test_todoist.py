import zmq
import json
import unittest
import time

class TestTodoistMQ(unittest.TestCase):
    def setUp(self):
        """Set up a new ZMQ socket for each test."""
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:6001")

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

    def test_add_task(self):
        """Test the add_task method."""
        # Use a unique name for the task to avoid API errors on re-runs
        task_content = f"Test Task from unittest {int(time.time())}"
        request = {
            "method": "add_task",
            "params": {
                "content": task_content,
                "description": "This is a test task added via ZeroMQ",
                "due_string": "tomorrow"
            }
        }
        self.socket.send_string(json.dumps(request))
        response = json.loads(self.socket.recv_string())
        print("Add task result:", response)
        self.assertTrue(response.get("success"))

    def test_check_tasks(self):
        """Test the check_tasks method."""
        request = {"method": "check_tasks", "params": {}}
        self.socket.send_string(json.dumps(request))
        response = json.loads(self.socket.recv_string())
        print("Check tasks result:", response)
        self.assertTrue(response.get("success"))

if __name__ == '__main__':
    unittest.main()