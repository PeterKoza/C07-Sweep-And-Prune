from tkinter import *
from tkinter.ttk import *

from main_canvas import MainCanvas

class Application(Frame):
    def __init__(self):
        w = 750
        h = 550
        self.root = Tk()
        self.createUpperFrame(w, h)
        separator = Frame(self.root, height=2, relief=SUNKEN).pack(fill=X, padx=5, pady=5)
        self.createCenterFrame(w, h)
        separator = Frame(self.root, height=2, relief=SUNKEN).pack(fill=X, padx=5, pady=5)
        self.createLowerFrame(w, h)
        self.root.resizable(width=False, height=False)


    def createUpperFrame(self, w, h):
        style = Style()
        style.configure("BW.TLabel", foreground="black", background="#f8f8f8")
        style = Style().configure("C.TButton", font=('Arial Black', 12))
        self.upperFrame = Frame(self.root, width=w, height=h/6, style="BW.TLabel").pack()
        # ADD BUTTON
        addButton = Button(self.upperFrame, text="ADD", style="C.TButton")
        addButton.place(x=w/10*3, y=h/12, anchor="c")
        addButton.configure(command = lambda: self.setMode("ADD"))
        # REMOVE BUTTON
        removeButton = Button(self.upperFrame, text="Remove", style="C.TButton")
        removeButton.place(x=w/10, y=h/12, anchor="c")
        removeButton.configure(command = lambda: self.setMode("REMOVE"))
        # UPDATE BUTTON
        updateButton = Button(self.upperFrame, text="Update", style="C.TButton")
        updateButton.place(x=w/10*5, y=h/12, anchor="c")
        updateButton.configure(command = lambda: self.setMode("UPDATE"))
        # PLAY BUTTON
        playButton = Button(self.upperFrame, text="Play", style="C.TButton")
        playButton.place(x=w/10*7, y=h/12, anchor="c")
        playButton.configure(command = self.play)
        # STOP BUTTON
        stopButton = Button(self.upperFrame, text="Stop", style="C.TButton")
        stopButton.place(x=w/10*9, y=h/12, anchor="c")
        stopButton.configure(command = self.stop)


    def createCenterFrame(self, w, h):
        canvas = Canvas(self.root, bg='white', width=w, height=h/3*2)
        canvas.pack()
        self.mainCanvas = MainCanvas(canvas, w, h/3*2)

 
    def createLowerFrame(self, w, h):
        h = h / 100
        w = w / 6
        px = 25
        f = font=('Times New Roman', 12)
        lowerFrame = Frame(self.root).pack()
        # LABELS - Broad Phase Collision Detection
        lowerLeftFrame = LabelFrame(lowerFrame, text="Broad Phase Collision Detection")
        lowerLeftFrame.pack(side=LEFT, padx=px)
        self.BPCD_BoxesLabel = Label(lowerLeftFrame, text="Boxes: ", font=f).pack(padx=w, pady=h)
        self.BPCD_CollisionsLabel = Label(lowerLeftFrame, text="Collisions: ", font=f).pack(padx=w, pady=h)
        self.BPCD_TimeLabel = Label(lowerLeftFrame, text="Time: ", font=f).pack(padx=w, pady=h)
        # LABELS - Sweep And Prune
        lowerRightFrame = LabelFrame(lowerFrame, text="Sweep And Prune")
        lowerRightFrame.pack(side=RIGHT, padx=px)
        self.SAP_BoxesLabel = Label(lowerRightFrame, text="Boxes: ", font=f).pack(padx=w, pady=h)
        self.SAP_CollisionsLabel = Label(lowerRightFrame, text="Collisions: ", font=f).pack(padx=w, pady=h)
        self.SAP_TimeLabel = Label(lowerRightFrame, text="Time: ", font=f).pack(padx=w, pady=h)

   
    def setMode(self, mode):
        self.mainCanvas.setMode(mode)

    def play(self):
        self.mainCanvas.play()

    def stop(self):
        self.mainCanvas.stop()

app = Application()
#app.mainloop()


