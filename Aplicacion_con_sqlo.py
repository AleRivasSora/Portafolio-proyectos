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
        cursor.execute("SELECT Nombre From registro_productos")
        a = cursor.fetchall()
        i=0
        print(type(a))
        #print(rows)
        for fila in rows:
            datos_mostrar.insert("",END,text=a[i],values=rows[i])
            
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
        cursor.execute("SELECT Nombre From registro_productos ORDER BY Marca , Nombre")
        a = cursor.fetchall()
        i=0
        print(type(a))
        #print(rows)
        for fila in rows:
            
            datos_mostrar.insert("",END,text=a[i],values=rows[i])
            
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
            cursor.execute("SELECT Nombre From registro_productos ORDER BY Precio DESC")
            a = cursor.fetchall()
            i=0
            print(e)
            #print(rows)
            for fila in rows:
                
                datos_mostrar.insert("",END,text=a[i],values=rows[i])
                
                i +=1
            e+=1
            conn.close()
        else:
            cursor = conn.cursor()
            cursor.execute("SELECT Precio , Marca FROM registro_productos ORDER BY Precio")
            rows=cursor.fetchall()
            cursor.execute("SELECT Nombre From registro_productos ORDER BY Precio")
            a = cursor.fetchall()
            i=0
            print(e)
            #print(rows)
            for fila in rows:
                
                datos_mostrar.insert("",END,text=a[i],values=rows[i])
                
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
        cursor.execute("SELECT Nombre From registro_productos ORDER BY Nombre")
        a = cursor.fetchall()
        i=0
        print(type(a))
        #print(rows)
        for fila in rows:
            
            datos_mostrar.insert("",END,text=a[i],values=rows[i])
            
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
    activar_carrito.config(state=NORMAL)
    entry1.config(state=NORMAL)
    entry2.config(state=NORMAL)
    entry3.config(state=NORMAL)
    guardar.config(state=NORMAL)
    borrar.config(state=NORMAL)
    modificar.config(state=NORMAL)
    '''Deshabilita carrito de compras'''
    cancelar_compra.config(state=DISABLED)
    elegir_producto.config(state=DISABLED)
    productos.config(state=DISABLED)
    entry1_c.config(state=DISABLED)
    entry3_c.config(state=DISABLED)
    entry2_c.config(state=DISABLED)
    entry4_c.config(state=DISABLED)
    
    elegir_producto.config(state=DISABLED)
    añadir_carrito.config(state=DISABLED)
    comprar_c.config(state=DISABLED)
########################################################################################
############---Funciones Parte Clientes---##############################################
def habilitar_carrito():
    '''Deshabilita el frame de productos y modificar productos'''
    limpiar()
    limpiarM()
    activar_carrito.config(state=DISABLED)
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
    cancelar_compra.config(state=NORMAL)
    productos.config(state=NORMAL)
    elegir_producto.config(state=NORMAL)
    entry1_c.config(state=NORMAL)
    entry2_c.config(state=NORMAL)
    entry4_c.config(state=NORMAL)
    
    editar_producto.config(state=NORMAL)
    elegir_producto.config(state=NORMAL)
    añadir_carrito.config(state=NORMAL)
    comprar_c.config(state=NORMAL)

def limpiar_p():
    entry1_c.config(state=NORMAL)
    entry1_c.delete(0,END)
    entry2_c.config(state=NORMAL)
    entry2_c.delete(0,END)
    entry3_c.config(state=NORMAL)
    entry3_c.delete(0,END)
    entry3_c.config(state=DISABLED)
    entry4_c.delete(0,END)

def añadir_pantallaC():
    global dato_c
    dato_c = ""
    entry3_c.config(state=NORMAL)
    seleccionado = datos_mostrar.focus()
    dato_c = datos_mostrar.item(seleccionado)
    if dato_c != "":
        dato_a = dato_c["text"]
        dato_b = dato_c["values"]
        entry3_c.insert(0,dato_c["text"])
        entry3_c.config(state=DISABLED)

def vaciar_tablaC():
    fila = mostrar_carrito.get_children()
    for filas in fila:
        mostrar_carrito.delete(filas)

def actualizar_c():
    vaciar_tablaC()
    try:
        conn =sql.connect("archivos.db")
        a=0
        p=1
        cursor = conn.cursor()
        cursor.execute("SELECT Productos , Marca , Cantidad , Suma_total  FROM Carrito_compras")
        rows=cursor.fetchall()
        cursor.execute("SELECT SUM(Suma_total) FROM Carrito_compras")
        suma = cursor.fetchall()
        print(rows)
        print("\n",suma)
        for fila in rows:
            mostrar_carrito.insert("",END,text=p,values=(rows[a][0],rows[a][1],rows[a][2],rows[a][3]))
            a +=1
            p +=1
        mostrar_carrito.insert("",END,values=("","","",suma))
        conn.close()
    except sql.OperationalError:
        print("Error linea 327")

def añadir_carritoF():
    canti = int(entry4_c.get())
    try:
        if dato_c != "" or canti != 0:
            conexion=sql.connect("archivos.db")
            conexion.execute("insert into Carrito_compras (Productos,Marca,Cantidad,Suma_total) values (?,?,?,?)", (dato_c["text"],dato_c["values"][1],canti,dato_c["values"][0]*canti))
            conexion.commit()
            conexion.close()
            actualizar_c()
            limpiar_p()
        else:
            mensaje2 = tkinter.messagebox.showerror("Error","Elija el producta y cantidad")
    except sql.OperationalError:
        print("Error")

def cancelar_c():
    vaciar_tablaC()
    conn = sql.connect("archivos.db")
    cursor = conn.cursor()
    cursor.execute("Delete FROM Carrito_compras")
    conn.commit()
    conn.close()

def editar_c():
    seleccionado = mostrar_carrito.focus()
    dato = mostrar_carrito.item(seleccionado)
    print(dato["text"])
    try:
        conn = sql.connect("archivos.db")
        cursor = conn.cursor()
        cursor.execute(f"Delete FROM Carrito_compras Where Productos = '{dato['values'][0]}' ")
        conn.commit()
        conn.close()
        actualizar_c()
    except sql.OperationalError:
        print("Error linea 367")

def comprar():
    try:
        if entry1_c == "" or entry2_c == None:
            mensaje2 = tkinter.messagebox.showerror("Error","Coloque nombre y cedula")
        else:
            nom = entry1_c.get()
            nombre = nom.capitalize()
            cedula = entry2_c.get()
            compra = mostrar_carrito.get_children()
            productos = compra[0]
            conexion=sql.connect("archivos.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM clientes_registro")
            registro = cursor.fetchall()
            print("\n",compra,"\n",productos)
            for i in range(len(registro)):
                if cedula == registro[i][2]:
                    cursor.execute(f"INSER INTO registro_clintes ( Total_c, Historial ) VALUES ('{compra[4]+registro[i][3]}','{productos}') ")
                    conexion.commit()
                    conexion.close()
                    vaciar_tablaC()
                    limpiar_p()
                elif cedula != registro[i][2]:
                    cursor.execute(f"INSERT INTO clientes_registro (Nombre , Cedula , Total_c , Historial) VALUES ('{nombre}','{cedula}','{compra[4]}','{productos}')")
                    conexion.commit()
                    conexion.close()
                    vaciar_tablaC()
                    limpiar_p()
    except sql.OperationalError:
        print("error 396")
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

editar_producto = Button(frame4,text="Editar producto",bg="Light green",state=DISABLED,command=lambda:editar_c())
editar_producto.place(relx=0.55,rely=0.1,relheight=0.15,relwidth=0.3)
elegir_producto = Button(frame4,text="Añadir producto",bg="Light blue",state=DISABLED,command=lambda:añadir_pantallaC())
elegir_producto.place(relx=0.55,rely=0.3,relheight=0.15,relwidth=0.3)
añadir_carrito = Button(frame4,text="Añadir al\ncarrito",bg="Light blue",state=DISABLED,command=lambda:añadir_carritoF())
añadir_carrito.place(relx=0.55,rely=0.5,relheight=0.15,relwidth=0.3)
comprar_c = Button(frame4,text="Comprar",bg="Green",state=DISABLED,command=lambda:comprar())
comprar_c.place(relx=0.55,rely=0.7,relheight=0.15,relwidth=0.3)
cancelar_compra=Button(frame4,text="Cancelar",bg="Red",fg="White",state=DISABLED,command=lambda:cancelar_c())
cancelar_compra.place(relx=0.01,rely=0.8,relheight=0.15,relwidth=0.3)

frame5 = Frame(ventana)
frame5.place(relx=0.01,rely=0.56,relheight=0.5,relwidth=0.3)

mostrar_carrito = ttk.Treeview(frame5,columns=("col1","col2","coli3","coli4"))
mostrar_carrito.heading("#0",text="ID",anchor="center")
mostrar_carrito.heading("#1",text="Productos",anchor="center")
mostrar_carrito.heading("#2",text="Marca",anchor="center")
mostrar_carrito.heading("#3",text="Cantidad",anchor="center")
mostrar_carrito.heading("#4",text="Suma total",anchor="center")
mostrar_carrito.column("#0",width=10)
mostrar_carrito.column(0,width=100)
mostrar_carrito.column(1,width=70)
mostrar_carrito.column(2,width=70)
mostrar_carrito.column(3,width=70)
mostrar_carrito.pack_configure(fill= X)
mostrar_carrito['selectmode']='browse'

activar_carrito = Button(ventana,fg="White",font="arial",text="Carrito de\ncompras",height=2,width=15,bg="green",command=lambda:habilitar_carrito())
activar_carrito.place(x=880,y=120)

#añadir_pantallaC()



ventana.mainloop()