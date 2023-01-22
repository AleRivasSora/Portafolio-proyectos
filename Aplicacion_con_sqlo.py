from tkinter import ttk
import sqlite3 as sql
import numpy as np
import pandas as pd
import os
import tkinter.messagebox
from tkinter import *

def eliminar():
    seleccionado = datos_mostrar.focus()
    print(seleccionado)

    dato1 = datos_mostrar.item(seleccionado)
    eldato= dato1["text"]
    conn = sql.connect("archivos.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM registro_productos Where Nombre = '{}' ".format(eldato))
    conn.commit()
    conn.close()
    vaciar_tabla()
    conectarDB()
    
def conectarDB():
    conn = sql.connect("archivos.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Precio , Marca FROM registro_productos")
        rows=cursor.fetchall()
        cursor.execute("SELECT Id, Nombre From registro_productos")
        a = cursor.fetchall()
        i=0
        print(type(a))
        #print(rows)
        for fila in rows:
            
            datos_mostrar.insert("",END,text=a[i][1],values=rows[i])
            
            i +=1
            
        conn.close()    
    except sql.OperationalError:
        print("Error")

def ordenar_marca():
    vaciar_tabla()
    conn = sql.connect("archivos.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Precio , Marca FROM registro_productos ORDER BY Marca , Nombre")
        rows=cursor.fetchall()
        cursor.execute("SELECT Id, Nombre From registro_productos ORDER BY Marca , Nombre")
        a = cursor.fetchall()
        i=0
        print(type(a))
        #print(rows)
        for fila in rows:
            
            datos_mostrar.insert("",END,text=a[i][1],values=rows[i])
            
            i +=1
            
        conn.close()    
    except sql.OperationalError:
        print("Error")

e=1

def ordenar_precio():
    global e
    vaciar_tabla()
    conn = sql.connect("archivos.db")
    try:
        if e%2 == 0:
            cursor = conn.cursor()
            cursor.execute("SELECT Precio , Marca FROM registro_productos ORDER BY Precio DESC")
            rows=cursor.fetchall()
            cursor.execute("SELECT Id, Nombre From registro_productos ORDER BY Precio DESC")
            a = cursor.fetchall()
            i=0
            print(type(a))
            #print(rows)
            for fila in rows:
                
                datos_mostrar.insert("",END,text=a[i][1],values=rows[i])
                
                i +=1
                e+=1
            conn.close()
        else:
            cursor = conn.cursor()
            cursor.execute("SELECT Precio , Marca FROM registro_productos ORDER BY Precio")
            rows=cursor.fetchall()
            cursor.execute("SELECT Id, Nombre From registro_productos ORDER BY Precio")
            a = cursor.fetchall()
            i=0
            print(type(a))
            #print(rows)
            for fila in rows:
                
                datos_mostrar.insert("",END,text=a[i][1],values=rows[i])
                
                i +=1
                e +=1
    except sql.OperationalError:
        print("Error")

def ordenar_alfabetico():
    vaciar_tabla()
    conn = sql.connect("archivos.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Precio , Marca FROM registro_productos ORDER BY Nombre")
        rows=cursor.fetchall()
        cursor.execute("SELECT Id, Nombre From registro_productos ORDER BY Nombre")
        a = cursor.fetchall()
        i=0
        print(type(a))
        #print(rows)
        for fila in rows:
            
            datos_mostrar.insert("",END,text=a[i][1],values=rows[i])
            
            i +=1
            
        conn.close()    
    except sql.OperationalError:
        print("Error")

def update():
    n = entry4.get()
    p = int(entry5.get())
    m = entry6.get()
    dato1 = dato["text"]
    if n or m != "" or p !=None:
        try:
            conn = sql.connect("archivos.db")
            cursor = conn.cursor()
            cursor.execute(f"Update registro_productos SET Nombre = '{n}' , Precio = '{p}' , Marca = '{m}' WHERE Nombre = '{dato1}' ")
            conn.commit()
            conn.close()
            limpiarM()
            vaciar_tabla()
            conectarDB()
            guardar_modificado.config(state=DISABLED)
            entry4.config(state=DISABLED)
            entry5.config(state=DISABLED)
            entry6.config(state=DISABLED)
        except sql.OperationalError:
            print("error")
        except (ValueError,TypeError):
            print("error")
            error1 = tkinter.messagebox.showerror("Error","Valor invalido")
            
def cancelarM():
    limpiarM()
    entry1.config(state=NORMAL)
    entry2.config(state=NORMAL)
    entry3.config(state=NORMAL)

    guardar.config(state=NORMAL)
    borrar.config(state=NORMAL)
    modificar.config(state=NORMAL)

    cancelar_modificado.config(state=DISABLED)
    guardar_modificado.config(state=DISABLED)

    entry4.config(state=DISABLED)
    entry5.config(state=DISABLED)
    entry6.config(state=DISABLED)

def fmodificar():
    global dato
    seleccionado = datos_mostrar.focus()
    dato = datos_mostrar.item(seleccionado)
    if dato["text"] == "":
        mensaje1 = tkinter.messagebox.showerror("Error","Seleciona un producto")
    else:
        entry1.config(state=DISABLED)
        entry2.config(state=DISABLED)
        entry3.config(state=DISABLED)

        guardar.config(state=DISABLED)
        borrar.config(state=DISABLED)
        modificar.config(state=DISABLED)

        entry4.config(state=NORMAL)
        entry5.config(state=NORMAL)
        entry6.config(state=NORMAL)
        guardar_modificado.config(state=NORMAL)
        cancelar_modificado.config(state=NORMAL)
        entry4.insert(0,dato["text"])
        entry5.insert(0,dato["values"][0])
        entry6.insert(0,dato["values"][1])
        print(entry4.get())
        

def vaciar_tabla():
    fila = datos_mostrar.get_children()
    for filas in fila:
        datos_mostrar.delete(filas)

def limpiarM():
    entry4.delete(0,END)
    entry5.delete(0,END)
    entry6.delete(0,END)

def limpiar():
    entry1.delete(0,END)
    entry2.delete(0,END)
    entry3.delete(0,END)

def ingresar_datos():
    global i
    try:
        nom1 = str(nombre1.get())
        nom = nom1.capitalize()
        pre = float(precio1.get())
        marc1 = str(marca1.get())
        marc = marc1.capitalize()
        if nom and marc != "" or pre ==None:
            conexion=sql.connect("archivos.db")
            conexion.execute("insert into registro_productos(Nombre,Precio,Marca) values (?,?,?)", (nom,pre,marc))
            conexion.commit()
            conexion.close()
            vaciar_tabla()
            conectarDB()
            limpiar()
            print()
        else:
            mensaje2 = tkinter.messagebox.showerror("Error","Rellena los datos")
    except (ValueError,TypeError):
        print("error")
        error1 = tkinter.messagebox.showerror("Error","Valor invalido")
        limpiar()

i = 0
def habilitar_productos():
    '''HABILITA productos'''
    entry1.config(state=NORMAL)
    entry2.config(state=NORMAL)
    entry3.config(state=NORMAL)
    guardar.config(state=NORMAL)
    borrar.config(state=NORMAL)
    modificar.config(state=NORMAL)
    '''Deshabilita carrito de compras'''
    entry1_c.config(state=DISABLED)
    entry3_c.config(state=DISABLED)
    entry2_c.config(state=DISABLED)
    entry4_c.config(state=DISABLED)
    
    ingresa_c.config(state=DISABLED)
    añadir_carrito.config(state=DISABLED)
    comprar.config(state=DISABLED)
########################################################################################
############---Funciones Parte Clientes---##############################################
def habilitar_carrito():
    '''Deshabilita el frame de productos y modificar productos'''
    limpiar()
    limpiarM()
    entry1.config(state=DISABLED)
    entry2.config(state=DISABLED)
    entry3.config(state=DISABLED)
    guardar.config(state=DISABLED)
    borrar.config(state=DISABLED)
    modificar.config(state=DISABLED)

    cancelar_modificado.config(state=DISABLED)
    guardar_modificado.config(state=DISABLED)
    entry4.config(state=DISABLED)
    entry5.config(state=DISABLED)
    entry6.config(state=DISABLED)

    '''Habilita la parte de compras'''
    entry1_c.config(state=NORMAL)
    entry3_c.config(state=NORMAL)
    entry2_c.config(state=NORMAL)
    entry4_c.config(state=NORMAL)
    
    ingresa_c.config(state=NORMAL)
    añadir_carrito.config(state=NORMAL)
    comprar.config(state=NORMAL)

if __name__ == "__main__":

    ventana = Tk()
    ventana.attributes("-fullscreen",True)
    ventana.title("Negocio")

############################################
#Parte 1 del programa#######################

nombre1= StringVar()
precio1= StringVar()
marca1= StringVar()

frame = LabelFrame(ventana, text= "Introduzca Producto",pady=20,padx=20,font="Arial 20")
frame.place(relx=0.01,rely=0.01,relheight=0.2,relwidth=0.3)
frame2 = LabelFrame(ventana,pady=20,height=250,width=800).place(relx=0.01,rely=4)


etiqueta1 = Label(frame,text="Nombre").grid(row=0,column=1)
etiqueta2 = Label(frame,text="Precio").grid(row=2,column=1)
etiqueta3 = Label(frame,text="Marca").grid(row=4,column=1)

#Entradas
entry1 = Entry(frame,textvariable=nombre1)
entry1.grid(row=0,column= 2)
entry2 = Entry(frame,textvariable=precio1)
entry2.grid(row=2,column= 2)
entry3 = Entry(frame,textvariable=marca1)
entry3.grid(row=4,column= 2)


#botones
guardar = Button(frame,bg="Green", height=1, width=10, text="Guardar",command= lambda:ingresar_datos())
guardar.grid(row=8,column=2)
borrar = Button(frame,bg="Red",height=1,width=10,text="Eliminar", command= lambda:eliminar())
borrar.grid(row=8,column=3)
modificar = Button(frame,bg="Blue",height=1,width=10,text="Modificar",command= lambda:fmodificar())
modificar.grid(row=2,column=3)

#Treeview
datos_mostrar = ttk.Treeview(frame2,columns=("col1","col2"))
datos_mostrar.heading("#0",text="Nombre",anchor=CENTER)
datos_mostrar.heading("#1",text="Precio",anchor=CENTER)
datos_mostrar.heading("#2",text="Marca",anchor=CENTER)
#datos_mostrar.insert("",END,text="")
datos_mostrar.place(x=10,y=200)
datos_mostrar['selectmode']='browse'

etiqueta_ordenar = Label(frame2, text="Ordenar productos por\norden",font="Arial 12").place(x=630,y=200)
ordenar_datos1 = Button(frame2,text="Alfabetico",bg="Sky blue",command= lambda:ordenar_alfabetico())
ordenar_datos1.place(x=650,y=250)

ordenar_datos2 = Button(frame2,text="Precio",bg="Sky blue",command=lambda:ordenar_precio())
ordenar_datos2.place(x=650,y=300)

ordenar_datos3 = Button(frame2,text="Marca",bg="Sky blue",command=lambda:ordenar_marca())
ordenar_datos3.place(x=650,y=350)
#Scrollbarr del treeview############

barra1 = Scrollbar(frame2,orient=VERTICAL)
barra1.place(x=594,y=201,height=224)
barra1.config(command=datos_mostrar.yview)
datos_mostrar.config(yscrollcommand=barra1.set)


##########################################
#parte 2 ''modificar'' ###################
nombre_modificar = StringVar()
precio_modificar = StringVar()
marca_modificar = StringVar()
frame3 = LabelFrame(ventana, text= "Modificar datos de producto",pady=20,padx=20,font="Arial 18")
frame3.place(relx=0.35,rely=0.01,relheight=0.2,relwidth=0.25)
entry4 = Entry(frame3,textvariable=nombre_modificar,state=DISABLED)
entry5 = Entry(frame3,textvariable=precio_modificar,state=DISABLED)
entry6 = Entry(frame3,textvariable=marca_modificar,state=DISABLED)

entry4.grid(row=1,column=2)
entry5.grid(row=3,column=2)
entry6.grid(row=5,column=2)

etiqueta4 = Label(frame3,text="Nombre").grid(row=1,column=1)
etiqueta5 = Label(frame3,text="Precio").grid(row=3,column=1)
etiqueta6 = Label(frame3,text="Marca").grid(row=5,column=1)

guardar_modificado = Button(frame3,bg="Green",text="Guardar",height=1,width=10,command= lambda:update())
guardar_modificado.grid(row=7,column=1)
guardar_modificado.config(state=DISABLED)
cancelar_modificado = Button(frame3,bg="Red",text="Cancelar",height=1,width=10,command=lambda:cancelarM())
cancelar_modificado.grid(row=7,column=2)
cancelar_modificado.config(state=DISABLED)

'''Habilitar parte de productos'''
productos = Button(ventana,fg="White",text="Ingresar Productos",bg="green",height=2,width=15,font="arial",command=lambda:habilitar_productos())
productos.place(x=880,y=50)

conectarDB()

########################################################################################
############----Parte Clientes----#####################

frame4 = LabelFrame(ventana, text="Ingrese compra",font="Arial 20",labelanchor="n")
frame4.place(relx=0.33,rely=0.54,relheight=0.3,relwidth=0.3)

nombre_c = Label(frame4,text="Nombre del cliente").grid(row=0,column=0)
cedula_c = Label(frame4,text="Cedula").grid(row=2,column=0)
producto_c = Label(frame4,text="Producto").grid(row=4,column=0)
cantidad_c = Label(frame4,text="Cantidad").grid(row=6,column=0)

nombre_cliente = StringVar()
cedula_cliente = StringVar()
producto_cliente = StringVar()
cantidad_cliente = IntVar()

entry1_c = Entry(frame4,textvariable=nombre_cliente, state=DISABLED)
entry2_c = Entry(frame4,textvariable=cedula_cliente,state=DISABLED)
entry3_c = Entry(frame4,textvariable=producto_cliente,state=DISABLED)
entry4_c = Entry(frame4,textvariable=cantidad_cliente,state=DISABLED)
entry1_c.grid(row=1,column=0)
entry2_c.grid(row=3,column=0)
entry3_c.grid(row=5,column=0)
entry4_c.grid(row=7,column=0)

ingresa_c = Button(frame4,text="Ingresar Cliente",bg="Light green",state=DISABLED)
ingresa_c.place(relx=0.55,rely=0.1,relheight=0.15,relwidth=0.3)
añadir_carrito = Button(frame4,text="Añadir al\ncarrito",bg="Light blue",state=DISABLED)
añadir_carrito.place(relx=0.55,rely=0.5,relheight=0.15,relwidth=0.3)
comprar = Button(frame4,text="Comprar",bg="Green",state=DISABLED)
comprar.place(relx=0.55,rely=0.7,relheight=0.15,relwidth=0.3)

frame5 = Frame(ventana)
frame5.place(relx=0.01,rely=0.56,relheight=0.5,relwidth=0.3)

mostrar_carrito = ttk.Treeview(frame5,columns=("col1","col2","coli3"))
mostrar_carrito.heading("#0",text="ID",anchor="center")
mostrar_carrito.heading("#1",text="Productos",anchor=CENTER)
mostrar_carrito.heading("#2",text="Cantidad",anchor=CENTER)
mostrar_carrito.heading("#3",text="Suma total",anchor=CENTER)
mostrar_carrito.column("#0",width=20)
mostrar_carrito.column(0,width=120)
mostrar_carrito.column(1,width=80)
mostrar_carrito.column(2,width=80)
mostrar_carrito.pack_configure(fill= X)
mostrar_carrito['selectmode']='browse'

activar_carrito = Button(ventana,fg="White",font="arial",text="Carrito de\ncompras",height=2,width=15,bg="green",command=lambda:habilitar_carrito())
activar_carrito.place(x=880,y=120)





ventana.mainloop()
