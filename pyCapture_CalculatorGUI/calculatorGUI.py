"""
=================
This is the Graphical User Interface: "calculatorGUI.py"
It uses the python function for estimates of capture efficiency by direct interception:
pyCaptureDB.captureEfficiencyDI

This tool has been provided as additional material of the journal paper:
Espinosa-Gayosso A., Ghisalberti M., Shimeta J. & Ivey G.N. "On predicting particle capture rates in aquatic systems"
Submited to PLOSOne on September2020.
=================

For examples on how to use the function, check the scripts "basicUse.py" and "totalBiomassOptimisation_Fig10.py"

"""

#Import needed dependencies
import tkinter as tk
from tkinter import *
from tkinter import ttk

#Identifying the path of this script in order to load pyCapture
import os
scriptPath = os.getcwd()

#Defining the path to add to python in order to recognize the pyCapture package:
pyCapturePath=scriptPath + '/../../pyCaptureDev' #Definition as relative path to this script
#pyCapturePath='/Users/esp025/Dropbox/BiologicalPaper/Python/pyCaptureDev' #Definition as absolute path in your own compute

#Loading modules from the pyCapture package
import sys
sys.path.append(pyCapturePath)
from pyCapture import pyCaptureDB

#Defining formats and default values
floatOutFormat='10.3E'
waterDensityDefault='998.2' #[kg/m3] @ 20C
waterViscosityDefault='1.002E-3' #[(N s)/m2] @ 20C

def calculate(*args):
    try:

        #unit variables Section calculations
        if unitSec.get() == 1:
            Uh=float(upstreamVelocity.get())
            Dch=float(collectorDiameter.get())
            rhoh=float(fluidDensity.get())
            muh=float(fluidViscosity.get())
            Dph=float(particleDiameter.get())
            Reynolds.set(format(Uh*Dch*rhoh/muh,floatOutFormat))
            particleSizeRatio.set(format(Dph/Dch,floatOutFormat))

        #dimensionLess Section calculations  
        Reh=float(Reynolds.get())
        rph=float(particleSizeRatio.get())
        (rpArr,ReyArr,etaArr)=pyCaptureDB.captureEfficiencyDI(rp=rph,Rey=Reh)
        etah=etaArr[0]
        captureEfficiency.set(format(etah,floatOutFormat))


        #dynamic Section calculations    
        if dynamicSec.get() == 1:
            hh=float(collectorHeight.get())           
            Cph=float(particleConcentration.get())
            Fph=Cph*Uh*hh*Dch
            CRh=etah*Fph
            particleFlux.set(format(Fph,floatOutFormat))
            particleCaptureRate.set(format(CRh,floatOutFormat))
    except ValueError:
        pass

def reset():
    Reynolds.set('')
    captureEfficiency.set('')
    particleSizeRatio.set('')
    upstreamVelocity.set('')
    collectorDiameter.set('')
    particleDiameter.set('')
    fluidDensity.set(waterDensityDefault)
    fluidViscosity.set(waterViscosityDefault)

def unitActive(*args):
    try:
        if unitSec.get() == 1:
            upstreamVelocity_entry.config({"state":'normal',"background": normalBG})
            collectorDiameter_entry.config({"state":'normal',"background": normalBG})
            particleDiameter_entry.config({"state":'normal',"background": normalBG})
            fluidDensity_entry.config({"state":'normal',"background": normalBG})
            fluidViscosity_entry.config({"state":'normal',"background": normalBG})
        else:
            upstreamVelocity_entry.config({"state":'disabled',"background": disabledBG})
            collectorDiameter_entry.config({"state":'disabled',"background": disabledBG})
            particleDiameter_entry.config({"state":'disabled',"background": disabledBG})
            fluidDensity_entry.config({"state":'disabled',"background": disabledBG})
            fluidViscosity_entry.config({"state":'disabled',"background": disabledBG})
    except ValueError:
        pass

def dynamicActive(*args):
    try:
        if dynamicSec.get() == 1:
            unitSec.set(value=1)
            unitActive()
            collectorHeight_entry.config({"state":'normal',"background": normalBG})
            particleConcentration_entry.config({"state":'normal',"background": normalBG})
            particleFlux_label.config({"background": answerBG,"foreground": answerFG})
            particleFlux_entry.config({"state":'disabled',"disabledbackground": answerBG,"disabledforeground": answerFG})
            particleCaptureRate_label.config({"background": answerBG,"foreground": answerFG})
            particleCaptureRate_entry.config({"state":'disabled',"disabledbackground": answerBG,"disabledforeground": answerFG})
        else:
            collectorHeight_entry.config({"state":'disabled',"background": disabledBG})
            particleConcentration_entry.config({"state":'disabled',"background": disabledBG})
            particleFlux_label.config({"background": disabledBG,"foreground": disabledFG})
            particleFlux_entry.config({"state":'disabled',"disabledbackground": disabledBG,"disabledforeground": disabledFG})
            particleCaptureRate_label.config({"background": disabledBG,"foreground": disabledFG})
            particleCaptureRate_entry.config({"state":'disabled',"disabledbackground": disabledBG,"disabledforeground": disabledFG})
    except ValueError:
        pass
    
#Style choices
    #Background colors
titleBG='lightgreen'
instructionsBG='red'
normalBG='white'
disabledBG='grey90'
#answerBG='lemon chiffon'
answerBG='yellow'
    #Foreground colors
normalFG='black'
disabledFG='gray60'
answerFG='black'
    #Widths
messageWidth=400
    #Fonts
#titleFont='Helvetica 16 bold'
titleFont='Helvetica 0 bold'
#instructionsFont='Courier 16 bold'
instructionsFont='Courier 0 bold'


#The root, mainframe and title
root = Tk()
root.title("Particle Capture Estimator")

mainframe=ttk.Frame(root,padding="3 3 12 12")
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)

#Variables to use
captureEfficiency=StringVar()
Reynolds=StringVar()
particleSizeRatio=StringVar()
radioDLess=StringVar()
unitSec=IntVar()
upstreamVelocity=StringVar()
collectorDiameter=StringVar()
particleDiameter=StringVar()
fluidDensity=StringVar(value=waterDensityDefault)
fluidViscosity=StringVar(value=waterViscosityDefault)
dynamicSec=IntVar()
collectorHeight=StringVar()
particleConcentration=StringVar()
particleFlux=StringVar()
particleCaptureRate=StringVar()

#Counter for the row for ease the script
rowWindow=0

#Internal title row
rowWindow+=1
reTitle_text=Message(mainframe,text=root.title())
#reTitle_text.configure(font=titleFont,width=messageWidth,bg=titleBG)
reTitle_text.configure(width=messageWidth,bg=titleBG)
reTitle_text.grid(row=rowWindow,column=1,columnspan=2)

#First Instructions row
rowWindow+=1
instructions1_text=Message(mainframe,text="Fill in the parameters: Reynolds number and Particle Size Ratio. Then click the \"Calculate\" button.")
instructions1_text.configure(width=messageWidth,bg=instructionsBG)
instructions1_text.grid(row=rowWindow,column=1,columnspan=2)

#Settings for the "Reynolds" row
rowWindow+=1
Reynolds_label=ttk.Label(mainframe,text="Reynolds Number [-]. Valid range: (0,1000]")
Reynolds_label.grid(row=rowWindow,column=1,sticky=W)
Reynolds_entry=tk.Entry(mainframe,width=16,textvariable=Reynolds,background=normalBG,state='normal')
Reynolds_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "particleSizeRatio" row
rowWindow+=1
particleSizeRatio_label=ttk.Label(mainframe,text="Particle Size Ratio [-]. Valid range: [0,1.5]")
particleSizeRatio_label.grid(row=rowWindow,column=1,sticky=W)
particleSizeRatio_entry=tk.Entry(mainframe,width=16,textvariable=particleSizeRatio,background=normalBG,state='normal')
particleSizeRatio_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "captureEfficiency" row
rowWindow+=1
captureEfficiency_label=tk.Label(mainframe,text="Capture Efficiency [-]",background=answerBG,foreground=answerFG)
captureEfficiency_label.grid(row=rowWindow,column=1,sticky=W)
captureEfficiency_entry=tk.Entry(mainframe,width=16,textvariable=captureEfficiency,disabledforeground=answerFG,disabledbackground=answerBG,state='disabled')
captureEfficiency_entry.grid(row=rowWindow,column=2,sticky=W)

#Buttons row
rowWindow+=1
reset_button=ttk.Button(mainframe,text="Reset",command=reset)
reset_button.grid(row=rowWindow,column=1,sticky=N)

calc_button=ttk.Button(mainframe,text="Calculate",command=calculate)
calc_button.grid(row=rowWindow,column=2,sticky=N)

#Second Instructions row
rowWindow+=1
instructions2_text=Message(mainframe,text="To use dimensional variables, activate the check button. Enter all the dimensional variables below. Then click the \"Calculate\" button.")
instructions2_text.configure(width=messageWidth,bg=instructionsBG)
instructions2_text.grid(row=rowWindow,column=1,columnspan=2)

#Unit parameters check button row
rowWindow+=1
unit_check=ttk.Checkbutton(mainframe,variable=unitSec,text="Use dimensional variables to estimate parameters", command=unitActive)
unit_check.grid(row=rowWindow,column=1,columnspan=2,sticky=N)

#Settings for the "upstreamVelocity" row
rowWindow+=1
upstreamVelocity_label=ttk.Label(mainframe,text="Upstream Velocity [m/s]")
upstreamVelocity_label.grid(row=rowWindow,column=1,sticky=W)
upstreamVelocity_entry=tk.Entry(mainframe,width=16,textvariable=upstreamVelocity,disabledforeground=disabledFG,disabledbackground=disabledBG,state='disabled')
upstreamVelocity_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "collectorDiameter" row
rowWindow+=1
collectorDiameter_label=ttk.Label(mainframe,text="Collector Diameter [m]")
collectorDiameter_label.grid(row=rowWindow,column=1,sticky=W)
collectorDiameter_entry=tk.Entry(mainframe,width=16,textvariable=collectorDiameter,disabledforeground=disabledFG,disabledbackground=disabledBG,state='disabled')
collectorDiameter_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "particleDiameter" row
rowWindow+=1
particleDiameter_label=ttk.Label(mainframe,text="Particle Diameter [m]")
particleDiameter_label.grid(row=rowWindow,column=1,sticky=W)
particleDiameter_entry=tk.Entry(mainframe,width=16,textvariable=particleDiameter,disabledforeground=disabledFG,disabledbackground=disabledBG,state='disabled')
particleDiameter_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "fluidDensity" row
rowWindow+=1
fluidDensity_label=ttk.Label(mainframe,text="Fluid Density [kg/m\u00B3]")
fluidDensity_label.grid(row=rowWindow,column=1,sticky=W)
fluidDensity_entry=tk.Entry(mainframe,width=16,textvariable=fluidDensity,disabledforeground=disabledFG,disabledbackground=disabledBG,state='disabled')
fluidDensity_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "fluidViscosity" row
rowWindow+=1
fluidViscosity_label=ttk.Label(mainframe,text="Fluid Viscosity [(N s)/m\u00B2]")
fluidViscosity_label.grid(row=rowWindow,column=1,sticky=W)
fluidViscosity_entry=tk.Entry(mainframe,width=16,textvariable=fluidViscosity,disabledforeground=disabledFG,disabledbackground=disabledBG,state='disabled')
fluidViscosity_entry.grid(row=rowWindow,column=2,sticky=W)

#Third Instructions row
rowWindow+=1
instructions3_text=Message(mainframe,text="To estimate dynamic rates, activate the check button. Fill all the dimensional variables above and the Collector Height and Particle concentration below. Then click the \"Calculate\" button.")
instructions3_text.configure(width=messageWidth,bg=instructionsBG)
instructions3_text.grid(row=rowWindow,column=1,columnspan=2)

#Dynamic rates check button row
rowWindow+=1
dynamic_check=ttk.Checkbutton(mainframe,variable=dynamicSec,text="Estimate dynamic rates", command=dynamicActive)
dynamic_check.grid(row=rowWindow,column=1,columnspan=2,sticky=N)

#Settings for the "collectorHeight" row
rowWindow+=1
collectorHeight_label=ttk.Label(mainframe,text="Collector Height [m]")
collectorHeight_label.grid(row=rowWindow,column=1,sticky=W)
collectorHeight_entry=tk.Entry(mainframe,width=16,textvariable=collectorHeight,disabledforeground=disabledFG,disabledbackground=disabledBG,state='disabled')
collectorHeight_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "particleConcentration" row
rowWindow+=1
particleConcentration_label=ttk.Label(mainframe,text="Particle Concentration [particles/m\u00B3]")
particleConcentration_label.grid(row=rowWindow,column=1,sticky=W)
particleConcentration_entry=tk.Entry(mainframe,width=16,textvariable=particleConcentration,disabledforeground=disabledFG,disabledbackground=disabledBG,state='disabled')
particleConcentration_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "particleFlux" row
rowWindow+=1
particleFlux_label=tk.Label(mainframe,text="Particle Flux [particles/s] (approaching)",fg=disabledFG,bg=disabledBG)
particleFlux_label.grid(row=rowWindow,column=1,sticky=W)
particleFlux_entry=tk.Entry(mainframe,width=16,textvariable=particleFlux,disabledforeground=disabledFG,disabledbackground=disabledBG,state='disabled')
particleFlux_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "particleCaptureRate" row
rowWindow+=1
particleCaptureRate_label=tk.Label(mainframe,text="Particle Capture Rate [particles/s]",fg=disabledFG,bg=disabledBG)
particleCaptureRate_label.grid(row=rowWindow,column=1,sticky=W)
particleCaptureRate_entry=tk.Entry(mainframe,width=16,textvariable=particleCaptureRate,disabledforeground=disabledFG,disabledbackground=disabledBG,state='disabled')
particleCaptureRate_entry.grid(row=rowWindow,column=2,sticky=W)

#Pretty stuff
for child in mainframe.winfo_children(): child.grid_configure(padx=5,pady=5)

#Startup
Reynolds_entry.focus()
#captureEfficiency_radio.invoke()
#unit_check.invoke()

#Key actions
root.bind('<Return>',calculate)

#Run the tool
root.mainloop()

