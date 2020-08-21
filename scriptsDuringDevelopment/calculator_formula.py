from tkinter import *
from tkinter import ttk

def calculateNumbers(*args):
    try:

        #unit variables Section calculations
        if unitSec.get() == 1:
            Uh=float(velocity.get())
            Dch=float(collectorDiameter.get())
            rhoh=float(fluidDensity.get())
            muh=float(fluidViscosity.get())
            Dph=float(particleDiameter.get())
            Reynolds.set(Uh*Dch*rhoh/muh)
            particleSizeRatio.set(Dph/Dch)

        #dimensionLess Section calculations  
        if radioDLess.get() == "captureEfficiency":
            Reh=float(Reynolds.get())
            rph=float(particleSizeRatio.get())
            etah=0.224*(Reh**0.718)*(rph**2.08)
            captureEfficiency.set(etah)
        elif radioDLess.get() == "Reynolds":
            etah=float(captureEfficiency.get())
            rph=float(particleSizeRatio.get())
            Reh=(etah/(0.224*(rph**2.08)))**(1.0/0.718)
            Reynolds.set(Reh)
        elif radioDLess.get() == "particleSizeRatio":
            etah=float(captureEfficiency.get())
            Reh=float(Reynolds.get())
            rph=(etah/(0.224*(Reh**0.718)))**(1.0/2.08)
            particleSizeRatio.set(rph)

        #dynamic Section calculations    
        if dynamicSec.get() == 1:
            hh=float(collectorHeight.get())           
            Cph=float(particleConcentration.get())
            Fph=Cph*Uh*hh*Dch
            CRh=etah*Fph
            particleFlux.set(Fph)
            particleCaptureRate.set(CRh)
    except ValueError:
        pass

def reset():
    Reynolds.set('')
    captureEfficiency.set('')
    particleSizeRatio.set('')

def unitActive(*args):
    try:
        if unitSec.get() == 1:
            velocity_entry.config({"state":'normal',"background": activeBG})
            collectorDiameter_entry.config({"state":'normal',"background": activeBG})
            particleDiameter_entry.config({"state":'normal',"background": activeBG})
            fluidDensity_entry.config({"state":'normal',"background": activeBG})
            fluidViscosity_entry.config({"state":'normal',"background": activeBG})
        else:
            velocity_entry.config({"state":'disabled',"background": disabledBG})
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
            collectorHeight_entry.config({"state":'normal',"background": activeBG})
            particleConcentration_entry.config({"state":'normal',"background": activeBG})
            particleFlux_entry.config({"state":'normal',"background": activeBG})
            particleCaptureRate_entry.config({"state":'normal',"background": activeBG})
        else:
            collectorHeight_entry.config({"state":'disabled',"background": disabledBG})
            particleConcentration_entry.config({"state":'disabled',"background": disabledBG})
            particleFlux_entry.config({"state":'disabled',"background": disabledBG})
            particleCaptureRate_entry.config({"state":'disabled',"background": disabledBG})
    except ValueError:
        pass
    
#Style choices
mainBG='lightBlue'
instBG='red'
activeBG='blue'
disabledBG='red'
messageWidth=400


#The root, mainframe and title
root = Tk()
root.title("Particle Capture Parameter Estimator")
root.configure(bg=mainBG)

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
velocity=StringVar()
collectorDiameter=StringVar()
particleDiameter=StringVar()
fluidDensity=StringVar(value="1000")
fluidViscosity=StringVar(value="0.001")
dynamicSec=IntVar()
collectorHeight=StringVar()
particleConcentration=StringVar()
particleFlux=StringVar()
particleCaptureRate=StringVar()

#Counter for the row for ease the script
rowWindow=0

#Internal title row
rowWindow+=1
reTitle_text=Message(mainframe,text='Particle Capture Parameter Estimator')
reTitle_text.configure(font='Helvetica 18 bold',width=messageWidth,bg=mainBG)
reTitle_text.grid(row=rowWindow,column=1,columnspan=2)

#First Instructions row
rowWindow+=1
instructions1_text=Message(mainframe,text="Choose the parameter to estimate and fill in the rest. Then type enter (or click the \"calculate\" button)")
instructions1_text.configure(font='Courier 16',width=messageWidth,bg=instBG)
instructions1_text.grid(row=rowWindow,column=1,columnspan=2)

#Settings for the "captureEfficiency" row
rowWindow+=1
captureEfficiency_radio=ttk.Radiobutton(mainframe,variable=radioDLess,value="captureEfficiency",text="captureEfficiency")
captureEfficiency_radio.grid(row=rowWindow,column=1,sticky=W)
captureEfficiency_entry=ttk.Entry(mainframe,width=16,textvariable=captureEfficiency,background=activeBG)
captureEfficiency_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "Reynolds" row
rowWindow+=1
Reynolds_radio=ttk.Radiobutton(mainframe,variable=radioDLess,value="Reynolds",text="Reynolds")
Reynolds_radio.grid(row=rowWindow,column=1,sticky=W)
Reynolds_entry=ttk.Entry(mainframe,width=16,textvariable=Reynolds,background=activeBG)
Reynolds_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "particleSizeRatio" row
rowWindow+=1
particleSizeRatio_radio=ttk.Radiobutton(mainframe,variable=radioDLess,value="particleSizeRatio",text="particleSizeRatio")
particleSizeRatio_radio.grid(row=rowWindow,column=1,sticky=W)
particleSizeRatio_entry=ttk.Entry(mainframe,width=16,textvariable=particleSizeRatio,background=activeBG,state='normal')
particleSizeRatio_entry.grid(row=rowWindow,column=2,sticky=W)

#Buttons row
rowWindow+=1
reset_button=ttk.Button(mainframe,text="Reset",command=reset)
reset_button.grid(row=rowWindow,column=1,sticky=N)

calc_button=ttk.Button(mainframe,text="Calculate",command=calculateNumbers)
calc_button.grid(row=rowWindow,column=2,sticky=N)

#Second Instructions row
rowWindow+=1
instructions2_text=Message(mainframe,text="If you want to work with dimensional variables, activate the check button")
instructions2_text.configure(font='Courier 16',width=messageWidth,bg=instBG)
instructions2_text.grid(row=rowWindow,column=1,columnspan=2)

#Unit parameters check button row
rowWindow+=1
unit_check=ttk.Checkbutton(mainframe,variable=unitSec,text="Activate dimensional variables", command=unitActive)
unit_check.grid(row=rowWindow,column=1,columnspan=2,sticky=N)

#Settings for the "Velocity" row
rowWindow+=1
velocity_label=ttk.Label(mainframe,text="Upstream Velocity [m/s]")
velocity_label.grid(row=rowWindow,column=1,sticky=W)
velocity_entry=ttk.Entry(mainframe,width=16,textvariable=velocity,background=activeBG,state='disabled')
velocity_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "collectorDiameter" row
rowWindow+=1
collectorDiameter_label=ttk.Label(mainframe,text="Collector Diameter [m]")
collectorDiameter_label.grid(row=rowWindow,column=1,sticky=W)
collectorDiameter_entry=ttk.Entry(mainframe,width=16,textvariable=collectorDiameter,background=activeBG,state='disabled')
collectorDiameter_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "particleDiameter" row
rowWindow+=1
particleDiameter_label=ttk.Label(mainframe,text="Particle Diameter [m]")
particleDiameter_label.grid(row=rowWindow,column=1,sticky=W)
particleDiameter_entry=ttk.Entry(mainframe,width=16,textvariable=particleDiameter,background=activeBG,state='disabled')
particleDiameter_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "fluidDensity" row
rowWindow+=1
fluidDensity_label=ttk.Label(mainframe,text="Fluid Density [kg/m3]")
fluidDensity_label.grid(row=rowWindow,column=1,sticky=W)
fluidDensity_entry=ttk.Entry(mainframe,width=16,textvariable=fluidDensity,background=activeBG,state='disabled')
fluidDensity_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "fluidViscosity" row
rowWindow+=1
fluidViscosity_label=ttk.Label(mainframe,text="Fluid Viscosity [(N s)/m2]")
fluidViscosity_label.grid(row=rowWindow,column=1,sticky=W)
fluidViscosity_entry=ttk.Entry(mainframe,width=16,textvariable=fluidViscosity,background=activeBG,state='disabled')
fluidViscosity_entry.grid(row=rowWindow,column=2,sticky=W)

#Third Instructions row
rowWindow+=1
instructions3_text=Message(mainframe,text="If you want to estimate dynamic rates, activate the check button")
instructions3_text.configure(font='Courier 16',width=messageWidth,bg=instBG)
instructions3_text.grid(row=rowWindow,column=1,columnspan=2)

#Dynamic rates check button row
rowWindow+=1
dynamic_check=ttk.Checkbutton(mainframe,variable=dynamicSec,text="Activate dinamic rates", command=dynamicActive)
dynamic_check.grid(row=rowWindow,column=1,columnspan=2,sticky=N)

#Settings for the "collectorHeight" row
rowWindow+=1
collectorHeight_label=ttk.Label(mainframe,text="Collector Height [m]")
collectorHeight_label.grid(row=rowWindow,column=1,sticky=W)
collectorHeight_entry=ttk.Entry(mainframe,width=16,textvariable=collectorHeight,background=activeBG,state='disabled')
collectorHeight_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "particleConcentration" row
rowWindow+=1
particleConcentration_label=ttk.Label(mainframe,text="Particle Concentration [particles/m3]")
particleConcentration_label.grid(row=rowWindow,column=1,sticky=W)
particleConcentration_entry=ttk.Entry(mainframe,width=16,textvariable=particleConcentration,background=activeBG,state='disabled')
particleConcentration_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "particleFlux" row
rowWindow+=1
particleFlux_label=ttk.Label(mainframe,text="Particle Flux [particles/s] (approaching)")
particleFlux_label.grid(row=rowWindow,column=1,sticky=W)
particleFlux_entry=ttk.Entry(mainframe,width=16,textvariable=particleFlux,background=activeBG,state='disabled')
particleFlux_entry.grid(row=rowWindow,column=2,sticky=W)

#Settings for the "particleCaptureRate" row
rowWindow+=1
particleCaptureRate_label=ttk.Label(mainframe,text="Particle Capture Rate [particles/s]")
particleCaptureRate_label.grid(row=rowWindow,column=1,sticky=W)
particleCaptureRate_entry=ttk.Entry(mainframe,width=16,textvariable=particleCaptureRate,background=activeBG,state='disabled')
particleCaptureRate_entry.grid(row=rowWindow,column=2,sticky=W)

#Pretty stuff
for child in mainframe.winfo_children(): child.grid_configure(padx=5,pady=5)

#Startup
Reynolds_entry.focus()
captureEfficiency_radio.invoke()
#unit_check.invoke()

#Key actions
root.bind('<Return>',calculateNumbers)

#Run the tool
root.mainloop()

