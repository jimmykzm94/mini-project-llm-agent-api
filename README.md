# Mini project - LLM agent API

## Description
1. The frontend console app processes human language into **JSON format** using an LLM.
2. The processed JSON is sent to a backend server through **ZeroMQ**.
3. The backend server calls and interacts with APIs.
    
    **Supported APIs:**
    1. Google Sheets API
    2. Todoist API
 
## Prerequisite
1. **Google Account** – To use Google Sheets API, you need to set it up from Google Cloud. *This setup is not covered here.*
2. **Todoist Account** – Go to `Settings` > `Integrations` > `Developer` tab, and copy the API token.
3. **Python Environment** – Create a virtual environment, activate it, and run:
   ```bash
   pip install -r requirements.txt
   ```
 
## Demo
1. Start the server:
   ```bash
   python start_server.py
   ```
   (Google authentication will be requested the first time you run it.)
2. Open another terminal and run the application:
   ```bash
   python app.py
   ```

### Advanced
Run the server inside a Docker container.

**Build:**
```bash
docker build -t my-google-app .
```

**Run:**
```bash
docker run -d --env-file .env -p 6001:6001 -p 6002:6002 -p 8081:8081 -v "$(pwd)/credentials.json:/app/credentials.json" -v "$(pwd)/google_tokens:/app/google_tokens" --name my-google-app-container my-google-app
```

## Keywords
![Python](https://img.shields.io/badge/Language-Python-blue)
![ZeroMQ](https://img.shields.io/badge/-ZeroMQ-red)
![LLM](https://img.shields.io/badge/-LLM-purple)
![API](https://img.shields.io/badge/-API-yellow)
![Docker](https://img.shields.io/badge/-Docker-blue)
