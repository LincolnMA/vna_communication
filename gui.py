import nanovna as vna
import driver_lib

import customtkinter as CTK
from tkinter import filedialog as fd

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from matplotlib.figure import Figure
import numpy as np

import json

# Api do sistema vvvvvv
liteVna = None


#driver = driver_lib.positioner()



CTK.set_appearance_mode("System")  # Modes: system (default), light, dark
CTK.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


#GUI CONFIG
save_dir = './'

#GUI constants
SP = 4 #small pad
MP = 8 #medium pad
GP = 16 #big pad


class myEntry(CTK.CTkFrame):
    def __init__(self,master,label):
        super().__init__(master, fg_color="transparent")
        self.title = CTK.CTkLabel(self,text=label)
        self.entry = CTK.CTkEntry(self,placeholder_text=label)

        self.title.grid(column = 0, row = 0)
        self.entry.grid(column = 0, row = 1, padx = MP, pady = MP)

    def set(self, text):
        self.entry.insert(index=0, string=text)

    def get(self):
        return self.entry.get()

    def grid(self, column,row):
        super().grid(column = column, row = row)
class myButton(CTK.CTkButton):
    def __init__(self, master, text, command = None):
        super().__init__(master, text=text, command=command)
    def grid(self, column, row):
        super().grid(column = column, row = row, pady = MP, padx = MP)

class myCombo(CTK.CTkFrame):
    def __init__(self, master, label, options):
        super().__init__(master, fg_color="transparent")
        self.title = CTK.CTkLabel(self, text = label)
        self.combobox = CTK.CTkComboBox(self, values = options)

        self.title.grid(column = 0, row = 0)
        self.combobox.grid(column = 1, row = 0)

    def get(self):
        return self.combobox.get()

class plot():
    def __init__(self, master, data):
        self.plotFrame = CTK.CTkFrame(master)
        self.plotFrame.grid(column = 1, row = 0)

        fig = Figure(figsize=(5, 4), dpi=100)
        #t = np.arange(0, 3, .01)
        ax = fig.add_subplot()
        line, = ax.plot(data[0], data[1])
        ax.set_xlabel("time [s]")
        ax.set_ylabel("f(t)")

        canvas = FigureCanvasTkAgg(fig, master=self.plotFrame)  # A tk.DrawingArea.
        canvas.draw()

        # pack_toolbar=False will make it easier to use a layout manager later on.
        toolbar = NavigationToolbar2Tk(canvas, self.plotFrame, pack_toolbar=False)
        toolbar.update()

        button_quit = CTK.CTkButton(master=self.plotFrame, text="Quit", command=self.plotFrame.destroy)


        # Packing order is important. Widgets are processed sequentially and if there
        # is no space left, because the window is too small, they are not displayed.
        # The canvas is rather flexible in its size, so we pack it last which makes
        # sure the UI controls are displayed as long as possible.
        button_quit.pack(side=CTK.BOTTOM)

        toolbar.pack(side=CTK.BOTTOM, fill=CTK.X)
        canvas.get_tk_widget().pack(side=CTK.TOP, fill=CTK.BOTH, expand=True)



app = CTK.CTk()  # create CTk window like you do with the Tk window

#sweep, calibration, save read, config, etc ...
tools = CTK.CTkFrame(app)
display = CTK.CTkFrame(app)

tools.grid(column = 0, row = 0, sticky=CTK.N, padx = 16)
display.grid(column = 1, row = 0)


sweepFrame = CTK.CTkFrame(tools)

calibrationFrame = CTK.CTkFrame(tools)

ReadFrame = CTK.CTkFrame(tools)

configFrame = CTK.CTkFrame(tools)

configFrame.grid(column = 0, row = 3, pady = MP, ipadx = SP,ipady = SP)
#Sweep Frame Section vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

sFreqEntry = myEntry(sweepFrame, "Start Frequency")
eFreqEntry = myEntry(sweepFrame, "End Frequency")

numOfPointsEntry = myEntry(sweepFrame, "Number of Points")
mppEntry = myEntry(sweepFrame, "Measure Per Points")

startSweepButton = CTK.CTkButton(sweepFrame)


sFreqEntry.grid(0,0)
eFreqEntry.grid(1,0)

numOfPointsEntry.grid(0,1)
mppEntry.grid(1,1)

sweepFrame.grid(column = 0, row = 0)

#Calibration Section vvvvvvvvvvvvvvvvvvvvvvvvvvvv
def loadCalib():
    
    calib_file = fd.askopenfilename()
    #usar funcao load calib

def calib():
    save_name = fd.asksaveasfilename()
    
    sfreq = None
    efreq = None
    n_points = None
    mpp = None
    n_passos = None
    #tem que zerar o frame sempre antes pra apagar a mensagem de erro anterior
    for child in display.winfo_children():
        child.destroy()
    try:
        sfreq = int(sFreqEntry.get())

        efreq = int(eFreqEntry.get())

        n_points = int(numOfPointsEntry.get())
        mpp = int(mppEntry.get())
        
        n_passos = int(n_passosEntry.get())
    except:
        CTK.CTkLabel(display, text="SWEEP INVALIDO", font=CTK.CTkFont(size=40)).pack()
        return

    liteVna.calibration(sfreq,efreq, n_points,mpp)
    liteVna.save_calib(f"{save_name}/{save_name[save_name.rfind('/')+1:]}")

def saveCalib():
    filename = fd.asksaveasfilename()
    #usar função salvar vna



calibrateButton = CTK.CTkButton(calibrationFrame, text= "Calibrate", command=calib)

#use tkinter askforfile
loadCalibButton = CTK.CTkButton(calibrationFrame, text="Load Calib", command=loadCalib)

#use tkinter askfordirectory
saveCalibButton = CTK.CTkButton(calibrationFrame,text = "Save Calib", command=saveCalib)

#Pasta das medidas vvvvvvvvvvvvvvv

calibrateButton.grid(column = 0, row = 0, pady = 8)
loadCalibButton.grid(column =  0, row = 1, pady = 8)
saveCalibButton.grid(column = 0, row = 2, pady = 8)

calibrationFrame.grid(column = 0, row = 1, pady = 16,sticky=CTK.W)


#read 
def read():
    save_name = fd.asksaveasfilename()
    print("save file name: ",save_name)
    
    sfreq = None
    efreq = None
    n_points = None
    mpp = None
    n_passos = None
    #tem que zerar o frame sempre antes pra apagar a mensagem de erro anterior
    for child in display.winfo_children():
        child.destroy()
    try:
        sfreq = int(sFreqEntry.get())

        efreq = int(eFreqEntry.get())

        n_points = int(numOfPointsEntry.get())
        mpp = int(mppEntry.get())
        
        n_passos = int(n_passosEntry.get())
    except:
        CTK.CTkLabel(display, text="SWEEP INVALIDO", font=CTK.CTkFont(size=40)).pack()
        return
    liteVna.measure(sfreq,efreq,n_points,mpp)
    #lite.calibrate_S11()

    f,real = liteVna.extract_S11_RAW()

    plt = None 
    for i in range(n_passos):
        vna.save2s1p(["Hz","S","RI","R 50"],[f, real],f"{save_name}/{save_name[save_name.rfind('/')+1:]}_{i}")
        plt = plot(display, [f,real])


    
readButton = myButton(ReadFrame, text = "Read", command=read)

#passos
n_passosEntry = myEntry(ReadFrame, "numero de passos")


readButton.grid(column = 1, row = 0)
n_passosEntry.grid(column=0,row = 0)

ReadFrame.grid(column = 0, row = 2)


#frame config

valid_ports = vna.get_ports()

vna_port = myCombo(configFrame, "Porta VNA", valid_ports)
pos_driver_port = myCombo(configFrame, "porta Posicionador", valid_ports)

def connect():
    global liteVna 
    liteVna = vna.Nvna(baudrate=2e6, port_name=f'/dev/{vna_port.get()}')



b_connect = CTK.CTkButton(configFrame, text="Conectar", command=connect)


vna_port.grid(column = 0,row = 0)

b_connect.grid(column = 1,row = 0)

pos_driver_port.grid(column = 0,row = 1)



#algumas configurações



def on_close():
    last_save = {
        "sfreq": sFreqEntry.get(),
        "efreq": eFreqEntry.get(),
        "n_points": numOfPointsEntry.get(),
        "mpp" : mppEntry.get(),
        "n_steps": n_passosEntry.get() 
    }

    f = open('config.json', 'w')
    json_data = json.dump(last_save, f)

    app.destroy()
f = open('config.json', 'r')
last_data = json.load(f)
f.close()

sFreqEntry.set(last_data['sfreq'])
eFreqEntry.set(last_data['efreq'])
numOfPointsEntry.set(last_data['n_points'])
mppEntry.set(last_data['mpp'])
n_passosEntry.set(last_data['n_steps'])





app.protocol('WM_DELETE_WINDOW', on_close)
app.mainloop()



