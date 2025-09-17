def start_zeromq_server():
    import subprocess
    import time
    
    servers_to_start = [
        'todoist_mq.py',
        'google_sheet_mq.py'
    ]
    
    processes = []
    for server_script in servers_to_start:
        process = subprocess.Popen(['python', server_script])
        print(f"Started {server_script} server...")
        processes.append(process)
    
    # Give servers some time to start
    time.sleep(5)
    
    return processes

def stop_zeromq_server(process):
    process.terminate()
    process.wait()
    print(f"Stopped server with PID: {process.pid}")

if __name__ == "__main__":
    running_processes = start_zeromq_server()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping servers...")
    finally:
        for proc in running_processes:
            stop_zeromq_server(proc)