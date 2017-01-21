from tkinter import *
from tkinter.ttk import *
import time

from main_canvas import MainCanvas
from broad_phase_collision_detection import BPCD
from sweep_and_prume import SAP


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
        self.BPCDthread = BPCD()
        self.SAPthread = SAP()
        self.BPCDthread.start()
        self.SAPthread.start()
        self.updateLabels()

    def createUpperFrame(self, w, h):
        style = Style()
        style.configure("BW.TLabel", foreground="black", background="#f8f8f8")
        style = Style().configure("C.TButton", font=('Arial Black', 12))
        upperFrame = Frame(self.root, width=w, height=h/6, style="BW.TLabel").pack()
        # ADD BUTTON
        self.addButton = Button(upperFrame, text="ADD", style="C.TButton")
        self.addButton.place(x=w/10*3, y=h/12, anchor="c")
        self.addButton.configure(command = lambda: self.setMode("ADD"))
        # REMOVE BUTTON
        self.removeButton = Button(upperFrame, text="Remove", style="C.TButton")
        self.removeButton.place(x=w/10, y=h/12, anchor="c")
        self.removeButton.configure(command = lambda: self.setMode("REMOVE"))
        # UPDATE BUTTON
        self.updateButton = Button(upperFrame, text="Update", style="C.TButton")
        self.updateButton.place(x=w/10*5, y=h/12, anchor="c")
        self.updateButton.configure(command = lambda: self.setMode("UPDATE"))
        # PLAY BUTTON
        playButton = Button(upperFrame, text="Play", style="C.TButton")
        playButton.place(x=w/10*7, y=h/12, anchor="c")
        playButton.configure(command = self.play)
        # STOP BUTTON
        stopButton = Button(upperFrame, text="Stop", style="C.TButton")
        stopButton.place(x=w/10*9, y=h/12, anchor="c")
        stopButton.configure(command = self.stop)


    def createCenterFrame(self, w, h):
        integerHeight = int(h/3*2)
        canvas = Canvas(self.root, bg='white', width=w, height=integerHeight)
        canvas.pack()
        self.mainCanvas = MainCanvas(canvas, w, integerHeight)

 
    def createLowerFrame(self, w, h):
        h = h / 100
        w = w / 6
        px = 100
        f = font=('Times New Roman', 12)
        lowerFrame = Frame(self.root).pack()
        # LABELS - Broad Phase Collision Detection
        lowerLeftFrame = LabelFrame(lowerFrame, text="Broad Phase Collision Detection")
        lowerLeftFrame.pack(side=LEFT, padx=px)
        self.BPCD_BoxesLabel = Label(lowerLeftFrame, text="Boxes: ", font=f)
        self.BPCD_BoxesLabel.pack(padx=0, pady=h)
        self.BPCD_CollisionsLabel = Label(lowerLeftFrame, text="Collisions: ", font=f)
        self.BPCD_CollisionsLabel.pack(padx=0, pady=h)
        self.BPCD_TimeLabel = Label(lowerLeftFrame, text="Time: ", font=f)
        self.BPCD_TimeLabel.pack(padx=0, pady=h)
        # LABELS - Sweep And Prune
        lowerRightFrame = LabelFrame(lowerFrame, text="Sweep And Prune")
        lowerRightFrame.pack(side=RIGHT, padx=px)
        self.SAP_BoxesLabel = Label(lowerRightFrame, text="Boxes: ", font=f)
        self.SAP_BoxesLabel.pack(padx=0, pady=h)
        self.SAP_CollisionsLabel = Label(lowerRightFrame, text="Collisions: ", font=f)
        self.SAP_CollisionsLabel.pack(padx=0, pady=h)
        self.SAP_TimeLabel = Label(lowerRightFrame, text="Time: ", font=f)
        self.SAP_TimeLabel.pack(padx=0, pady=h)
   
    def setMode(self, mode):
        self.mainCanvas.setMode(mode)

    def play(self):
        self.addButton.config(state = DISABLED)
        self.removeButton.config(state = DISABLED)
        self.updateButton.config(state = DISABLED)
        self.mainCanvas.setMode(None)
        self.mainCanvas.play()
        self.BPCDthread.startCounting(self.mainCanvas.rectangles)
        self.SAPthread.startCounting(self.mainCanvas.rectangles)
    
    def stop(self):
        self.addButton.config(state = NORMAL)
        self.removeButton.config(state = NORMAL)
        self.updateButton.config(state = NORMAL)
        self.mainCanvas.stop()
        self.BPCDthread.stopCounting()
        self.SAPthread.stopCounting()

    def updateLabels(self):
        boxes, collisions, time = self.BPCDthread.collisionInfo()
        self.BPCD_BoxesLabel['text'] = "Boxes: " + str(boxes)
        self.BPCD_CollisionsLabel['text'] = "Collisions: " + str(collisions)
        self.BPCD_TimeLabel['text'] = "Time: " + str(round(time, 5))
        boxes, collisions, time = self.SAPthread.collisionInfo()
        self.SAP_BoxesLabel['text'] = "Boxes: " + str(boxes)
        self.SAP_CollisionsLabel['text'] = "Collisions: " + str(collisions)
        self.SAP_TimeLabel['text'] = "Time: " + str(round(time, 5))
        self.root.after(500, self.updateLabels)

app = Application()
#app.mainloop()




