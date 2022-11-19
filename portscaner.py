import socket
import threading
import queue
OPEN_PORTS = []

def scan_ports(ip: str, threads: int):
# This is a special list full of PORT numbers
    q = queue.Queue()
    for i in range(1, 1001):
        q.put(i)

    def scan():
        print("PORTSCANNER: Started Scanning")
        # Thread takes port from queue and removes it
        while not q.empty():
            port = q.get()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Sock:
                try:
                    Sock.connect((ip, port))
                    print(f"\nPORTSCANNER: {port} is open\n")
                    OPEN_PORTS.append(port)
                except:
                    pass
            q.task_done()
                
    # Create 30 threads for scanning, daemon=True kills all threads after program stops
    for i in range(threads):
        t = threading.Thread(target=scan, daemon=True)
        t.start()

    #? This makes sure that following code wont execute untill the queue is empty 
    #? We use the q.task_done() to keep track of all operations
    q.join()
    print("PORTSCANNER: Finished scanning.")
    print(f"PORTSCANNER: Ports {OPEN_PORTS} are open.")

    


