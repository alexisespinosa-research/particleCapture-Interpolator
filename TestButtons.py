import tkinter as tk

root = tk.Tk()


class Principal(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.foo = tk.StringVar()
        self.nac = tk.IntVar()

        self.ck1 = tk.Checkbutton(root, text='test',
            variable=self.nac, command=self.naccheck)
        self.ck1.pack()

        self.ent1 = tk.Entry(root, width=20, background='blue',
            textvariable=self.foo, state='disabled')
        self.ent1.pack()

    def naccheck(self):
        print ("check")
        if self.nac.get() == 0:
            self.ent1.configure(state='disabled')
        else:
            self.ent1.configure(state='normal')

app = Principal()
root.mainloop()
