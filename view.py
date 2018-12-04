#!/usr/bin/env python3
""" The view module manages the GUI """
import tkinter as tk
import tkinter.messagebox
import csv

import params as p
import auth
import egram
import comms

class LoginFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.pack()
        self.master = master
        self.start = auth.auth()

        #Setting up intial login screen
        master.title("3K04 - Group 12 - Heartscape")
        master.geometry("400x400")
        tk.Label(master, text="", font = "none 10").pack()
        tk.Label(master, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(master, text="", font = "none 10").pack()

        #setting up login and password entry fields
        tk.Label(master, text="Username:", font="none 12").pack()
        self.usernameBox = tk.Entry(master, width=14)
        self.usernameBox.pack()

        tk.Label(master, text="Password:", font="none 12").pack()
        self.passwordBox = tk.Entry(master, width = 14)
        self.passwordBox.pack()

        #Setting up login and register buttons
        tk.Label(master, text="", font="none 5").pack() 
        tk.Button(master, text="Log In", fg="white", bg="green", font="none 12 bold", command=self.login).pack()
        tk.Label(master, text="", font="none 5").pack() 
        tk.Button(master, text="Register", font="none 12 bold", command=self.register).pack()


    #if login button is pressed
    def login(self):
        self.start = auth.auth()
        username = self.usernameBox.get()
        password = self.passwordBox.get()
        if (self.start.login_auth(username, password) == False):
            tk.Label (self, text="Incorrect Credentials", fg="red", font="none 11").pack()
            username = None
            password = None
        else:
            self.master.withdraw()
            win_login = MainWin(master=root)
            win_login.title("Pacemaker DCM")

    #if register button is pressed
    def register(self):
        self.master.withdraw()
        win_register = RegisterFrame(master=root)
        win_register.title("Register User")

        
class RegisterFrame(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.geometry("400x400")
        tk.Label(self, text="3K04 - Group 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="~Please fill in the info below~", font="none 12 bold").pack()
        tk.Label(self, text="                     ", font="none 12").pack()

        #Grabbing username
        tk.Label(self, text="Username:", font="none 12").pack()
        self.username = tk.Entry(self, width = 14)
        self.username.pack()
        #Grabbing password
        tk.Label(self, text="Password:", font="none 12").pack()
        self.password = tk.Entry(self, width=14)
        self.password.pack()

        #Grabbing password again to avoid password mismatch
        tk.Label(self, text="Re-Enter Password:", font="none 12").pack()
        self.password2 = tk.Entry(self, width=14)
        self.password2.pack()
        
        tk.Label(self, text="                     ", font="none 12").pack()

        #Register button
       
        tk.Button(self, text="Register", font="none 12 bold", command=self.RegisterButton).pack()
        tk.Button(self, text="Return", font="none 12 bold", command=self.return_Login).pack()
                  
    def RegisterButton(self):
        NewUser = self.username.get()
        NewPass = self.password.get()
        NewPass2 = self.password2.get()

        self.start = auth.auth()
        if (NewUser == "") or (NewPass == ""):
            tk.Label(self, text="Invalid Input", fg="red", font="none 12 bold").pack()
        elif (NewPass != NewPass2):
            tk.Label(self, text="Passwords do not match", fg="red", font="none 12 bold").pack()
        else:
            if (self.start.reg_auth(NewUser, NewPass) == (True, False, False)):
                tk.Label(self, text="Successful", fg="green", font="none 12 bold").pack()
            elif (self.start.reg_auth(NewUser, NewPass) == (False, False, True)):
                tk.Label(self, text="User Already Exists", fg="red", font="none 12 bold").pack()
            elif (self.start.reg_auth(NewUser, NewPass) == (False, True, False)):
                tk.Label(self, text="Max Users", fg="red", font="none 12 bold").pack()
            elif (self.start.reg_auth(NewUser, NewPass) == (False, True, True)):
                tk.Label(self, text="Max Users", fg="red", font="none 12 bold").pack()

    def return_Login(self):
        self.withdraw()
        root.deiconify()
            
class NumericParamFrame(tk.Frame):
    def __init__(self, param, name, master=None):
        super().__init__(master)
        self.pack()

        self.param = param
        self.name = name
        
        self.tk_var = tk.IntVar()
        self.tk_var.set(self.param.get())

        self.create_widgets()

    def create_widgets(self):
        self.tk_incr_button = tk.Button(self, text=">", command=self.incr)
        self.tk_decr_button = tk.Button(self, text="<", command=self.decr)

        if self.name:
            self.tk_name = tk.Label(self, text=self.name)
        else:
            self.tk_name = tk.Label(self, text="param")

        self.tk_value = tk.Label(self, textvariable=self.tk_var)

        self.tk_name.pack(side="left")
        self.tk_decr_button.pack(side="left")
        self.tk_value.pack(side="left")
        self.tk_incr_button.pack(side="left")

    def incr(self):
        self.param.increment()
        self.tk_var.set(self.param.get());

    def decr(self):
        self.param.decrement()
        self.tk_var.set(self.param.get());

"""
Allows user to set non numeric parameter values.
TODO:
    - make it neater
        - consider if this should be replaced with radio button menu instead
        - horizontal or vertical orientation?
    - button to default to nominal value
    -
"""
class NonNumericParamFrame(tk.Frame):
    def __init__(self, param, name, master=None):
        super().__init__(master)
        self.pack()
        self.param = param
        self.name = name
        self.tk_var = tk.StringVar()
        self.tk_var.set(self.param.get_str())
        # add callback for when tk_var gets written by the radio-button events
        self.tk_var.trace_add("write", self.update_param)

        self.create_widgets()

    def create_widgets(self):
        if self.name:
            self.tk_name = tk.Label(self, text=self.name)
        else:
            self.tk_name = tk.Label(self, text="param")
        self.tk_name.pack(side="left")

        for text in self.param.get_strings():
            b = tk.Radiobutton(master=self, text=text, variable=self.tk_var, value=text)
            b.pack(side="left")

    def update_param(self, *args):
        self.param.set(self.tk_var.get())

class NonNumericParamDropDown(NonNumericParamFrame):
    def create_widgets(self):
        if self.name:
            self.tk_name = tk.Label(self, text=self.name)
        else:
            self.tk_name = tk.Label(self, text="param")
        self.tk_name.pack(side="left")

        values = self.param.get_strings()
        self.options = tk.OptionMenu(self, self.tk_var, *values)
        self.options.pack(side="left")

""" Connection Status Light to check if the pacemaker is connected. """
class Light(tk.Label):
    def __init__(self, master=None, period=100):
        self.tk_text = tk.StringVar()
        self.light = super().__init__(master=master, relief="raised", textvariable=self.tk_text)
        self.pack(anchor="w")

        self.period = period

        self.check_status()

    def check_status(self):
        if (comms.pacemaker_connected()):
            self.turn_on()
        else:
            self.turn_off()

        self.after(self.period, self.check_status)

    def turn_on(self):
        self.tk_text.set("Connected")
        self.configure(bg="green")

    def turn_off(self):
        self.tk_text.set("Disconnected")
        self.configure(bg="red")

class MainWin(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        l1 = tk.Label(self, text="\nPlease choose a pacing mode from the\ndrop down menu labelled Mode \nor by pressing one of the buttons below.", font="none 12").pack()
        #http://www.scoberlin.de/content/media/http/informatik/tkinter/x5441-patterns.htm

        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text ="VOO", font = "none 12 bold", command = self.VOO).pack(fill = tk.X)
        tk.Button(self, text ="AOO", font = "none 12 bold", command = self.AOO).pack(fill = tk.X)
        tk.Button(self, text ="VVI", font = "none 12 bold", command = self.VVI).pack(fill = tk.X)
        tk.Button(self, text ="AAI", font = "none 12 bold", command = self.AAI).pack(fill = tk.X)
        tk.Button(self, text ="AAT", font = "none 12 bold", command = self.AAT).pack(fill = tk.X)
        tk.Button(self, text ="VVT", font = "none 12 bold", command = self.VVT).pack(fill = tk.X)
        tk.Button(self, text ="VVD", font = "none 12 bold", command = self.VVD).pack(fill = tk.X)
        tk.Button(self, text ="DOO", font = "none 12 bold", command = self.DOO).pack(fill = tk.X)
        tk.Button(self, text ="DDI", font = "none 12 bold", command = self.DDI).pack(fill = tk.X)
        tk.Button(self, text ="DDD", font = "none 12 bold", command = self.DDD).pack(fill = tk.X)
        tk.Button(self, text ="AOOR", font = "none 12 bold", command = self.AOOR).pack(fill = tk.X)
        tk.Button(self, text ="AAIR", font = "none 12 bold", command = self.AAIR).pack(fill = tk.X)
        tk.Button(self, text ="VOOR", font = "none 12 bold", command = self.VOOR).pack(fill = tk.X)
        tk.Button(self, text ="VVIR", font = "none 12 bold", command = self.VVIR).pack(fill = tk.X)
        tk.Button(self, text ="VDDR", font = "none 12 bold", command = self.VDDR).pack(fill = tk.X)
        tk.Button(self, text ="DOOR", font = "none 12 bold", command = self.DOOR).pack(fill = tk.X)
        tk.Button(self, text ="DDIR", font = "none 12 bold", command = self.DDIR).pack(fill = tk.X)
        tk.Button(self, text ="DDDR", font = "none 12 bold", command = self.DDDR).pack(fill = tk.X)
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO",command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)

    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")


'''
ALL THE MODE FRAMES
LOT OF REPETITION
SHOULD PUT IN ONE FUNCTION THOUGH
'''
class VOOFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: VOO", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["VOO"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))

        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")

class AOOFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: AOO", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["AOO"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")

class VIIFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: VVI", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["VVI"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")

class AAIFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: AAI", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["AAI"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")

class AATFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: AAT", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["AAT"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")


class VVTFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: VVT", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["VVT"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")


class VVDFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: VVD", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["VVD"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")


class DOOFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: DOO", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["DOO"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")

class DDIFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: DDI", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["DDI"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")

class DDDFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: DDD", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["DDD"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")

class AOORFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: AOOR", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["AOOR"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")

class AAIRFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: AAIR", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["AAIR"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")

class VOORFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: VOOR", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["VOOR"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")

class VVIRFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: VVIR", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["VVIR"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")

class VDDRFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: VDDR", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["VDDR"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")

class DOORFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: DOOR", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["DOOR"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")

class DDIRFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("800x800")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: DDIR", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["DDIR"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")

class DDDRFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.geometry("900x900")
        self.light = Light(master=self)
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Label(self, text="3K04 - Group - 12 - Heartscape", font="none 12 bold").pack()
        tk.Label(self, text="Pacing Mode: DDDR", font="Times 14").pack()
        menubar = tk.Menu(master = self)
        self.config(menu=menubar)
        
        #master.config(menu = menubar)
        
        Sub_File = tk.Menu(menubar)
        menubar.add_cascade(label = "File", menu = Sub_File)
        Sub_File.add_command(label = "Start Egram", command = self.start_egram)
        Sub_File.add_command(label = "About",command = self.About)
        #Sub_File.add_command(label = "Log-Out",command = self.logout)
        Sub_File.add_separator()
        Sub_File.add_command(label = "Exit", command = self.master.destroy)

        Sub_Mode = tk.Menu(menubar)
        menubar.add_cascade(label = "Mode", menu = Sub_Mode)
        Sub_Mode.add_command(label = "VOO", command = self.VOO)
        Sub_Mode.add_command(label = "AOO",command = self.AOO)
        Sub_Mode.add_command(label = "VVI",command = self.VVI)
        Sub_Mode.add_command(label = "AAI",command = self.AAI)
        Sub_Mode.add_command(label = "AAT",command = self.AAT)
        Sub_Mode.add_command(label = "VVT",command = self.VVT)
        Sub_Mode.add_command(label = "VVD",command = self.VVD)
        Sub_Mode.add_command(label = "DOO",command = self.DOO)
        Sub_Mode.add_command(label = "DDI",command = self.DDI)
        Sub_Mode.add_command(label = "DDD",command = self.DDD)
        Sub_Mode.add_command(label = "AOOR",command = self.AOOR)
        Sub_Mode.add_command(label = "AAIR",command = self.AAIR)
        Sub_Mode.add_command(label = "VOOR",command = self.VOOR)
        Sub_Mode.add_command(label = "VVIR",command = self.VVIR)
        Sub_Mode.add_command(label = "VDDR",command = self.VDDR)
        Sub_Mode.add_command(label = "DOOR",command = self.DOOR)
        Sub_Mode.add_command(label = "DDIR",command = self.DDIR)
        Sub_Mode.add_command(label = "DDDR",command = self.DDDR)



        relevant_params = p.params_by_pacing_mode["DDDR"]
        self.param_widgets = []
        for param_name in relevant_params:
            if isinstance(p.params[param_name], p.NumericParam):
                self.param_widgets.append(NumericParamFrame(p.params[param_name], name=param_name, master=self)) 
            else:
                self.param_widgets.append(NonNumericParamDropDown(p.params[param_name], name=param_name, master=self))
                           
        tk.Label(self, text=" ", font="none 12 bold").pack()
        tk.Button(self, text="Send Params", command=comms.update_pacemaker_params).pack()
            
    def About(self):
        tkinter.messagebox.showinfo('About', '3K04 Final Project\nMade by Group 12 - Heartscape\nJacob Luft\nPierre Tadrus\nRey Pastolero\nSean Stel\nShubham Shukla\nHamza Rahmani\nDevin Jhaveri\nAlex Hollebone')
    def start_egram(self):
        egram.EgramWin(master=self)
    def logout(self):
        self.master.withdraw()
        root.deiconify()
        login = LoginFrame(master=root)    
    def VOO(self):
        self.withdraw()
        winVOO = VOOFrame(master = root)
        winVOO.title("Mode: VOO")
    def AOO(self):
        self.withdraw()
        winAOO = AOOFrame(master = root)
        winAOO.title("Mode: AOO")
    def VVI(self):
        self.withdraw()
        winVII = VIIFrame(master = root)
        winVII.title("Mode: VII")
    def AAI(self):
        self.withdraw()
        winAII = AAIFrame(master = root)
        winAII.title("Mode: AAI")
    def AAT(self):
        self.withdraw()
        winAII = AATFrame(master = root)
        winAII.title("Mode: AAT")
    def VVT(self):
        self.withdraw()
        winAII = VVTFrame(master = root)
        winAII.title("Mode: VVT")
    def VVD(self):
        self.withdraw()
        winAII = VVDFrame(master = root)
        winAII.title("Mode: VVD")
    def DOO(self):
        self.withdraw()
        winAII = DOOFrame(master = root)
        winAII.title("Mode: DOO")
    def DDI(self):
        self.withdraw()
        winAII = DDIFrame(master = root)
        winAII.title("Mode: DDI")
    def DDD(self):
        self.withdraw()
        winAII = DDDFrame(master = root)
        winAII.title("Mode: DDD")
    def AOOR(self):
        self.withdraw()
        winAII = AOORFrame(master = root)
        winAII.title("Mode: AOOR")
    def AAIR(self):
        self.withdraw()
        winAII = AAIRFrame(master = root)
        winAII.title("Mode: AAIR")
    def VOOR(self):
        self.withdraw()
        winAII = VOORFrame(master = root)
        winAII.title("Mode: VOOR")
    def VVIR(self):
        self.withdraw()
        winAII = VVIRFrame(master = root)
        winAII.title("Mode: VVIR")
    def VDDR(self):
        self.withdraw()
        winAII = VDDRFrame(master = root)
        winAII.title("Mode: VDDR")
    def DOOR(self):
        self.withdraw()
        winAII = DOORFrame(master = root)
        winAII.title("Mode: DOOR")
    def DDIR(self):
        self.withdraw()
        winAII = DDIRFrame(master = root)
        winAII.title("Mode: DDIR")
    def DDDR(self):
        self.withdraw()
        winAII = DDDRFrame(master = root)
        winAII.title("Mode: DDDR")        

"""
Allows user to set numeric parameter values.
TODO:
    - Add horizontal padding to prevent changes in width.
    - Grey-out buttons when at edge of range
    - Add text entry box
    - Add units readout
"""

"""

Top Window which contains multiple frames.
TODO:
    - read data from view model and build GUI based on that
"""
if __name__ == "__main__":
    root = tk.Tk()

    # name and add the login frame to the root window
    login = LoginFrame(master=root)

    root.mainloop()
