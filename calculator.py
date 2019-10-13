from tkinter import *
from tkinter import ttk

def calculate(*args):
    try:
        if check.get() == "captureEfficiency":
            Reh=float(Reynolds.get())
            rph=float(particleSizeRatio.get())
            captureEfficiency.set((0.5*Reh**0.5*rph**0.7))
        elif check.get() == "Reynolds":
            etah=float(captureEfficiency.get())
            rph=float(particleSizeRatio.get())
            Reynolds.set((etah/(0.5*rph**0.7))**(1.0/0.5))
        elif check.get() == "particleSizeRatio":
            etah=float(captureEfficiency.get())
            Reh=float(Reynolds.get())
            particleSizeRatio.set((etah/(0.5*Reh**0.5))**(1.0/0.7))
    except ValueError:
        pass

def reset():
    Reynolds.set('')
    captureEfficiency.set('')
    
#The root, mainframe and title
root = Tk()
root.title("Particle Capture Parameter Estimator")

mainframe=ttk.Frame(root,padding="3 3 12 12")
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)

#Variables to use
captureEfficiency=StringVar()
Reynolds=StringVar()
particleSizeRatio=StringVar()
check=StringVar()

#Settings for the "captureEfficiency" row
captureEfficiency_entry=ttk.Entry(mainframe,width=16,textvariable=captureEfficiency)
captureEfficiency_entry.grid(row=1,column=1,sticky=E)
captureEfficiency_radio=ttk.Radiobutton(mainframe,variable=check,value="captureEfficiency",text="captureEfficiency")
captureEfficiency_radio.grid(row=1,column=2,sticky=W)

#Settings for the "Reynolds" row
Reynolds_entry=ttk.Entry(mainframe,width=16,textvariable=Reynolds)
Reynolds_entry.grid(row=2,column=1,sticky=E)
Reynolds_radio=ttk.Radiobutton(mainframe,variable=check,value="Reynolds",text="Reynolds")
Reynolds_radio.grid(row=2,column=2,sticky=W)

#Settings for the "particleSizeRatio" row
particleSizeRatio_entry=ttk.Entry(mainframe,width=16,textvariable=particleSizeRatio)
particleSizeRatio_entry.grid(row=3,column=1,sticky=E)
particleSizeRatio_radio=ttk.Radiobutton(mainframe,variable=check,value="particleSizeRatio",text="particleSizeRatio")
particleSizeRatio_radio.grid(row=3,column=2,sticky=W)

#Buttons
calc_button=ttk.Button(mainframe,text="Calculate",command=calculate)
calc_button.grid(row=4,column=2,sticky=W)

reset_button=ttk.Button(mainframe,text="Reset",command=reset)
reset_button.grid(row=5,column=2,sticky=W)

#Pretty stuff
for child in mainframe.winfo_children(): child.grid_configure(padx=5,pady=5)

#Startup
Reynolds_entry.focus()
captureEfficiency_radio.invoke()

#Key actions
root.bind('<Return>',calculate)

#Run the tool
root.mainloop()

