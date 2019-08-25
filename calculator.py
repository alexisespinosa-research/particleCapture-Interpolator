from tkinter import *
from tkinter import ttk

def calculate(*args):
    try:
        if check.get() == "meters":
            value=float(feet.get())
            meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
        elif check.get() == "feet":
            value=float(meters.get())
            feet.set((value / 0.3048 * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

def reset():
    meters.set('')
    feet.set('')
    
#The root, mainframe and title
root = Tk()
root.title("Feet to meters")

mainframe=ttk.Frame(root,padding="3 3 12 12")
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)

#Variables to use
feet=StringVar()
meters=StringVar()
check=StringVar()

#Settings for the "feet" row
feet_entry=ttk.Entry(mainframe,width=16,textvariable=feet)
feet_entry.grid(row=1,column=1,sticky=E)
feet_radio=ttk.Radiobutton(mainframe,variable=check,value="feet",text="feet")
feet_radio.grid(row=1,column=2,sticky=W)

#Settings for the "meters" row
meters_entry=ttk.Entry(mainframe,width=16,textvariable=meters)
meters_entry.grid(row=2,column=1,sticky=E)
meters_radio=ttk.Radiobutton(mainframe,variable=check,value="meters",text="meters")
meters_radio.grid(row=2,column=2,sticky=W)

#Buttons
calc_button=ttk.Button(mainframe,text="Calculate",command=calculate)
calc_button.grid(row=3,column=2,sticky=W)

reset_button=ttk.Button(mainframe,text="Reset",command=reset)
reset_button.grid(row=4,column=2,sticky=W)

#Pretty stuff
for child in mainframe.winfo_children(): child.grid_configure(padx=5,pady=5)

#Startup
feet_entry.focus()
meters_radio.focus()

#Key actions
root.bind('<Return>',calculate)

#Run the tool
root.mainloop()

