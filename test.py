from tkinter import *

root = Tk()
texto1 = Label(text = "ingresa un dato")
texto1.grid(row = 0, column = 1)

panel1 = Entry(root)
panel1.grid(row = 0, column = 1)

def ejecutar():
 varstr = Label(text = panel1.get())
 var = str(varstr)
 print(var)

btn = Button(root, text = "tomar dato", command=ejecutar)
btn.grid(row = 2, column = 1)

LF = LabelFrame(root, text = "Output")
LF.grid(row = 3, column = 1)

root.mainloop()