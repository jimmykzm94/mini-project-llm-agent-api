import ollama
import zmq
import json

context = zmq.Context()
socket_todoist = context.socket(zmq.REQ)
socket_todoist.connect("tcp://localhost:6001")
socket_google_sheet = context.socket(zmq.REQ)
socket_google_sheet.connect("tcp://localhost:6002")

def query_ollama(prompt, model="llama3.2"):
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def send_todoist(request):
    # Get request json
    json_request = json.loads(request)
    method = json_request.get("method")
    params = json_request.get("params", {})

    # Check method and params, ignore extra or noise params
    if method not in ["add_task", "check_tasks", "status"]:
        raise ValueError(f"Unsupported method '{method}' for Todoist.")
    
    if method == "add_task":
        if not all(k in params for k in ("content", "description", "due_string")):
            raise ValueError("Missing required parameters for 'add_task' method.")
        
        content = params.get("content")
        description = params.get("description")
        due_string = params.get("due_string")

        params = {
            "content": content,
            "description": description,
            "due_string": due_string
        }
    elif method in ["check_tasks", "status"]:
        params = {}
    
    # Set request
    new_request = {
        "method": method,
        "params": params
    }
    socket_todoist.send_string(json.dumps(new_request))
    response = socket_todoist.recv_string()
    return response

def send_google_sheet(request):
    # Get request json
    json_request = json.loads(request)
    method = json_request.get("method")
    params = json_request.get("params", {})

    # Check method and params, ignore extra or noise params
    if method not in ["find_person", "insert_person", "status"]:
        raise ValueError(f"Unsupported method '{method}' for Google Sheet.")
    
    if method == "find_person":
        if "name" not in params:
            raise ValueError("Missing required parameter 'name' for 'find_person' method.")
        
        name = params.get("name")
        params = {
            "name": name
        }
    elif method == "insert_person":
        if not all(k in params for k in ("name", "age", "occupation")):
            raise ValueError("Missing required parameters for 'insert_person' method.")
        
        name = params.get("name")
        age = params.get("age")
        occupation = params.get("occupation")

        params = {
            "name": name,
            "age": age,
            "occupation": occupation
        }
    elif method == "status":
        params = {}
    
    # Set request
    new_request = {
        "method": method,
        "params": params
    }
    socket_google_sheet.send_string(json.dumps(new_request))
    response = socket_google_sheet.recv_string()
    return response

def send_request_to_server(request):
    try:
        json_request = json.loads(request)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format generated from ollama.")
    method = json_request.get("method")

    if method == "status":
        # Send to both servers and combine results
        todoist_response = send_todoist(request)
        google_sheet_response = send_google_sheet(request)
        return {
            "todoist": json.loads(todoist_response),
            "google_sheet": json.loads(google_sheet_response)
        }
    if method in ["add_task", "check_tasks"]:
        return send_todoist(request)
    elif method in ["find_person", "insert_person"]:
        return send_google_sheet(request)
    else:
        raise ValueError(f"Unsupported method '{method}' in the request.")

if __name__ == "__main__":
    try:
        prompt = """
        Strictly return one json only, no explanations.
        Unknown or unsupported methods should return an error message in json.

        Supported methods:
        1. find_person
        2. insert_person
        3. add_task
        4. check_tasks
        5. status

        Example output json:
        {{
            "method": "find_person",
            "params": {{
                "name": "John Doe"
            }}
        }}
        
        
        Query:
        {query}
        """
        new_prompt = prompt.format(query="Hello, who are you?")
        # new_prompt = prompt.format(query="Who is Alice Smith?")
        # new_prompt = prompt.format(query="What is status of my Todoist and Google Sheet servers?")
        # new_prompt = prompt.format(query="What is status of my Todoist")
        # new_prompt = prompt.format(query="Find person named John Doe")
        # new_prompt = prompt.format(query="Add a new person named Alice Smith, age 30, occupation Engineer")
        # new_prompt = prompt.format(query="Add a new person named Bob Brown without age and occupation")
        new_prompt = prompt.format(query="Add a new task to my Todoist with content 'Finish the report', description 'Due by end of the week', due_string 'in 2 days'")
        # new_prompt = prompt.format(query="Check my tasks in Todoist")
        response = query_ollama(new_prompt)
        print(f"Ollama response: {response}")
        # Determine which server to send based on method
        final_response = send_request_to_server(response)
        print(f"Final response: {final_response}")
    finally:
        socket_todoist.close()
        socket_google_sheet.close()
        context.term()
