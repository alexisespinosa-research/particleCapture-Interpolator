import tkinter as tk

root = tk.Tk()


class Principal(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.foo = tk.StringVar()
        self.nac = {}
        self.ent = {}

        self.ent["test"] = tk.Entry(root, width=20, background='white', textvariable=self.foo, state='disabled')
        self.ent["test"].pack()

        self.ent["image"] = tk.Entry(root, width=20, background='white', textvariable=self.foo, state='disabled')
        self.ent["image"].pack()

        self.nac["test"] = tk.IntVar()
        self.ck1 = tk.Checkbutton(root, text='test', variable=self.nac["test"], command=self.naccheck("test"))
        self.ck1.pack()

        self.nac["image"] = tk.IntVar()
        self.ck1 = tk.Checkbutton(root, text='image', variable=self.nac["image"], command=self.naccheck("image"))
        self.ck1.pack()


    def naccheck(self,item):
        print ("check "+item)
        print (self.nac[item].get())
        if self.nac[item].get() == 0:
            self.ent[item].configure(state='disabled')
        else:
            self.ent[item].configure(state='normal')

app = Principal()
root.mainloop()
