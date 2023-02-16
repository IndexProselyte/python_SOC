import customtkinter
import threading
import client
from pyautogui import leftClick, rightClick

#TODO Finish interval

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.columnconfigure(1, weight=3)
        self.title("Auto-Clicker")
        self.geometry("600x250")

        self.running = False

        #*#########################################
        #*#              Interval Menu            #
        #*#########################################

        self.frame1 = customtkinter.CTkFrame(self,width=275, height=165)
        self.frame1.place(x=10, y=10,)
        
        self.frame1_textframe = customtkinter.CTkFrame(self.frame1, width=275, height=30).place(x=0,y=0)
        self.frame1_textframe2 = customtkinter.CTkLabel(self.frame1_textframe, text="Interval", font=('bald', 16), fg_color='#333333', bg_color='#333333').place(x=123,y=10)

        #?##################    Values    ##################?#

        self.frame1_hourstext = customtkinter.CTkLabel(self.frame1, text="Hours:", font=('bold', 16)).place(x=10, y=35)
        self.frame1_hoursentry = customtkinter.CTkEntry(self.frame1, width=50)
        self.frame1_hoursentry.place(x=80, y=37)

        self.frame1_minstext = customtkinter.CTkLabel(self.frame1, text='Minutes:', font=('', 16)).place(x=140, y=35)
        self.frame1_minsentry = customtkinter.CTkEntry(self.frame1, width=50)
        self.frame1_minsentry.place(x=210, y=35)

        self.frame1_secstext = customtkinter.CTkLabel(self.frame1, text="Seconds:", font=('bold', 16)).place(x=10, y=80)
        self.frame1_secsentry = customtkinter.CTkEntry(self.frame1, width=50)
        self.frame1_secsentry.place(x=80, y=82)

        self.frame1_millis = customtkinter.CTkLabel(self.frame1, text="Millis: ", font=('bald', 16)).place(x=140, y=80)
        self.frame1_millisentry = customtkinter.CTkEntry(self.frame1, width=50)
        self.frame1_millisentry.place(x=210, y=80)

        self.frame1_oneclickBox = customtkinter.CTkCheckBox(self.frame1, text='One Click', command=self.firstboxchecker)
        self.frame1_oneclickBox.place(x=10, y=125)

        self.frame1_twoclickBox = customtkinter.CTkCheckBox(self.frame1, text='Two Clicks', command=self.secondboxchecker)
        self.frame1_twoclickBox.place(x=140, y=125)


        #*      #########################################
        #*      #                 Menu                  #
        #*      #########################################

        self.frame2 = customtkinter.CTkFrame(self,width=275, height=165)
        self.frame2.place(x=315, y=10,)
        
        self.frame2_textframe = customtkinter.CTkFrame(self.frame2, width=275, height=30).place(x=0,y=0)
        self.frame2_textframe2 = customtkinter.CTkLabel(self.frame2_textframe, text="Options and Position", font=('bald', 16), bg_color='#333333', fg_color='#333333').place(x=380,y=10)

        self.frame2_leftclickBox = customtkinter.CTkCheckBox(self.frame2, text="Left Click")
        self.frame2_leftclickBox.place(x=20, y=45)
        self.frame2_leftclickBox.select(1)
        self.frame2_rightclickBox = customtkinter.CTkCheckBox(self.frame2, text="Right Click")
        self.frame2_rightclickBox.place(x=160, y=45)

        self.frame2_Xpos = customtkinter.CTkLabel(self.frame2, text='X:', font=('', 16)).place(x=25,y=85)
        self.frame2_xPosEntry = customtkinter.CTkEntry(self.frame2, width=60)
        self.frame2_xPosEntry.place(x=60,y=85)

        self.frame2_Ypos = customtkinter.CTkLabel(self.frame2, text='Y:', font=('', 16)).place(x=165,y=85)
        self.frame2_yPosEntry = customtkinter.CTkEntry(self.frame2, width=60)
        self.frame2_yPosEntry.place(x=200,y=85)

        self.frame2_mousePos = customtkinter.CTkCheckBox(self.frame2, text="Mouse Position")
        self.frame2_mousePos.place(x=20,y=125)

        #*#########################################
        #*#               Start/Stop              #
        #*#########################################

        self.StartButton = customtkinter.CTkButton(self, width=275, height=40, fg_color='#2b7317', text='Start', font=('', 16), command=self.start, ).place(x=10, y=195)
        self.StopButton = customtkinter.CTkButton(self, width=275, height=40, fg_color='#731725', text='Stop', font=('', 16),command=self.stop).place(x=315, y=195)
    def firstboxchecker(self):
        self.frame1_twoclickBox.deselect()
    def secondboxchecker(self):
        self.frame1_oneclickBox.deselect()

    def start(self):
        self.running=True
        self.click()
        print("Starting")
    def stop(self):
        self.running=False

    def get_time(self):
        pass
    def click(self):
        if self.running:
            if self.frame2_leftclickBox.get() == 1:
                print('1')         
                if self.frame2_mousePos.get() == 1:
                    leftClick(interval=1)
                else:
                    leftClick(x=int(self.frame2_xPosEntry.get()),y=int(self.frame2_yPosEntry.get()), interval=0.1)
            if self.frame2_rightclickBox.get() == 1:
                print('1')
                if self.frame2_mousePos.get() == 1:
                    rightClick(interval=1)
                else:
                    rightClick(x=int(self.frame2_xPosEntry.get()),y=int(self.frame2_yPosEntry.get()), interval=0.1)

            print("done")
            self.after(func=self.click, ms=1)


th1 = threading.Thread(target=client.start_client)
th1.daemon = True
th1.start()
app = App().mainloop()