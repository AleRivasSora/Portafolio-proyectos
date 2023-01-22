from tkinter import *

def ventana1():


    Button(ventana1, text="ir a ventana2", width=20, command=ventana2).place(relx=0.5, rely=0.5)

    ventana1.mainloop()

def ventana2():
    global ventana2
    ventana2 = Toplevel(ventana1) #crear una ventana siguiente de la ventana1
    ventana2.geometry("500x500")
    ventana2.title("ventana2")
    a = Toplevel()
    Button(ventana2, text="volver a ventana1", width=20, command=volver_ventana).place(relx=0.5, rely=0.5)
    
    if(ventana2):
        ventana1.withdraw()

    ventana2.mainloop()

def volver_ventana():
    ventana1.iconify()
    ventana1.deiconify()
    ventana2.destroy()

ventana1()
