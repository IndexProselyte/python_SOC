import threading
import platform
from time import sleep
import socket
import psutil
import os
from uuid import getnode

# Get the hostname of the computer
hostname = socket.gethostname()
# Get the IP address of the computer
ip_address = socket.gethostbyname(hostname)
# Get the operating system information
os_name = os.name
os_release = platform.release()
os_version = platform.version()
# Get the mac address
mac_adr = ':'.join(['{:02x}'.format((getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
# Get the processor information
processor_name = platform.processor()
processor_architecture = platform.architecture()[0]
# Get the memory information
total_memory = round(psutil.virtual_memory().total / (1024 ** 3), 2)
available_memory = round(psutil.virtual_memory().available / (1024 ** 3), 2)
used_memory = round(total_memory - available_memory, 2)
# Get the disk usage information
total_disk_space = round(psutil.disk_usage('/').total / (1024 ** 3), 2)
used_disk_space = round(psutil.disk_usage('/').used / (1024 ** 3), 2)
free_disk_space = round(psutil.disk_usage('/').free / (1024 ** 3), 2)

gather_SOIP = "127.0.0.69"
gather_SOPORT = 42069

def startGathering():
    th = threading.Thread(target=Gathering)
    th.daemon=True
    th.start()

def Gathering():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((gather_SOIP, gather_SOPORT))

        #? Sending PC informations to the Server
        sock.send((f"Name: {hostname}").encode('utf-8'))
        sleep(0.2)
        sock.send((f"Mac Address: {mac_adr}").encode('utf-8'))
        sleep(0.2)
        sock.send((f"OS: {os_name} {os_release} {os_version}").encode('utf-8'))
        sleep(0.2)
        sock.send((f"Processor: {processor_name} {processor_architecture}").encode('utf-8'))
        sleep(0.2)
        sock.send((f"Memory: {total_memory} GB (Used: {used_memory} GB, Available: {available_memory} GB)").encode('utf-8'))
        sleep(0.2)
        sock.send((f"Disk Space: {total_disk_space} GB (Used: {used_disk_space} GB, Free: {free_disk_space} GB)").encode('utf-8'))
        sleep(0.2)


        sock.send("END_SENDING".encode('utf-8')) # End of sending informations
        print("Sending information was finished!")
        sock.close()
