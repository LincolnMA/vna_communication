import tkinter as tk

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
import serial
import serial.tools.list_ports
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.ticker import EngFormatter

SPAD = 4
MPAD = 8
LPAD = 16


class UI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.controlPannel = ctk.CTkFrame(self)
        self.infoPannel = ctk.CTkScrollableFrame(self)
        self.chartPannel = ctk.CTkFrame(self)

        pannelPadding = 8
        self.controlPannel.pack(
            side="left", padx=pannelPadding, pady=pannelPadding, fill='y')

        self.infoPannel.pack(side="left", padx=pannelPadding,
                             pady=pannelPadding, fill='y', ipadx=MPAD)
        self.chartPannel.pack(side="left", padx=pannelPadding,
                              pady=pannelPadding, fill='both', expand=True)

        # Parte de controle
        self.sweepControl = SweepControl(self.controlPannel)
        callibration = CalibControl(self.controlPannel)
        self.serialControl = SerialControl(self.controlPannel)
        # Parte de info
        self.markersInfo = Marker(self.infoPannel, "Marker 1", data)
        self.markersInfo = Marker(self.infoPannel, "Marker 2", data)

        # Parte de grafico

        xs = np.logspace(1,-9,100)
        prng = np.random.RandomState(19680801)
        S11grafico = Chart(self.chartPannel, "S11", xdata=xs, ydata=(0.8 + 0.4 * prng.uniform(size=100)) * np.log10(xs)**2)

        S21grafico  = Chart(self.chartPannel, "S11", xdata=xs, ydata=(0.8 + 0.4 * prng.uniform(size=100)) * np.log10(xs)**2)
        S11polar = Chart(self.chartPannel,"S11 Polar", xdata=xs, ydata=xs, projection='polar')

        S11polar.grid(column = 0, row = 0,padx = MPAD,pady = MPAD)
        S11grafico.grid(column = 1, row = 0)
        S21grafico.grid(column = 0, row = 1)
        

        self.attributes('-zoomed', True)

        self.mainloop()


class SerialControl(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent",
                         border_color="gray30", border_width=1)
        self.pack(fill='x', expand=True, pady=MPAD, anchor='s')

        title = ctk.CTkLabel(self, text="Serial Control",
                             fg_color="gray30", corner_radius=6)
        title.grid(column=0, row=0, sticky="nw", pady=MPAD, padx=MPAD)

        selectPortLabel = ctk.CTkLabel(self, text="Porta Serial: ")
        selectPortLabel.grid(column=0, row=1, padx=MPAD)

        self.selectedPort = ctk.StringVar(value=None)
        self.selectPort = ctk.CTkComboBox(
            self, values=self.getPortsAvailable(), variable=self.selectedPort)

        self.selectPort.grid(column=1, row=1)

        connectBtn = ctk.CTkButton(self, text="Conectar ao VNA")
        connectBtn.grid(column=0, row=2, columnspan=10, pady=MPAD)

    def connect(self): return True

    def getPortsAvailable(self) -> list:
        return ['PORTA1', ' PORTA2']

class CalibControl(ctk.CTkFrame):
    
    def __init__(self,master):
        super().__init__(master, fg_color="transparent",
                         border_color="gray30", border_width=1)
        

        title = ctk.CTkLabel(self, text="Calibbration",
                             fg_color="gray30", corner_radius=6)
        title.grid(column=0, row=0, sticky="nw", pady=MPAD, padx=MPAD)
        self.pack(fill='both', expand=True)



        loadBtn = ctk.CTkButton(self,text="Load")
        addBtn = ctk.CTkButton(self,text="Add Callibration")

        addBtn.grid(column = 0, row = 1, pady = SPAD)
        loadBtn.grid(column = 0, row = 2, pady = SPAD, padx = SPAD)

class SweepControl(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent", border_width=1)
        self.pack(fill='both', expand=True)

        title = ctk.CTkLabel(self, text="Sweep Control",
                             fg_color="gray30", corner_radius=6)
        title.grid(column=0, row=0, sticky="nw", pady=MPAD, padx=MPAD)

        # Parametros do sweep
        sweepParam = ctk.CTkFrame(self, fg_color='transparent')
        self.sweepStart = ctk.StringVar(self)
        self.sweepStop = ctk.StringVar(self)

        sweepStartEntry = ctk.CTkEntry(
            sweepParam, textvariable=self.sweepStart)
        sweepStopEntry = ctk.CTkEntry(sweepParam, textvariable=self.sweepStop)

        startLabel = ctk.CTkLabel(sweepParam, text="Sweep Start")
        stopLabel = ctk.CTkLabel(sweepParam, text="Sweep Stop")

        startLabel.grid(column=0, row=0, padx=SPAD)
        sweepStartEntry.grid(column=1, row=0, pady=SPAD)

        stopLabel.grid(column=0, row=1)
        sweepStopEntry.grid(column=1, row=1)

        #
        progressBar = ctk.CTkProgressBar(self)
        progressBar.set(39/100)
        progresspct = ctk.CTkLabel(self, text="39%")
        #
        sweepBtn = ctk.CTkButton(self, text="sweep")

        sweepParam.grid(column=0, row=1, padx=SPAD)
        progressBar.grid(column=0, row=2, pady=LPAD)
        progresspct.grid(column=1, row=2, padx=MPAD)
        sweepBtn.grid(column=0, row=3)

    def configSweep(): pass


data = {
    'Frequency': '13 Hz',
    'Impedance': '132.1321 Ohmns',
    'Parallel R': '333.320 mOhms',
    'Parralel X': '10 Ohms',
    'L equiv.': '5402 H',
    'C equiv.': '1 uF',
    'Return loss': '3db',
    'VSWR': '310',
    'Q': None,
    'S21': complex(30, 3),
    'S11 Phase': '10°',
    'S11': complex(1, 323),
}


class Marker(ctk.CTkFrame):

    def __init__(self, master, name, data):
        super().__init__(master)
        title = ctk.CTkLabel(self, text=name)
        title.grid(column=0, row=0)

        rowc = 1

        for k in data.keys():
            label = ctk.CTkLabel(self, text=k + ":")
            value = ctk.CTkLabel(self, text=data[k])

            label.grid(padx=SPAD, row=rowc, column=0, sticky="NW")
            value.grid(row=rowc, column=1, sticky="NW", padx=LPAD)

            rowc += 1

        self.pack(pady=MPAD)


class Chart(ctk.CTkFrame):
    def __init__(self, master, title, xdata, ydata, projection = None):
        super().__init__(master)

        # The x data span over several decades to demonstrate several SI prefixes.
        px = 1/plt.rcParams['figure.dpi']
        fig = Figure(figsize=(400*px, 300*px))
        self.t = np.arange(0, 3, .01)

        ax = fig.add_subplot(projection=projection)

        ax.set_ylabel("time [s]")
        ax.set_xlabel("f(t)")
        ax.set_title(title)

        formatter0 = EngFormatter(unit='Hz')
        ax.xaxis.set_major_formatter(formatter0)
        ax.set_yscale('log')

        self.line, = ax.plot(xdata, ydata)
        self.canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        self.canvas.draw()

        toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        toolbar.update()

        self.canvas.mpl_connect("key_press_event", key_press_handler)

        self.canvas.mpl_connect('scroll_event', lambda event: print(event))

        self.canvas.get_tk_widget().grid(column=0, row=1)
        toolbar.grid(column=0, row=0)



ui = UI()
