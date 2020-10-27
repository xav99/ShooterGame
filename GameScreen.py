import tkinter as tk
from tkinter import *
import os
#import hashlib
#from tkinter import messagebox

class Mainframe(tk.Tk):
    """
    Defines which frame is the main frame
    """

    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = Home(self)
        self.frame.pack()

    def change(self, frame):
        self.frame.pack_forget()  # delete current frame
        self.frame = frame(self)
        self.frame.pack()  # make new frame


class Home(tk.Frame):
    """
    Application home screen
    """

    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        master.title("Main application")
        master.geometry("400x200")

        # pulldown menu initiation
        self.menubar = Menu(self)
        master.config(menu=self.menubar)

        # Pulldown menu file
        fileMenu = Menu(self.menubar, tearoff=0)
        fileMenu.add_command(label="Log out", command=lambda: self.changeFrame(Home))
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=exit)
        self.menubar.add_cascade(label="File", menu=fileMenu)

        # Pulldown menu settings
        settingsMenu = Menu(self.menubar, tearoff=0)
        settingsMenu.add_command(label="Change password", command=lambda: self.changeFrame(Home))
        settingsMenu.add_command(label="Other", command=0)
        self.menubar.add_cascade(label="Settings", menu=settingsMenu)

        # Buttons
        self.btnWeaponEquip = self.newButton("   Weapon Equip   ", posx=90, posy=10, font="Ariel 16", command=lambda: None)
        self.btnShop = self.newButton("   Shop   ", posx=90, posy=70, font="Ariel 16", command=lambda: None)
        self.btnPlay = self.newButton("   Play   ", posx=90, posy=130, font="Ariel 16", command=lambda: self.changeFrame(GamemodeSelection))
        self.btnHelp = self.newButton("   Help   ", posx=320, posy=15, font="Ariel 12",  command=lambda: None) # controlls gamemodes etc

    def newButton(self, text=None, visible=True, posx=None, posy=None, font="ariel 12", command=None):
        """
        :param text: Specify text the button displays
        :param visible: Specify whether the button should be visible
        :param posx: Specify x position
        :param posy: Specify y position
        :param font: Specify font
        :param command: Specify a command the button carries out when pressed
        :return: Returns the button object
        Create a button
        """
        btn = tk.Button(self.master, text=text, font=font, command=command)
        if visible:
            btn.place(x=posx, y=posy)
        return btn

    def newLabel(self, text=None, visible=True, posx=None, posy=None, font="ariel 12", textvar=None):
        """
        :param text: Specify text the label displays
        :param visible: Specify whether the label should be visible
        :param posx: Specify x position
        :param posy: Specify y position
        :param font: Specify font
        :return: Returns the label object
        Create a label
        """
        lbl = tk.Label(self.master, text=text, font=font, textvariable=textvar)
        if visible:
            lbl.place(x=posx, y=posy)
        return lbl

    def changeFrame(self, frame):
        """
        :param frame: Specify frame to change to
        Change the frame
        """
        for widget in self.master.winfo_children():
            widget.destroy()
        self.master.change(frame)


class GamemodeSelection(Home):
    """
    Application home screen
    """

    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        master.title("Main application")
        master.geometry("400x200")

        # pulldown menu initiation
        self.menubar = Menu(self)
        master.config(menu=self.menubar)

        # Pulldown menu file
        fileMenu = Menu(self.menubar, tearoff=0)
        fileMenu.add_command(label="Log out", command=lambda: self.changeFrame(Home))
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=exit)
        self.menubar.add_cascade(label="File", menu=fileMenu)

        # Pulldown menu settings
        settingsMenu = Menu(self.menubar, tearoff=0)
        settingsMenu.add_command(label="Change password", command=lambda: self.changeFrame(Home))
        settingsMenu.add_command(label="Other", command=0)
        self.menubar.add_cascade(label="Settings", menu=settingsMenu)

        # Buttons
        self.btnLevelMode = self.newButton("   Level Mode   ", posx=100, posy=10, font="Ariel 14", command=lambda: os.system('start main.py'))
        self.btnTimeMode = self.newButton("   Time Mode   ", posx=100, posy=70, font="Ariel 14", command=lambda: None)
        self.btnSurvivalMode = self.newButton("   Survival Mode   ", posx=100, posy=130, font="Ariel 14",  command=lambda: None)
        self.btnBack = self.newButton("   Back   ", posx=5, posy=135, font="Ariel 12", command=lambda: self.changeFrame(Home))


if __name__ == "__main__":
    app = Mainframe()
    app.mainloop()