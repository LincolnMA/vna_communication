import customtkinter as CTK
from tkinter import filedialog as fd

CTK.set_appearance_mode("System")  # Modes: system (default), light, dark
CTK.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class myEntry(CTK.CTkFrame):
    def __init__(self,master,label):
        super().__init__(master)
        self.title = CTK.CTkLabel(self,text=label)
        self.entry = CTK.CTkEntry(self,placeholder_text=label)

        self.title.grid(column = 0, row = 0)
        self.entry.grid(column = 0, row = 1)

    def grid(self, column,row):
        super().grid(column = column, row = row)

def pos(l):
    for i in range(len(l)):
        for j in range(len(l[i])):
            l[i][j].grid(column = j,row = i)

app = CTK.CTk()  # create CTk window like you do with the Tk window

#Sweep Frame Section vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
sweepFrame = CTK.CTkFrame(app)
sweepFrameTitle = CTK.CTkLabel(sweepFrame,text="Sweep",fg_color="gray30", corner_radius=6)


sFreqEntry = myEntry(sweepFrame, "Start Frequency")
eFreqEntry = myEntry(sweepFrame, "End Frequency")

numOfPointsEntry = myEntry(sweepFrame, "Number of Points")
mppEntry = myEntry(sweepFrame, "Measure Per Points")

startSweepButton = CTK.CTkButton(sweepFrame)

#Calibration Section vvvvvvvvvvvvvvvvvvvvvvvvvvvv

fd.askdirectory()

calibrationFrame = CTK.CTkFrame(app)

calibrateButton = CTK.CTkButton(calibrationFrame, text= "Calibrate")

#use tkinter askforfile
loadCalibButton = CTK.CTkButton(calibrationFrame, text="Load Calib")

#use tkinter askfordirectory
saveCalibButton = CTK.CTkButton(calibrationFrame,text = "Save Calib")

#Pasta das medidas vvvvvvvvvvvvvvv

#botao para escolher pasta para salvar medidas
saveMeasuresButton = CTK.CTkButton(app, text = "Save Measures")

app.mainloop()



