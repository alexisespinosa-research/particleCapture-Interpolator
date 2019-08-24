from tkinter import *
from tkinter import ttk

def calculate(*args):
    try:
        value=float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

def reset():
    meters.set(0,delete)
    feet.set(0,delete)
    

root = Tk()
root.title("Feet to meters")

mainframe=ttk.Frame(root,padding="3 3 12 12")
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)

feet=StringVar()
meters=StringVar()

feet_entry=ttk.Entry(mainframe,width=7,textvariable=feet)
feet_entry.grid(row=1,column=2,sticky=(W,E))
ttk.Label(mainframe,text="feet").grid(row=1,column=3,sticky=W)

ttk.Label(mainframe,text="is equivalent to:").grid(row=2,column=1,sticky=E)
ttk.Label(mainframe,textvariable=meters).grid(row=2,column=2,sticky=(W,E))
ttk.Label(mainframe,text="meters").grid(row=2,column=3,sticky=W)

ttk.Button(mainframe,text="Calculate",command=calculate).grid(row=3,column=3,sticky=W)

ttk.Button(mainframe,text="Reset",command=reset).grid(row=4,column=3,sticky=W)
for child in mainframe.winfo_children(): child.grid_configure(padx=5,pady=5)

feet_entry.focus()

root.bind('<Return>',calculate)



root.mainloop()

