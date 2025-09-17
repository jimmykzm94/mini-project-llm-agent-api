import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:6001")

# Test add task function
request = {
    "method": "add_task",
    "params": {
        "content": "Test Task from Clientw",
        "description": "This is a test task added via ZeroMQ",
        "due_string": "tomorrow"
    }
}
socket.send_string(json.dumps(request))
response = socket.recv_string()
print("Add result:", json.loads(response))

# Test check tasks function
request = {
    "method": "check_tasks",
    "params": {}
}
socket.send_string(json.dumps(request))
response = socket.recv_string()
print("Tasks:", json.loads(response))

# Test status function
request = {
    "method": "status",
    "params": {}
}
socket.send_string(json.dumps(request))
response = socket.recv_string()
print("Status:", json.loads(response))

socket.close()
context.term()