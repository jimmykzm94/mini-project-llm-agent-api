import zmq
import json

from google_sheet_api import GoogleSheetsAPI
sheet_api = GoogleSheetsAPI()

def get_status():
    """Get server status"""
    return {"status": "ok", "message": "Server is running"}

def find_person(name):
    """Find a person by name in the Google Sheet"""
    try:
        person = sheet_api.find_person_by_name(name)
        if person:
            return {"found": True, "person": person}
        else:
            return {"found": False, "message": f"Person '{name}' not found."}
    except Exception as e:
        raise RuntimeError(f"Failed to find person: {str(e)}")
    
def insert_person(name, age, occupation):
    """Insert a new person into the Google Sheet"""
    try:
        print("Inserting person:", name, age, occupation)
        result = sheet_api.insert_person_data(name, age, occupation)
        return {"inserted": True, "result": result}
    except Exception as e:
        raise RuntimeError(f"Failed to insert person: {str(e)}")
    
def main():
    # Setup ZeroMQ context and socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:6002")
    
    print("Google Sheets Server started. Listening on port 6002...")
    
    # Function mapping
    try:
        api_functions = {
            "status": get_status,
            "find_person": find_person,
            "insert_person": insert_person
        }
        
        while True:
            try:
                # Receive request
                message = socket.recv_string()
                print(f"Received request: {message}")
                
                # Parse JSON request
                request = json.loads(message)
                method = request.get("method")
                params = request.get("params", {})
                
                # Process request
                if method in api_functions:
                    try:
                        result = api_functions[method](**params)
                        response = {
                            "success": True,
                            "result": result
                        }
                    except Exception as e:
                        response = {
                            "success": False,
                            "error": str(e)
                        }
                else:
                    response = {
                        "success": False,
                        "error": f"Method '{method}' not found"
                    }
                
                # Send response
                socket.send_string(json.dumps(response))
                
            except Exception as e:
                # Handle unexpected errors during request processing
                error_response = {
                    "success": False,
                    "error": f"Server error: {str(e)}"
                }
                socket.send_string(json.dumps(error_response))
    except KeyboardInterrupt:
        print("\nShutting down Google Sheets server...")
    finally:
        # Ensure the socket and context are closed on exit
        socket.close()
        context.term()

if __name__ == "__main__":
    main()