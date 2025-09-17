import todoist_api as todoist
import zmq
import json
import os
from dotenv import load_dotenv

load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")

def get_status():
    """Get server status"""
    return {"status": "ok", "message": "Server is running"}

def add_task(content, description, due_string):
    """Add a new task to Todoist"""
    try:
        task = todoist.api.add_task(
            content=content,
            description=description,
            project_id=PROJECT_ID,
            due_string=due_string
        )
        return {"task_id": task.id, "content": task.content}
    except Exception as e:
        raise RuntimeError(f"Failed to add task: {str(e)}")
    
def check_tasks():
    """Check and return all tasks in the project"""
    try:
        tasks_iter = todoist.api.get_tasks(project_id=PROJECT_ID)
        tasks = []
        for task_list in tasks_iter:
            tasks.extend(task_list)
        return [{"id": task.id, "content": task.content, "description": task.description} for task in tasks]
    except Exception as e:
        raise RuntimeError(f"Failed to fetch tasks: {str(e)}")

def main():
    # Setup ZeroMQ context and socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:6001")
    
    print("Todoist Server started. Listening on port 6001...")
    
    # Function mapping
    try:
        api_functions = {
            "status": get_status,
            "add_task": add_task,
            "check_tasks": check_tasks
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
        print("\nShutting down Todoist server...")
    finally:
        # Ensure the socket and context are closed on exit
        socket.close()
        context.term()

if __name__ == "__main__":
    main()