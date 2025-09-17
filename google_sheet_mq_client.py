import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:6002")

# Test find person function
request = {
    "method": "find_person",
    "params": {
        "name": "John Doe"
    }
}
socket.send_string(json.dumps(request))
response = socket.recv_string()
print("Find result:", json.loads(response))

# Test insert person function
request = {
    "method": "insert_person",
    "params": {
        "name": "Alice Smith",
        "age": 30,
        "occupation": "Engineer"
    }
}
socket.send_string(json.dumps(request))
response = socket.recv_string()
print("Insert result:", json.loads(response))

# Try to insert a person without required fields
request = {
    "method": "insert_person",
    "params": {
        "name": "Bob Brown"
        # Missing age and occupation
    }
}
socket.send_string(json.dumps(request))
response = socket.recv_string()
print("Insert incomplete result:", json.loads(response))   




