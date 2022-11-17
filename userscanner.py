from os import path
from glob import glob

def getuser(): # Get all users from C:\Users\
    return [path.basename(x) for x in glob('C:\\Users\\*') if x not in ['C:\\Users\\Public', 'C:\\Users\\All Users', 'C:\\Users\\Default', 'C:\\Users\\Default User', 'C:\\Users\\desktop.ini']]

def getfiles(scan_user: str, dict_files: str):
    return [path.basename(x) for x in glob('C:\\Users\\'+scan_user+'\\'+dict_files+'\\*') if '.lnk' not in x]

print(getfiles('surov', 'Documents'))
