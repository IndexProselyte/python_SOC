import customtkinter
import threading
import client

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Auto-Clicker")
        self.geometry("600x400")

        self.frame1 = customtkinter.CTkFrame(self, width=565, height=180)
        self.frame1.pack(side=customtkinter.TOP, pady=15)
        self.frame1.grid_propagate(False)
        ### Text ###
        self.frametextInfo = customtkinter.CTkLabel(
            self.frame1, text="Click Interval")
        self.frametextInfo.pack(side=customtkinter.TOP, pady=10)
        self.button = customtkinter.CTkButton(
            self.frame1, text="Open Dialog", command=None)
        self.button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

        # Speed Frame
        self.frame_frame1 = customtkinter.CTkFrame(
            self.frame1, width=565, height=80)
        self.frame_frame1.pack(side=customtkinter.TOP)

        self.frame2 = customtkinter.CTkFrame(self, width=260, height=100)
        self.frame2.pack(side=customtkinter.LEFT, padx=20)
        self.frame2.grid_propagate(False)

        self.frame2textInfo = customtkinter.CTkLabel(
            self.frame2, text="Click Options")
        self.frame2textInfo.pack(side=customtkinter.TOP, pady=10)

        self.frame_frame2 = customtkinter.CTkFrame(
            self.frame2, width=260, height=100)
        self.frame_frame2.pack(side=customtkinter.TOP)

        self.frame3 = customtkinter.CTkFrame(self, width=260, height=100)
        self.frame3.pack(side=customtkinter.RIGHT, padx=20)
        self.frame3.grid_propagate(False)

        self.frame3textInfo = customtkinter.CTkLabel(
            self.frame3, text="Click Repeat")
        self.frame3textInfo.pack(side=customtkinter.TOP, pady=10)

        self.frame_frame3 = customtkinter.CTkFrame(
            self.frame3, width=260, height=100)
        self.frame_frame3.pack(side=customtkinter.TOP)

        self.frame4 = customtkinter.CTkFrame(self, width=565, height=300)
        self.frame4.pack(side=customtkinter.BOTTOM, pady=20)
        self.frame4.grid_propagate(False)

        self.frame4textInfo = customtkinter.CTkLabel(
            self.frame4, text="Click Repeat")
        self.frame4textInfo.pack(side=customtkinter.TOP, pady=10)

        self.frame_frame4 = customtkinter.CTkFrame(
            self.frame4, width=565, height=80)
        self.frame_frame4.pack(side=customtkinter.TOP)

        def changeInterval():
            pass

        def repeatClicking():
            pass

        def openOptions():
            pass

th1 = threading.Thread(target=client.start_client)
th1.daemon = False
th1.start()
app = App().mainloop()
