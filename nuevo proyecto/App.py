import re
from tkinter import ttk
import mysql.connector
import numpy as np
import pandas as pd
import tkinter.messagebox
from tkinter import *
#import tkinter as tk
import customtkinter as tk
from customtkinter import *
import random
import string
import datetime
import matplotlib.pyplot as plt
from mydb import user as userr
from mydb import contra as contraa


mydb = mysql.connector.connect(
    host="localhost",
    user=userr,
    password=contraa,
    port="3306",
    database="app_database"
)

print(mydb)

if __name__ == "__main__":

    ventana = CTk()
ventana.geometry("800x600+300+100")
ventana.resizable(False,False)
ventana.minsize(400,600)
ventana.maxsize(800,600)
#ventana.state("zoomed")
ventana.rowconfigure(0,weight=1)
ventana.columnconfigure(0,weight=1)

tk.set_appearance_mode("dark")
darkblack = "#030303"
fonta = tk.CTkFont(weight="bold",slant="roman",size=14,family="Open Sans")

OpenBig = tk.CTkFont(weight="bold",slant="roman",size=20,family="Open Sans")
font = tk.CTkFont(weight="bold",slant="roman",size=17,family="Open Sans")

frame1 = CTkFrame(ventana,fg_color=darkblack)
frame2= CTkFrame(ventana,fg_color="gray8")
frame3= CTkFrame(ventana,fg_color="gray10")
frame4= CTkFrame(ventana,fg_color="gray10")
frame5 = CTkFrame(ventana,fg_color=["Royalblue3","steelblue3"])

frame1.grid(row=0,column=0,sticky="nsew")
frame2.grid(row=0,column=0,sticky="nsew")
frame3.grid(row=0,column=0,sticky="nsew")
frame4.grid(row=0,column=0,sticky="nsew")
frame5.grid(row=0,column=0,sticky="nsew")


################################################################
#=======================Funciones frame4=======================#
class contabilidad(tk.CTk):
    def __init__(self,ganancias_total):
        super().__init__()
        self.ganancias_total = ganancias_total
        self.productos = []
        self.marcas = []
        self.ventas_dia = []
        self.productos_dia = []
        self.inventario = []


class graficos(tk.CTk):
    def __init__(self,nombre,cedula,total): 
        super().__init__()
        self.mombre = nombre
        self.cedula = cedula
        self.total = total
        self.gastos = []
        #self.datos = []

    def historigrama_ventas(self):
        cursor = mydb.cursor()
        consulta = f"SELECT SUM(total_g) , fecha FROM compra group by fecha"
        cursor.execute(consulta)
        np.datos = cursor.fetchall()
        datos1 = pd.DataFrame(np.datos,columns="ventas fechas".split())
        suma = datos1.fechas.value_counts()
        print(datos1)
        plt.bar(datos1.fechas,datos1.ventas)
        plt.show()
        cursor.close()

    def open_dialog(self):
        seleccionado = clientes_tree.focus()
        dato1 = clientes_tree.item(seleccionado)
        datos = dato1["values"]
        self.nombre = datos[0]
        self.cedula = datos[1]
        win_two=tk.CTkToplevel()
        win_two.geometry("700x500+300+100")
        win_two.resizable(False,False)
        

        frame4_boton_ventana.configure(state=DISABLED)  # Deshabilitamos el botón
        
        ##--Widges--##
        estadistica_nombre = tk.CTkLabel(win_two,width=150,height=75,bg_color="transparent",text=f'{self.nombre}',text_color="White",
            fg_color=None,font=font)
        estadistica_nombre.place_configure(x=250,y=1)

        estadistica_tree = ttk.Treeview(win_two,columns=("col1","col2","col3","col4","col5"),height=19)
        estadistica_tree.heading("#0",text="Nro",anchor=CENTER)
        estadistica_tree.heading(0,text="Productos",anchor=CENTER,command=lambda:ordernar_por(1))
        estadistica_tree.heading(1,text="Marca",anchor=CENTER,command=lambda:ordernar_por(2))
        estadistica_tree.heading(2,text="Cantidad",anchor=CENTER,command=lambda:ordernar_por(3))
        estadistica_tree.heading(3,text="Gasto",anchor=CENTER,command=lambda:ordernar_por(4))
        estadistica_tree.heading(4,text="Total gastado",anchor=CENTER)
        estadistica_tree.column("#0",width=30,anchor=CENTER)
        estadistica_tree.column(0,width=120,anchor=CENTER)
        estadistica_tree.column(1,width=100,anchor=CENTER)
        estadistica_tree.column(2,width=80,anchor=CENTER)
        estadistica_tree.column(3,width=80,anchor=CENTER)
        estadistica_tree.column(4,width=90,anchor=CENTER)
        estadistica_tree.place_configure(x=0,y=80)

        barra_estadistica = Scrollbar(win_two,orient=VERTICAL)
        barra_estadistica.config(command=estadistica_tree.yview)
        barra_estadistica.place_configure(x=500,y=80,height=400)

        def estadistica_datos(self):
            fila = estadistica_tree.get_children()
            for filas in fila:
                estadistica_tree.delete(filas)
            b = 1
            a = 0
            suma = 0
            cursor = mydb.cursor()
            consulta = f"SELECT idcliente FROM cliente WHERE nombre_c = '{self.nombre}' and cedula_c = '{self.cedula}'"
            cursor.execute(consulta)
            idcliente1 = cursor.fetchone()
            idcliente = idcliente1[0]
            print(idcliente)
            cursor = mydb.cursor()
            consulta2 = f"SELECT productos.nombre , marcas.marca , sum(compra.cantidad), sum(compra.total_g) FROM productos \
                left join marcas on marcas.codigo_marca = productos.codigo_marca\
                left join compra on compra.idproducto = productos.idproducto \
                WHERE compra.idcliente = '{idcliente}' group by compra.idproducto"
            cursor.execute(consulta2)
            np.datos = cursor.fetchall()
            print(np.datos)
            for i in np.datos:
                suma += np.datos[a][3]
                estadistica_tree.insert("","end",text=b,values=(np.datos[a][0],np.datos[a][1],np.datos[a][2],np.datos[a][3],suma))
                b += 1
                a += 1
            cursor.close()
        
        def ordernar_por(index1):
            if index1 == 1:
                index = "productos.nombre"
            elif index1 == 2:
                index == "marcas.marca"
            elif index1 == 3:
                index == "sum(compra.cantidad)"
            elif index1 == 4:
                index == "sum(compra.total_g)"
            fila = estadistica_tree.get_children()
            for filas in fila:
                estadistica_tree.delete(filas)
            b = 1
            a = 0
            suma = 0
            cursor = mydb.cursor()
            consulta = f"SELECT idcliente FROM cliente WHERE nombre_c = '{self.nombre}' and cedula_c = '{self.cedula}'"
            cursor.execute(consulta)
            idcliente1 = cursor.fetchone()
            idcliente = idcliente1[0]
            print(idcliente)
            cursor = mydb.cursor()
            consulta2 = f"SELECT productos.nombre , marcas.marca , sum(compra.cantidad), sum(compra.total_g) FROM productos \
                left join marcas on marcas.codigo_marca = productos.codigo_marca\
                left join compra on compra.idproducto = productos.idproducto \
                WHERE compra.idcliente = '{idcliente}' group by compra.idproducto order by '{index}' ASC"
            cursor.execute(consulta2)
            np.datos = cursor.fetchall()
            print(np.datos)
            for i in np.datos:
                suma += np.datos[a][3]
                estadistica_tree.insert("","end",text=b,values=(np.datos[a][0],np.datos[a][1],np.datos[a][2],np.datos[a][3],suma))
                b += 1
                a += 1
            cursor.close()
        estadistica_datos(self)
        

        def on_close():  
            '''
            Función que se llama cuando se pulsa el botón de cierre
            del gestor de ventanas 
            '''        
            win_two.destroy()  # Destruimos la ventana secundaria
            frame4_boton_ventana.configure(state=NORMAL)  # habilitamos el botón

        win_two.protocol("WM_DELETE_WINDOW", on_close)
    
    def mostrar_grafico(self):
        try:
            seleccionado = clientes_tree.focus()
            dato1 = clientes_tree.item(seleccionado)
            datos = dato1["values"]
            self.nombre = datos[0]
            self.cedula = datos[1]
            cursor = mydb.cursor()
            consulta = f"SELECT productos.nombre, SUM(compra.cantidad) FROM compra\
                LEFT JOIN productos ON productos.idproducto = compra.idproducto\
                WHERE compra.idcliente = (SELECT idcliente FROM cliente WHERE nombre_c = '{datos[0]}' and \
                cedula_c = '{datos[1]}') GROUP BY productos.nombre"
            cursor.execute(consulta)
            registro = cursor.fetchall()
            df = pd.DataFrame(registro,columns="nombres datos".split())
            total = sum(df.datos)
            total1 = int(total)
            print(total)
            plt.pie(df.datos, labels=df.nombres,autopct=lambda p: '{:.0f}'.format(p * total1 / 100))
            plt.legend(df.nombres, title = f"Historial de '{datos[0]}'", loc="lower right",bbox_to_anchor=(0.3, -0.08))
            plt.show()
            cursor.close()
        except IndexError:
            mensaje = tkinter.messagebox.showerror("ERROR","Seleccione un cliente para poder ver el grafico")




    def datos_clientes(self):
        vaciar_historial_c()
        parametro = frame4_lista_clientes.get()
        a = 0
        b = 1
        cursor = mydb.cursor()
        if parametro == "Cliente":
            funcion = entry4_2_buscador.get()
            func = funcion.capitalize()
            consulta = f"SELECT nombre_c , cedula_c FROM cliente WHERE nombre_c LIKE '{func+'%'}'"
        elif parametro == "Cedula":
            funcion = entry4_2_buscador.get()
            func = funcion
            consulta = f"SELECT id nombre_c , cedula_c FROM cliente WHERE cedula_c LIKE '{func+'%'}'"
        cursor.execute(consulta)
        np.datos = cursor.fetchall()
        print(np.datos)
        for i in np.datos:
            clientes_tree.insert("","end",text=b,values=(np.datos[a][0],np.datos[a][1]))
            a +=1
            b +=1
        entry4_2_buscador.delete(0,END)
        cursor.close()

def desactivar_clientes():
    clientes_tree.place_forget()
    entry4_2_buscador.place_forget()
    frame4_lista_clientes.place_forget()
    frame4_boton_buscador2.place_forget()
    frame4_boton_grafico.place_forget()
    frame4_boton_ventana.place_forget()
    barra_clientes.place_forget()
    frame4_boton_historigrama.place_forget()

def vaciar_historial_c():
    fila = clientes_tree.get_children()
    for filas in fila:
        clientes_tree.delete(filas)

def activar_clientes():
    desactivar_historial()
    clientes_tree.place_configure(x=0,y=60)
    entry4_2_buscador.place_configure(x=20,y=20)
    frame4_lista_clientes.place_configure(x=170,y=20)
    frame4_boton_buscador2.place_configure(x=320,y=20)
    frame4_boton_grafico.place_configure(x=520,y=20)
    frame4_boton_ventana.place_configure(x=520,y=80)
    barra_clientes.place_configure(x=205,y=61,height=415)
    #frame4_boton_historigrama.place_configure(x=520,y=140)
    grafico.datos_clientes()


'''Funciones del historial - Start'''

def buscador_4():
    try:
        vaciar_historial()
        valor1 = entry4_1_buscador.get()
        valora = valor1.capitalize()
        print(type(valora))
        dato = frame4_lista.get()
        print(dato)
        if dato == "Cliente":
            historial1(1,valora)
        elif dato == "Marca":
            historial1(2,valora)
        elif dato == "Producto":
            historial1(3,valora)
        elif dato == "Cedula":
            valor2 = int(valora)
            historial1(4,valor2)
    except TypeError:
        mensaje = tkinter.messagebox.showerror("ERROR","Valor invalido, inserte dato a buscar!")

def historial():
    desactivar_clientes()
    entry4_1_buscador.place_configure(x=200,y=20)
    frame4_lista.place_configure(x=350,y=20)
    frame4_boton_buscador.place_configure(x=500,y=20)
    barra4_1.place_configure(x=782,y=61,height=445)
    historial_tree.place_configure(x=0,y=60)
    vaciar_historial()
    a = 0
    b = 1
    cursor = mydb.cursor()
    consulta = f"SELECT compra.idcompra, cliente.nombre_c, cliente.cedula_c, productos.nombre, compra.cantidad , compra.total_g,\
            marcas.marca, compra.fecha FROM compra LEFT JOIN cliente ON cliente.idcliente = compra.idcliente \
            LEFT JOIN productos ON productos.idproducto = compra.idproducto \
            LEFT JOIN marcas on marcas.codigo_marca = productos.codigo_marca \
                ORDER BY 'compra.idcompra' and cliente.nombre_c"
    cursor.execute(consulta)
    np.datos = cursor.fetchall()
    for i in np.datos:
        historial_tree.insert("","end",text=b,values=(np.datos[a][0],np.datos[a][1],np.datos[a][2],np.datos[a][3],
        np.datos[a][4],np.datos[a][5],np.datos[a][6],np.datos[a][7]))
        a +=1
        b +=1
    cursor.close()

def historial1(valor: int,valor2):
    desactivar_clientes()
    entry4_1_buscador.place_configure(x=200,y=20)
    frame4_lista.place_configure(x=350,y=20)
    frame4_boton_buscador.place_configure(x=500,y=20)
    barra4_1.place_configure(x=782,y=61,height=445)
    historial_tree.place_configure(x=0,y=60)
    a = 0
    b = 1
    cursor = mydb.cursor()
    if valor == 1:
        consulta = f"SELECT compra.idcompra, cliente.nombre_c, cliente.cedula_c, productos.nombre, compra.cantidad , compra.total_g,\
            marcas.marca, compra.fecha FROM compra LEFT JOIN cliente ON cliente.idcliente = compra.idcliente \
            LEFT JOIN productos ON productos.idproducto = compra.idproducto \
            LEFT JOIN marcas on marcas.codigo_marca = productos.codigo_marca WHERE cliente.nombre_c LIKE '{valor2+'%'}' "
    if valor == 2:
        consulta = f"SELECT compra.idcompra, cliente.nombre_c, cliente.cedula_c, productos.nombre, compra.cantidad , compra.total_g,\
            marcas.marca, compra.fecha FROM compra LEFT JOIN cliente ON cliente.idcliente = compra.idcliente \
            LEFT JOIN productos ON productos.idproducto = compra.idproducto \
            LEFT JOIN marcas on marcas.codigo_marca = productos.codigo_marca WHERE marcas.marca LIKE '{valor2+'%'}' "
    if valor == 3:
        consulta = f"SELECT compra.idcompra, cliente.nombre_c, cliente.cedula_c, productos.nombre, compra.cantidad , compra.total_g,\
            marcas.marca, compra.fecha FROM compra LEFT JOIN cliente ON cliente.idcliente = compra.idcliente \
            LEFT JOIN productos ON productos.idproducto = compra.idproducto \
            LEFT JOIN marcas on marcas.codigo_marca = productos.codigo_marca WHERE productos.nombre LIKE '{valor2+'%'}' "
    if valor == 4:
        consulta = f"SELECT compra.idcompra, cliente.nombre_c, cliente.cedula_c, productos.nombre, compra.cantidad , compra.total_g,\
            marcas.marca, compra.fecha FROM compra LEFT JOIN cliente ON cliente.idcliente = compra.idcliente \
            LEFT JOIN productos ON productos.idproducto = compra.idproducto \
            LEFT JOIN marcas on marcas.codigo_marca = productos.codigo_marca WHERE cliente.cedula_c LIKE '{valor2+'%'}' "
    cursor.execute(consulta)
    np.datos = cursor.fetchall()
    for i in np.datos:
        historial_tree.insert("","end",text=b,values=(np.datos[a][0],np.datos[a][1],np.datos[a][2],np.datos[a][3],
        np.datos[a][4],np.datos[a][5],np.datos[a][6],np.datos[a][7]))
        a +=1
        b +=1
    cursor.close()
def vaciar_historial():
    fila = historial_tree.get_children()
    for filas in fila:
        historial_tree.delete(filas)

def desactivar_historial():
    entry4_1_buscador.place_forget()
    frame4_lista.place_forget()
    frame4_boton_buscador.place_forget()
    barra4_1.place_forget()
    historial_tree.place_forget()

grafico = graficos( "a", "b" , 0)
'''Funciones del historial - FIN'''
################################################################
#=======================Funciones frame 3======================#
class cliente:
    def __init__(self,nombre,cedula):
        self.nombre = nombre
        self.cedula = cedula

    def comprar(self):
        try:
            cursor = mydb.cursor()
            consulta = f"INSERT IGNORE INTO cliente(nombre_c,cedula_c) VALUES (%s, %s)"
            valores = (self.nombre,self.cedula)
            cursor.execute(consulta,valores)
            mydb.commit()
            idcompra = str(random.randint(100,999))+''.join((random.choice('abcdxz#r') for i in range(4)))+str(random.randint(10,99))
            cursor = mydb.cursor()
            consulta_c = f"SELECT idcliente FROM cliente WHERE nombre_c = '{self.nombre}' AND cedula_c = '{self.cedula}' "
            cursor.execute(consulta_c)
            idclient = cursor.fetchone()
            idcliente = idclient[0]
            x = datetime.datetime.now()
            consulta = f"SELECT producto,cantidad,monto,codigo FROM carrito"
            cursor.execute(consulta)
            carrito = cursor.fetchall()
            print(carrito)
            for i in range(len(carrito)):
                nombre = carrito[i][0]
                codigo = int(carrito[i][3])
                select = f" SELECT idproducto FROM productos WHERE nombre = '{nombre}' AND codigo_marca = '{codigo}'"
                cursor.execute(select)
                idproducto = cursor.fetchone()
                compra = f"INSERT INTO compra(idcompra,idcliente,idproducto,cantidad,total_g,fecha) VALUES(%s,%s,%s,%s,%s,%s)"
                cantidad = carrito[i][1]
                total = carrito[i][2]
                datos = (idcompra,idcliente,idproducto[0],cantidad,total,x.strftime("%Y/%m/%d"))
                cursor.execute(compra,datos)
                update = f"UPDATE productos SET inventario = inventario-'{cantidad}' WHERE idproducto = '{idproducto[0]}'"
                cursor.execute(update)
                mydb.commit()
            print(idcliente)
            print(idcompra)
            self.limpiar_carrito()
            cursor.close()
            mensaje = tkinter.messagebox.showinfo("Compra exitosa!","Su compra ha sido procesada con exito!!!")
        except TypeError:
            mensaje = tkinter.messagebox.showerror("ERROR","Su compra no ha podido ser procesada!")

    def show_frame_c(self):
        show_frame(frame2)
        self.activar_registro3()

    def activar_registro3(self):
        carrito_productos.place_forget()
        barra2_1.place_forget()
        barra_botones_3.pack_forget()
        buscador_3.place_forget()
        frame3_buscar.place_forget()
        frame3_lista.place_forget()
        carrito_compra.place_forget()
        frame3_label1.place_forget()
        barra2_2.place_forget()

        entry3_1.configure(state=NORMAL)
        entry3_2.configure(state=NORMAL)
        frame3_guardar_c.configure(state=NORMAL)

        entry3_1.place_configure(x=120,y=100)
        entry3_2.place_configure(x=120,y=200)
        frame3_nombre_label.place_configure(x=120,y=50)
        frame3_cedula_label.place_configure(x=120,y=150)
        frame3_guardar_c.place_configure(x=120,y=280)
        frame3_salir.place_configure(x=600,y=500)

    def limpiar_3(self):
        entry3_1.delete(0,END)
        entry3_2.delete(0,END)
        entry3_1.configure(state=DISABLED)
        entry3_2.configure(state=DISABLED)
        frame3_guardar_c.configure(state=DISABLED)
        
        entry3_1.place_forget()
        entry3_2.place_forget()
        frame3_guardar_c.place_forget()
        frame3_nombre_label.place_forget()
        frame3_cedula_label.place_forget()
        frame3_salir.place_forget()

    def ingresar_cliente(self):
        global valores
        try:
            nombre = ""
            cedula = 0
            n = entry3_1.get()
            c = entry3_2.get()
            nombre = n.capitalize()
            cedula = int(c)
            if nombre == "" or cedula < 0:
                mensaje = tkinter.messagebox.showwarning("Error","Rellene los campos")
            elif not isinstance(cedula, int):
                mensaje = tkinter.messagebox.showwarning("Error","Valores invalidos")
            else:
                self.limpiar_3()
            self.activar_frame3()
            self.actualizar3_compra()
            self.actualizar_3()
            self.nombre = nombre
            self.cedula = c
        except:
            pass

    def activar_frame3(self):
        a = 0
        cursor = mydb.cursor()
        consulta = "SELECT productos.idproducto, productos.nombre AS nombre, productos.precio AS precio, productos.inventario AS inventario \
            , marcas.marca AS marca \
            FROM productos LEFT JOIN marcas ON productos.codigo_marca = marcas.codigo_marca ORDER BY productos.idproducto"
        cursor.execute(consulta)
        datos = cursor.fetchall()
        #print(datos)
        for i in datos:
            carrito_productos.insert("",'end',text=a,values=(datos[a][1],datos[a][2],datos[a][4],datos[a][3],))
            a +=1
        carrito_productos.place_configure(x=0,y=0)
        barra2_1.place_configure(x=432,y=1,height=265)
        barra_botones_3.pack_configure(fill="y",side="right")
        buscador_3.place_configure(x=470,y=50)
        frame3_buscar.place_configure(x=470,y=100)
        frame3_lista.place_configure(x=470,y=150)
        carrito_compra.place_configure(x=0,y=285)
        frame3_label1.place_configure(x=530,y=285)
        barra2_2.place_configure(x=510,y=286,height=304)
        cursor.close()

    def buscador3_func(self):
        self.vaciar_tabla_3()
        a = 0
        busqueda1 = buscador_3.get()
        busqueda = busqueda1.capitalize()
        tipo = frame3_lista.get()
        cursor = mydb.cursor()
        if tipo == "Producto":
            consulta = f"SELECT productos.idproducto, productos.nombre AS nombre, productos.precio AS precio,\
            productos.inventario AS inventario , marcas.marca AS marca \
            FROM productos LEFT JOIN marcas ON productos.codigo_marca = marcas.codigo_marca WHERE productos.nombre LIKE '{busqueda+'%'}'\
            ORDER BY productos.nombre"
            cursor.execute(consulta)
            datos = cursor.fetchall()
            #print(datos)
            for i in datos:
                carrito_productos.insert("",'end',text=a,values=(datos[a][1],datos[a][2],datos[a][4],datos[a][3],))
                a +=1
        elif tipo == "Marca":
            consulta = f"SELECT productos.idproducto, productos.nombre AS nombre, productos.precio AS precio,\
            productos.inventario AS inventario , marcas.marca AS marca \
            FROM productos LEFT JOIN marcas ON productos.codigo_marca = marcas.codigo_marca WHERE marcas.marca LIKE '{busqueda+'%'}'\
            ORDER BY marcas.marca"
            cursor.execute(consulta)
            datos = cursor.fetchall()
            #print(datos)
            for i in datos:
                mostrar_productos.insert("",'end',text=a,values=(datos[a][1],datos[a][2],datos[a][4],datos[a][3],))
                a +=1
        elif tipo == "Codigo":
            consulta = f"SELECT productos.idproducto, productos.nombre AS nombre, productos.precio AS precio,\
            productos.inventario AS inventario , marcas.marca AS marca \
            FROM productos LEFT JOIN marcas ON productos.codigo_marca = marcas.codigo_marca WHERE productos.codigo_marca = '{busqueda}'\
            ORDER BY marcas.marca"
            cursor.execute(consulta)
            datos = cursor.fetchall()
            #print(datos)
            for i in datos:
                carrito_productos.insert("",'end',text=a,values=(datos[a][1],datos[a][2],datos[a][4],datos[a][3],))
                a +=1
        cursor.close()

    def eliminar_carrito(self):
        seleccionado = carrito_compra.focus()
        dato1 = carrito_compra.item(seleccionado)
        datos = dato1["values"]
        consulta = f"DELETE FROM carrito WHERE producto = '{datos[0]}'"
        cursor = mydb.cursor()
        cursor.execute(consulta)
        mydb.commit()
        self.actualizar3_compra()
        cursor.close()

    def agregar_3(self):
        seleccionado = carrito_productos.focus()
        dato1 = carrito_productos.item(seleccionado)
        r = CTkInputDialog(text="Ingrese la cantidad del producto que quiere comprar",title="Cantidad",button_fg_color="Royalblue4",button_hover_color="Royalblue3",
        button_text_color="White",fg_color="Gray10",entry_fg_color="gray16",entry_text_color="White",text_color="White")
        c = int(r.get_input())
        if isinstance(c,int):
            producto = dato1["values"]
            a = dato1["text"]
            cursor = mydb.cursor()
            consulta = f"SELECT productos.idproducto, productos.nombre AS nombre, productos.precio AS precio \
            , marcas.marca AS marca , marcas.codigo_marca AS codigo \
            FROM productos LEFT JOIN marcas ON productos.codigo_marca = marcas.codigo_marca WHERE productos.nombre = '{producto[0]}'\
            AND marcas.marca = '{producto[2]}'"
            cursor.execute(consulta)
            datos = cursor.fetchone()
            insertar = f"INSERT IGNORE INTO carrito (producto,cantidad,monto,marca,codigo) VALUES(%s,%s,%s,%s,%s)"
            monto = datos[2]*c
            valores = (datos[1],c,monto,datos[3],datos[4])
            cursor.execute(insertar,valores)
            mydb.commit()
            self.actualizar3_compra()
        elif not isinstance(c,int):
            mensaje = tkinter.messagebox.showerror("Error","Ingrese un dato valido (numeros)")
        cursor.close()

    def actualizar3_compra(self):
        a = 0
        b = 1
        self.vaciar_tabla3_carrito()
        cursor = mydb.cursor()
        consulta = "SELECT * FROM carrito"
        cursor.execute(consulta)
        datos = cursor.fetchall()
        consulta2 = f"SELECT SUM(monto) FROM carrito"
        cursor.execute(consulta2)
        suma = cursor.fetchall()
        for i in datos:
            carrito_compra.insert("",'end',text=b,values=(datos[a][0],datos[a][1],datos[a][2],datos[a][3],""))
            a +=1
            b +=1
        carrito_compra.insert("","end",text=b,values=("","","","",suma))
        cursor.close()

    def vaciar_tabla3_carrito(self):
        fila = carrito_compra.get_children()
        for filas in fila:
            carrito_compra.delete(filas)

    def vaciar_tabla_3(self):
        fila = carrito_productos.get_children()
        for filas in fila:
            carrito_productos.delete(filas)

    def limpiar_carrito(self):
        cursor = mydb.cursor()
        consulta = f"DELETE FROM carrito"
        cursor.execute(consulta)
        mydb.commit()
        self.actualizar3_compra()
        cursor.close()

    def actualizar_3(self):
        self.vaciar_tabla_3()
        a = 0
        cursor = mydb.cursor()
        consulta = "SELECT productos.idproducto, productos.nombre AS nombre, productos.precio AS precio, productos.inventario AS inventario \
            , marcas.marca AS marca \
            FROM productos LEFT JOIN marcas ON productos.codigo_marca = marcas.codigo_marca ORDER BY productos.idproducto"
        cursor.execute(consulta)
        datos = cursor.fetchall()
        #print(datos)
        for i in datos:
            carrito_productos.insert("",'end',text=a,values=(datos[a][1],datos[a][2],datos[a][4],datos[a][3],))
            a +=1
        cursor.close()
cliente1 = cliente("a","b")
################################################################
#========================Funciones frame 2=====================#
def user(valor):
    datos = ""
    cursor = mydb.cursor()
    cursor.execute(F"SELECT idempleado, usuario , nombre_e , cedula_e FROM empleado WHERE usuario = '{valor}' ")
    datos = cursor.fetchall()
    print(datos)
    label_id=CTkLabel(frame_usuario,text="ID empleado:   "+str(datos[0][0]),text_color="White",height=3,width=3)
    label_usuario=CTkLabel(frame_usuario,text="Username:   "+datos[0][1],text_color="White")
    label_nombre=CTkLabel(frame_usuario,text="Nombre del empleado:\n"+datos[0][2],text_color="White")
    label_cedula=CTkLabel(frame_usuario,text="Cedula:    "+str(datos[0][3]),text_color="White")
    
    label_id.place_configure(x=10,y=20)
    label_usuario.place_configure(x=10,y=40)
    label_nombre.place_configure(x=10,y=70)
    label_cedula.place_configure(x=10,y=110)
    cursor.close()

def buscador_2():
    vaciar_tabla()
    a = 0
    busqueda1 = entry2_buscador.get()
    busqueda = busqueda1.capitalize()
    tipo = frame2_lista.get()
    cursor = mydb.cursor()
    if tipo == "Producto":
        consulta = f"SELECT productos.idproducto, productos.nombre AS nombre, productos.precio AS precio,\
        productos.inventario AS inventario , marcas.marca AS marca \
        FROM productos LEFT JOIN marcas ON productos.codigo_marca = marcas.codigo_marca WHERE productos.nombre LIKE '{busqueda+'%'}'\
        ORDER BY productos.nombre"
        cursor.execute(consulta)
        datos = cursor.fetchall()
        #print(datos)
        for i in datos:
            print(i)
            mostrar_productos.insert("",'end',text=a,values=(datos[a][1],datos[a][2],datos[a][4],datos[a][3],))
            a +=1
    elif tipo == "Marca":
        consulta = f"SELECT productos.idproducto, productos.nombre AS nombre, productos.precio AS precio,\
        productos.inventario AS inventario , marcas.marca AS marca \
        FROM productos LEFT JOIN marcas ON productos.codigo_marca = marcas.codigo_marca WHERE marcas.marca LIKE '{busqueda+'%'}'\
        ORDER BY marcas.marca"
        cursor.execute(consulta)
        datos = cursor.fetchall()
        #print(datos)
        for i in datos:
            print(i)
            mostrar_productos.insert("",'end',text=a,values=(datos[a][1],datos[a][2],datos[a][4],datos[a][3],))
            a +=1
    cursor.close()

def eliminar_producto():
    seleccionado = mostrar_productos.focus()
    dato1 = mostrar_productos.item(seleccionado)
    print(dato1)
    producto = dato1["values"]
    cursor = mydb.cursor()
    consulta = f"DELETE FROM productos WHERE nombre = '{producto[0]}'"
    cursor.execute(consulta)
    mydb.commit()
    actualizar()
    cursor.close()

def guardar_edicion():
    nom = entry2_1.get()
    nombre = nom.capitalize()
    pre = entry2_2.get()
    precio = float(pre)
    canti = entry2_4.get()
    cantidad = int(canti)
    mar = entry2_5.get()
    marca = mar.capitalize()
    cursor = mydb.cursor()
    codigo_marca = random.randint(100,999)
    valores = (marca,codigo_marca)
    consulta = f"INSERT IGNORE INTO marcas (marca,codigo_marca) VALUES (%s, %s) "
    cursor.execute(consulta,valores)
    mydb.commit()
    cursor.execute(f"UPDATE IGNORE productos SET nombre = '{nombre}', precio = '{precio}', inventario = '{cantidad}' ")
    mydb.commit()
    cursor.execute(f"SELECT codigo_marca FROM marcas WHERE marca = '{marca}'")
    codigo1 = cursor.fetchone()
    codigo = codigo1[0]
    cursor.execute(f"UPDATE IGNORE productos SET codigo_marca = '{codigo}' WHERE nombre = '{nombre}' ")
    mydb.commit()
    entry2_1.delete(0,END)
    entry2_2.delete(0,END)
    entry2_4.delete(0,END)
    entry2_5.delete(0,END)
    actualizar()
    cursor.close()

def editar_producto():
    frame2_guardarPE.configure(state=NORMAL)
    frame2_guardarM.configure(state=DISABLED)
    frame2_guardarP.configure(state=DISABLED)
    seleccionado = mostrar_productos.focus()
    dato1 = mostrar_productos.item(seleccionado)
    print(dato1)
    producto = dato1["values"]
    entry2_1.insert(0,producto[0])
    entry2_2.insert(0,producto[1])
    entry2_4.insert(0,producto[3])
    entry2_5.insert(0,producto[2])

def add_m():
    #entry2_3.configure(state=NORMAL)
    entry2_1.configure(state=DISABLED)
    entry2_2.configure(state=DISABLED)
    entry2_4.configure(state=DISABLED)
    #entry2_5.configure(state=DISABLED)

def save_m():
    mar = entry2_5.get()
    marca = mar.capitalize()
    codigo_marca = random.randint(100,999)
    cursor = mydb.cursor()
    cursor.execute("SELECT marca , codigo_marca FROM marcas")
    np.datos = cursor.fetchall()
    for i in np.datos:
        if marca == np.datos[i][0]:
            mensaje = tkinter.messagebox.showwarning("Error",f"La marca {marca} ya esta registrada")
        elif codigo_marca == np.datos[i][1]:
            mensaje = tkinter.messagebox.showwarning("Error",f"El codigo generado ya existe, intente denuevo")
    else:
        insertar1 = f"INSERT INTO marcas (marca,codigo_marca) VALUES (%s, %s)"
        valores1 = (marca,codigo_marca)
        cursor.execute(insertar1,valores1)
        mydb.commit()
        entry2_5.delete(0,END)
    actualizar()
    cursor.close()

def add_p():
    activar_entry2()
    nom = entry2_1.get()
    nombre = nom.capitalize()
    pre = entry2_2.get()
    precio = float(pre)
    canti = entry2_4.get()
    cantidad = int(canti)
    mar = entry2_5.get()
    marca = mar.capitalize()
    if nom == "" or precio < 0 or cantidad < 0 or mar == "":
        mensaje = tkinter.messagebox.showwarning("Error","Rellene los campos")
    elif not isinstance(cantidad, int) or not isinstance(precio, float):
        mensaje = tkinter.messagebox.showwarning("Error","Valores invalidos")
    else:
        cursor = mydb.cursor()
        cursor.execute(f"SELECT codigo_marca from marcas WHERE marca = '{marca}' limit 1 ")
        codigo_marca1 = cursor.fetchone()
        #codigo_marca.pop()
        #codigo_marca = re.sub(",","",codigo_marca)
        if codigo_marca1 == None:
            codigo_marca = random.randint(100,999)
            insertar1 = f"INSERT INTO marcas (marca,codigo_marca) VALUES (%s, %s)"
            valores1 = (marca,codigo_marca)
            cursor.execute(insertar1,valores1)
            mydb.commit()
            insertar = f"INSERT INTO productos (nombre, codigo_marca ,precio , inventario) VALUES (%s, %s, %s, %s)"
            #print(nombre,precio,cantidad)
            valores = (nombre,codigo_marca,precio,cantidad)
            cursor.execute(insertar,valores)
            mydb.commit()
        else:
            codigo_marca =codigo_marca1
            insertar = f"INSERT INTO productos (nombre, codigo_marca ,precio , inventario) VALUES (%s, %s, %s, %s)"
            #print(nombre,precio,cantidad)
            valores = (nombre,codigo_marca,precio,cantidad)
            cursor.execute(insertar,valores)
            mydb.commit()
        #insertar2 = f"INSER INTO productos codigo_marca SELECT codigo_marca FROM marcas WHERE productos.nombre = '{nombre}' AND marcas.marca = '{marca}' "
        #cursor.execute(insertar2)
        #mydb.commit()
        entry2_1.delete(0,END)
        entry2_2.delete(0,END)
        entry2_4.delete(0,END)
        entry2_5.delete(0,END)
        actualizar()
    cursor.close()

def actualizar():
    vaciar_tabla()
    a = 0
    cursor = mydb.cursor()
    consulta = "SELECT productos.idproducto, productos.nombre AS nombre, productos.precio AS precio, productos.inventario AS inventario \
        , marcas.marca AS marca \
        FROM productos LEFT JOIN marcas ON productos.codigo_marca = marcas.codigo_marca ORDER BY productos.idproducto"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    #print(datos)
    for i in datos:
        print(i)
        mostrar_productos.insert("",'end',text=a,values=(datos[a][1],datos[a][2],datos[a][4],datos[a][3],))
        a +=1
    cursor.close()

def actualizar_nombre():
    vaciar_tabla()
    a = 0
    cursor = mydb.cursor()
    consulta = "SELECT productos.idproducto, productos.nombre AS nombre, productos.precio AS precio, productos.inventario AS inventario \
        , marcas.marca AS marca \
        FROM productos LEFT JOIN marcas ON productos.codigo_marca = marcas.codigo_marca ORDER BY productos.nombre"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    #print(datos)
    for i in datos:
        print(i)
        mostrar_productos.insert("",'end',text=a,values=(datos[a][1],datos[a][2],datos[a][4],datos[a][3],))
        a +=1
    cursor.close()

def actualizar_precio():
    vaciar_tabla()
    a = 0
    cursor = mydb.cursor()
    consulta = "SELECT productos.idproducto, productos.nombre AS nombre, productos.precio AS precio, productos.inventario AS inventario \
        , marcas.marca AS marca \
        FROM productos LEFT JOIN marcas ON productos.codigo_marca = marcas.codigo_marca ORDER BY productos.precio"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    #print(datos)
    for i in datos:
        print(i)
        mostrar_productos.insert("",'end',text=a,values=(datos[a][1],datos[a][2],datos[a][4],datos[a][3],))
        a +=1
    cursor.close()

def actualizar_marca():
    vaciar_tabla()
    a = 0
    cursor = mydb.cursor()
    consulta = "SELECT productos.idproducto, productos.nombre AS nombre, productos.precio AS precio, productos.inventario AS inventario \
        , marcas.marca AS marca \
        FROM productos LEFT JOIN marcas ON productos.codigo_marca = marcas.codigo_marca ORDER BY marcas.marca"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    #print(datos)
    for i in datos:
        print(i)
        mostrar_productos.insert("",'end',text=a,values=(datos[a][1],datos[a][2],datos[a][4],datos[a][3],))
        a +=1
    cursor.close()

def actualizar_inventario():
    vaciar_tabla()
    a = 0
    cursor = mydb.cursor()
    consulta = "SELECT productos.idproducto, productos.nombre AS nombre, productos.precio AS precio, productos.inventario AS inventario \
        , marcas.marca AS marca \
        FROM productos LEFT JOIN marcas ON productos.codigo_marca = marcas.codigo_marca ORDER BY productos.inventario"
    cursor.execute(consulta)
    datos = cursor.fetchall()
    #print(datos)
    for i in datos:
        print(i)
        mostrar_productos.insert("",'end',text=a,values=(datos[a][1],datos[a][2],datos[a][4],datos[a][3],))
        a +=1
    cursor.close()

def activar_marca():
    frame2_guardarP.configure(state=DISABLED)
    frame2_guardarM.configure(state=NORMAL)
    frame2_guardarPE.configure(state=DISABLED)
    entry2_1.configure(state=DISABLED)
    entry2_2.configure(state=DISABLED)
    entry2_4.configure(state=DISABLED)

def vaciar_tabla():
    fila = mostrar_productos.get_children()
    for filas in fila:
        mostrar_productos.delete(filas)


def activar_entry2():
    entry2_1.configure(state=NORMAL)
    entry2_2.configure(state=NORMAL)
    entry2_4.configure(state=NORMAL)

def activar_productos():
    frame2_botonP.configure(state=NORMAL)
    frame2_guardarM.configure(state=DISABLED)
    frame2_guardarPE.configure(state=DISABLED)
    entry2_1.configure(state=NORMAL)
    entry2_2.configure(state=NORMAL)
    entry2_4.configure(state=NORMAL)

def salir_frame2():
    entry2_1.configure(state=DISABLED)
    entry2_2.configure(state=DISABLED)
    entry2_4.configure(state=DISABLED)
    entry2_5.configure(state=DISABLED)
    
    entry3_1.configure(state=NORMAL)
    entry3_2.configure(state=NORMAL)
    frame3_guardar_c.configure(state=NORMAL)
################################################################
#========================Funciones frame 1=====================#
def login():
    usuario = entry1_1.get()
    contraseña = entry1_2.get()
    cursor = mydb.cursor()
    cursor.execute("SELECT usuario , contraseña FROM empleado")
    datos = cursor.fetchall()
    for i in datos:
        if usuario != i[0] and contraseña != i[1]:
            mensaje.place_configure(x=260,y=250)
        elif usuario == i[0] and contraseña == i[1]:
            frame2.tkraise()
            user(usuario)
            entry1_1.delete(0,END)
            entry1_2.delete(0,END)
            mensaje.place_forget()
            break
    actualizar()
    cursor.close()

def create_login():
    entry1_1.delete(0,END)
    entry1_2.delete(0,END)
    entry5_1.configure(state=NORMAL)
    entry5_2.configure(state=NORMAL)
    entry5_3.configure(state=NORMAL)
    entry5_4.configure(state=NORMAL)
    entry5_5.configure(state=NORMAL)
    frame5.tkraise()

#===================================================#
#===============Funciones frame 5 (crear usuario)===#

def crear_usuario():
    try:
        username = entry5_1.get()
        contraseña = entry5_2.get()
        contraseña2 = entry5_3.get()
        nombre = entry5_4.get()
        ced = entry5_5.get()
        cedula = int(ced)
        print(type(cedula))
        if contraseña != contraseña2:
            mensaje1 = tkinter.messagebox.showerror(title="error contraseña",message="Las contraseñas no son iguales")
            entry5_2.delete(0,END)
            entry5_3.delete(0,END)
        elif not isinstance(cedula, int):
            mensaje1 = tkinter.messagebox.showerror(title="error cedula",message="Valores invalidos, ingrese solo numeros")
            entry5_5.delete(0,END)
        elif username == "" or contraseña == "" or contraseña2 == "" or nombre == "" or cedula == None:
            mensaje1 = tkinter.messagebox.showerror(title="error",message="Rellene los campos")
        else:
            cursor = mydb.cursor()
            insertar = "INSERT INTO empleado (usuario,contraseña,nombre_e,cedula_e) VALUES (%s,%s,%s,%s)"
            val = (username,contraseña,nombre,cedula)
            cursor.execute(insertar,val)
            mydb.commit()
            mensaje = tkinter.messagebox.showinfo(title="Exito",message="Se ha creado el usuario con exito!!")
            entry5_1.delete(0,END)
            entry5_2.delete(0,END)
            entry5_3.delete(0,END)
            entry5_4.delete(0,END)
            entry5_5.delete(0,END)
            frame1.tkraise()
        cursor.close()
    except ValueError:
        mensaje1 = tkinter.messagebox.showerror(title="error",message="Rellene los campos")

def salir_crear():
    entry5_1.delete(0,END)
    entry5_2.delete(0,END)
    entry5_3.delete(0,END)
    entry5_4.delete(0,END)
    entry5_5.delete(0,END)
    entry5_1.configure(state=DISABLED)
    entry5_2.configure(state=DISABLED)
    entry5_3.configure(state=DISABLED)
    entry5_4.configure(state=DISABLED)
    entry5_5.configure(state=DISABLED)
    frame1.tkraise()

def show_frame(frame):
    frame.tkraise()
    

def ventana_up(frame):
    frame.tkraise()
    ventana.geometry("1000x800+300+100")
    ventana.resizable(False,False)
    ventana.minsize(400,600)
    ventana.maxsize(1000,800)



#========================================================#
#=====================Frame 1 code=======================#

frame1_boton = tk.CTkButton(frame1,width=90,height=40,border_color="royalblue4",border_width=1,corner_radius=10,
    font=font, text="Entrar",hover_color="royalblue3",text_color="royalblue4",fg_color="#030303",command=lambda:login())
frame1_boton.place_configure(x=350,y=390)
frame1_create= CTkButton(frame1,width=140,height=40,border_color="royalblue4",border_width=1,corner_radius=10,
    font=font, text="Crear cuenta",hover_color="royalblue3",text_color="royalblue4",fg_color="#030303",command=lambda:create_login())
frame1_create.place_configure(x=330,y=440)

entry1_1 = CTkEntry(frame1,width=180,height=30,corner_radius=50,fg_color=darkblack,border_color="royalblue4",
    bg_color="transparent",text_color="white",placeholder_text_color="royalblue3",placeholder_text="           Username")
entry1_1.place_configure(x=310,y=290)
entry1_2 = CTkEntry(frame1,width=180,height=30,corner_radius=50,fg_color=darkblack,border_color="royalblue4",
    bg_color="transparent",text_color="white",placeholder_text_color="royalblue3",placeholder_text="           Password")
entry1_2.place_configure(x=310,y=340)

mensaje = CTkLabel(frame1,font=fonta,text="El usuario o contraseña son incorrectos",text_color="royalblue4")
#========================================================#
#=====================Frame 2 code=======================#

frame_usuario = CTkFrame(frame2,height=160,width=160,bg_color="transparent",fg_color="gray18",corner_radius=20,
    border_color="gray12",border_width=3)

frame2_productos = CTkFrame(frame2,height=400,width=800,bg_color="transparent",fg_color="gray8",corner_radius=2,
    border_color="gray5",border_width=2)
frame2_productos.place_configure(x=0,y=200)
frame_usuario.place_configure(x=10,y=10)

frame2_buscador = CTkButton(frame2,font=fonta, text="Buscar",fg_color="mediumpurple3",command=lambda:buscador_2())
frame2_boton = CTkButton(frame2, text="Carrito",command=lambda:(show_frame(frame3),salir_frame2())
,fg_color="Royalblue4",hover_color="Springgreen3",font=font)
frame2_boton1 = CTkButton(frame2, text="Estadisticas",command=lambda:show_frame(frame4),font=font,fg_color="Royalblue4",hover_color="Royalblue3")
frame2_boton2 = CTkButton(frame2, text="Cerrar sesion",command=lambda:show_frame(frame1),font=font,fg_color="Royalblue4",hover_color="Firebrick3")
frame2_botonP = CTkButton(frame2_productos,text="productos",font=font,fg_color="gray14",command=lambda:activar_productos())
frame2_agregarP= CTkButton(frame2_productos,text="Agregar Producto",font=fonta,fg_color="gray14")
frame2_editarP= CTkButton(frame2_productos,text="Editar Producto",font=fonta,fg_color="gray14",command=lambda:editar_producto())
frame2_EliminarP= CTkButton(frame2_productos,text="Eliminar Producto",font=fonta,fg_color="gray14",command=lambda:eliminar_producto())
#frame2_marcas= CTkButton(frame2_productos,text="Marcas",font=fonta,fg_color="gray14")
frame2_editarM= CTkButton(frame2_productos,text="Editar Marca",font=fonta,fg_color="gray14")
frame2_agregarM= CTkButton(frame2_productos,text="Agregar Marca",font=fonta,fg_color="gray14",command=lambda:activar_marca())
frame2_guardarP = CTkButton(frame2_productos,text="Guardar Producto",font=fonta,fg_color="#1B5E20",command=lambda:add_p())
frame2_guardarM = CTkButton(frame2_productos,text="Guardar Marca",font=fonta,fg_color="#1B5E20",command=lambda:save_m(),state=DISABLED)
frame2_guardarPE = CTkButton(frame2_productos,text="Guardar edicion",font=fonta,fg_color="#1B5E20",state=DISABLED,command=lambda:guardar_edicion())
frame2_buscador.place_configure(x=330,y=160)
frame2_boton.place_configure(x=180,y=50)
frame2_boton1.place_configure(x=345,y=50)
frame2_boton2.place_configure(x=510,y=50)
frame2_botonP.place_configure(x=10,y=50)
#frame2_agregarP.place_configure(x=10,y=150)
frame2_editarP.place_configure(x=10,y=100)
frame2_EliminarP.place_configure(x=10,y=150)
#frame2_marcas.place_configure(x=10,y=200)
frame2_editarM.place_configure(x=10,y=200)
frame2_agregarM.place_configure(x=10,y=250)
frame2_guardarP.place_configure(x=635,y=300)
frame2_guardarM.place_configure(x=635,y=350)
frame2_guardarPE.place_configure(x=635,y=250)

frame2_lista = CTkOptionMenu(frame2,width=140,height=28,corner_radius=30,fg_color="gray14"
,dropdown_fg_color="gray14",values=["Producto","Marca"],font=fonta,dropdown_text_color="White",button_color="mediumpurple3")
frame2_lista.place_configure(x=480,y=160)
frame2_lista.set("Producto")

mostrar_productos= ttk.Treeview(frame2_productos,columns=("col1,","col2","col3","col4"),height=19,)
mostrar_productos.place_configure(x=180,y=2)
mostrar_productos['selectmode']='browse'
mostrar_productos.heading("#0",text="ID",anchor=CENTER)
mostrar_productos.heading("#1",text="Producto",anchor=CENTER,command=lambda:actualizar_nombre())    
mostrar_productos.heading("#2",text="Precio",anchor=CENTER,command=lambda:actualizar_precio())
mostrar_productos.heading("#3",text="Marca",anchor=CENTER,command=lambda:actualizar_marca())
mostrar_productos.heading("#4",text="Inventario",anchor=CENTER,command=lambda:actualizar_inventario())
mostrar_productos.column("#0",width=45,anchor=W)
mostrar_productos.column(0,width=125,anchor=CENTER)
mostrar_productos.column(1,width=80,anchor=CENTER)
mostrar_productos.column(2,width=120,anchor=CENTER)
mostrar_productos.column(3,width=65,anchor=CENTER)

barra1 = Scrollbar(frame2_productos,orient=VERTICAL)
barra1.place(x=615,y=3,height=400)
barra1.config(command=mostrar_productos.yview)

entry2_buscador = CTkEntry(frame2,width=140,height=30,corner_radius=3,placeholder_text_color="white",placeholder_text="Buscador",state=NORMAL)
entry2_1 = CTkEntry(frame2_productos,width=140,height=30,corner_radius=3,placeholder_text_color="white",placeholder_text="Nombre del producto",state=NORMAL)
entry2_2 = CTkEntry(frame2_productos,width=140,height=30,corner_radius=3,placeholder_text_color="white",placeholder_text="Precio",state=NORMAL)
#entry2_3 = CTkEntry(frame2_productos,width=140,height=30,corner_radius=3,placeholder_text_color="gray10",placeholder_text="Marca",state=DISABLED)
entry2_4 = CTkEntry(frame2_productos,width=140,height=30,corner_radius=3,placeholder_text_color="white",placeholder_text="Cantidad",state=NORMAL)
entry2_5 = CTkEntry(frame2_productos,width=140,height=30,corner_radius=3,placeholder_text_color="white",placeholder_text="Marca",state=NORMAL)
entry2_buscador.place_configure(x=180,y=160)
entry2_1.place_configure(x=635,y=50)
entry2_2.place_configure(x=635,y=100)
#entry2_3.place_configure(x=635,y=250)
entry2_4.place_configure(x=635,y=150)
entry2_5.place_configure(x=635,y=200)



#========================================================#
#=====================Frame 3 code=======================#

frame3_nombre_label = CTkLabel(frame3,width=150,height=30,font=fonta,text="Nombre del cliente",text_color="White")
frame3_cedula_label = CTkLabel(frame3,width=150,height=30,font=fonta,text="Cedula del cliente",text_color="White")
frame3_nombre_label.place_configure(x=120,y=50)
frame3_cedula_label.place_configure(x=120,y=150)

entry3_1 = CTkEntry(frame3,width=150,height=30,placeholder_text=" Nombre del cliente",corner_radius=5,state=DISABLED,placeholder_text_color="white")
entry3_2 = CTkEntry(frame3,width=150,height=30,placeholder_text=" Cedula del cliente",corner_radius=5,state=DISABLED,placeholder_text_color="white")
entry3_1.place_configure(x=120,y=100)
entry3_2.place_configure(x=120,y=200)

frame3_guardar_c = CTkButton(frame3,width=140,height=30,corner_radius=5,text="Ingresar",font=fonta,text_color="white"
    ,fg_color="#1B5E20",command=lambda:cliente1.ingresar_cliente())
frame3_salir = CTkButton(frame3,width=140,height=30,corner_radius=5,text="Salir",font=fonta,text_color="white"
    ,fg_color="Royalblue4",hover_color="Firebrick3",command=lambda:cliente1.show_frame_c())
frame3_guardar_c.place_configure(x=120,y=280)
frame3_salir.place_configure(x=600,y=500)

carrito_productos= ttk.Treeview(frame3,columns=("col1,","col2","col3","col4"),height=12)
carrito_productos['selectmode']='browse'
carrito_productos.heading("#0",text="ID",anchor=CENTER)
carrito_productos.heading("#1",text="Producto",anchor=CENTER)    
carrito_productos.heading("#2",text="Precio",anchor=CENTER)
carrito_productos.heading("#3",text="Marca",anchor=CENTER)
carrito_productos.heading("#4",text="Inventario",anchor=CENTER)
carrito_productos.column("#0",width=45,anchor=W)
carrito_productos.column(0,width=125,anchor=CENTER)
carrito_productos.column(1,width=80,anchor=CENTER)
carrito_productos.column(2,width=120,anchor=CENTER)
carrito_productos.column(3,width=65,anchor=CENTER)

barra2_1 = Scrollbar(frame3,orient=VERTICAL)
barra2_1.config(command=carrito_productos.yview)

carrito_compra = ttk.Treeview(frame3,columns=("col1,","col2","col3","col4","col5"),height=14)
carrito_compra['selectmode']='browse'
carrito_compra.heading("#0",text="ID",anchor=CENTER)
carrito_compra.heading("#1",text="Producto",anchor=CENTER)
carrito_compra.heading("#2",text="Cantidad",anchor=CENTER)
carrito_compra.heading("#3",text="Monto",anchor=CENTER)
carrito_compra.heading("#4",text="Marca",anchor=CENTER)
carrito_compra.heading("#5",text="Suma Total",anchor=CENTER)
carrito_compra.column("#0",width=45,anchor=W)
carrito_compra.column(0,width=125,anchor=CENTER)
carrito_compra.column(1,width=65,anchor=CENTER)
carrito_compra.column(2,width=80,anchor=CENTER)
carrito_compra.column(3,width=120,anchor=CENTER)
carrito_compra.column(4,width=80,anchor=CENTER)


barra2_2 = Scrollbar(frame3,orient=VERTICAL)
barra2_2.config(command=carrito_compra.yview)

buscador_3 = CTkEntry(frame3,width=140,height=30,corner_radius=5,placeholder_text="Buscador")
frame3_buscar = CTkButton(frame3,width=140,height=30,corner_radius=5,text="Buscar",fg_color="Royalblue4"
,bg_color="Royalblue4",font=font,command=lambda:cliente1.buscador3_func())

frame3_lista = CTkOptionMenu(frame3,width=140,height=28,corner_radius=30,fg_color="gray14"
,dropdown_fg_color="gray14",values=["Producto","Marca","Codigo"],font=fonta,dropdown_text_color="White",button_color="Royalblue4")
frame3_lista.set("Producto")

barra_botones_3 = CTkFrame(frame3,width=100,height=800,fg_color="Royalblue4")

frame3_add = CTkButton(barra_botones_3,text="Agregar",font=font,text_color="White",height=50,fg_color="Royalblue4"
,bg_color="Royalblue3",corner_radius=0,command=lambda:cliente1.agregar_3(),hover_color="Royalblue3")
frame3_delete = CTkButton(barra_botones_3,text="Eliminar",font=font,text_color="White",height=50,fg_color="Royalblue4"
,bg_color="Royalblue3",corner_radius=0,command=lambda:cliente1.eliminar_carrito(),hover_color="Royalblue3")
frame3_comprar = CTkButton(barra_botones_3,text="Comprar",font=font,text_color="White",height=50,fg_color="Royalblue4"
,hover_color="Springgreen3",corner_radius=0,command=lambda:cliente1.comprar())
frame3_boton = CTkButton(barra_botones_3, text="Menú",font=font,text_color="White",height=50,fg_color="Royalblue4"
,bg_color="Royalblue3",corner_radius=0,command=lambda:cliente1.show_frame_c())
frame3_limpiar = CTkButton(barra_botones_3,text="Limpiar\ncarrito",font=font,text_color="White",height=50,fg_color="Royalblue4"
,hover_color="Firebrick3",corner_radius=0,command=lambda:cliente1.limpiar_carrito())
frame3_agregar_c = CTkButton(barra_botones_3,text="Agregar\ncliente",font=font,text_color="White",height=50,fg_color="Royalblue4"
,hover_color="Firebrick3",corner_radius=0,command=lambda:cliente1.activar_registro3())
frame3_add.pack_configure(fill="x",side="top")
frame3_delete.pack_configure(fill="x",side="top")
frame3_comprar.pack_configure(fill="x",side="top")
frame3_limpiar.pack_configure(fill="x",side="top")
frame3_boton.pack_configure(fill="x",side="bottom")
frame3_agregar_c.pack_configure(fill="x",side="top")

frame3_label1 = CTkLabel(frame3,width=120,height=40,font=fonta,bg_color="transparent",text="Carrito de\ncompras"
,fg_color="gray10",compound="center",text_color="Springgreen4")
#========================================================#
#=====================Frame 4 code=======================#
frame4_barra_botones = CTkFrame(frame4,width=800,height=95,corner_radius=0,fg_color="Royalblue4")
frame4_barra_botones.pack_configure(fill="x",side="bottom")
'''FRONT del historial'''

historial_tree = ttk.Treeview(frame4,columns=("col1","col2","col3","col4","col5","col6","col7","col8"),height=21)
historial_tree.heading("#0",text="Nro",anchor=CENTER)
historial_tree.heading("#1",text="ID Compra",anchor=CENTER)
historial_tree.heading("#2",text="Cliente",anchor=CENTER)
historial_tree.heading("#3",text="Cedula",anchor=CENTER)
historial_tree.heading("#4",text="Producto",anchor=CENTER)
historial_tree.heading("#5",text="Cantidad",anchor=CENTER)
historial_tree.heading("#6",text="Monto",anchor=CENTER)
historial_tree.heading("#7",text="Marca",anchor=CENTER)
historial_tree.heading("#8",text="Fecha",anchor=CENTER)
historial_tree.column("#0",width=35,anchor=CENTER)
historial_tree.column(0,width=100,anchor=CENTER)
historial_tree.column(1,width=120,anchor=CENTER)
historial_tree.column(2,width=100,anchor=CENTER)
historial_tree.column(3,width=100,anchor=CENTER)
historial_tree.column(4,width=60,anchor=CENTER)
historial_tree.column(5,width=60,anchor=CENTER)
historial_tree.column(6,width=100,anchor=CENTER)
historial_tree.column(7,width=100,anchor=CENTER)

barra4_1 = Scrollbar(frame4,orient=VERTICAL)
barra4_1.config(command=historial_tree.yview)

entry4_1_buscador = CTkEntry(frame4,font=font,width=140,height=30,corner_radius=0,placeholder_text="Buscador",placeholder_text_color="white")
frame4_lista = CTkOptionMenu(frame4,width=140,height=30,corner_radius=10,bg_color="transparent",fg_color="gray8",text_color="white",
    button_hover_color="Royalblue4",dropdown_hover_color="gray8",dropdown_fg_color="gray8",dropdown_text_color="White",
    dropdown_font=font,font=font,values=["Cliente","Marca","Producto","Cedula"])
frame4_lista.set("Cliente")
frame4_boton_buscador = CTkButton(frame4,width=140,height=30,corner_radius=3,fg_color="Royalblue4",text="Buscar",font=font,
    text_color="White",command=lambda:buscador_4())

'''FRONT de CLIENTES'''
clientes_tree = ttk.Treeview(frame4,columns=("col1","col2"),height=20)
clientes_tree.heading("#0",text="ID",anchor=CENTER)
clientes_tree.heading("#1,",text="Cliente",anchor=CENTER)
clientes_tree.heading("#2",text="Cedula",anchor=CENTER)
clientes_tree.column("#0",width=30,anchor=CENTER)
clientes_tree.column(0,width=100,anchor=CENTER)
clientes_tree.column(1,width=80,anchor=CENTER)

barra_clientes = Scrollbar(frame4,orient=VERTICAL)
barra_clientes.config(command=clientes_tree.yview)

entry4_2_buscador = CTkEntry(frame4,font=font,width=140,height=30,corner_radius=0,placeholder_text="Buscador",
    placeholder_text_color="white")
frame4_boton_buscador2 = CTkButton(frame4,width=140,height=30,corner_radius=3,fg_color="Royalblue4",text="Buscar",font=font,
    text_color="White",command=lambda:grafico.datos_clientes())
frame4_lista_clientes = CTkOptionMenu(frame4,width=140,height=30,corner_radius=10,bg_color="transparent",fg_color="gray8",text_color="white",
    button_hover_color="Royalblue4",dropdown_hover_color="gray8",dropdown_fg_color="gray8",dropdown_text_color="White",
    dropdown_font=font,font=font,values=["Cliente","Cedula"])
frame4_lista_clientes.set("Cliente")
frame4_boton_grafico = CTkButton(frame4,width=140,height=30,corner_radius=3,fg_color="Royalblue4",text="Grafico",font=font,
    text_color="White",command=lambda:grafico.mostrar_grafico())
frame4_boton_ventana = CTkButton(frame4,width=140,height=32,corner_radius=3,fg_color="Royalblue4",text="Estadisticas",font=font,
    text_color="White",command=lambda:grafico.open_dialog())
frame4_boton_historigrama = CTkButton(frame4,width=140,height=32,corner_radius=3,fg_color="Royalblue4",text="Ventas fecha",font=font,
    text_color="White",command=lambda:grafico.historigrama_ventas())

'''Botones de la barra'''
frame4_historial_c = CTkButton(frame4_barra_botones,text="Historial",fg_color="Royalblue4",hover_color="Royalblue3",height=95
            ,corner_radius=0,width=100,font=font,command=lambda:historial())
frame4_clientes = CTkButton(frame4_barra_botones,text="Clientes",fg_color="Royalblue4",hover_color="Royalblue3",height=95
            ,corner_radius=0,width=100,font=font,command=lambda:activar_clientes())
frame4_boton = CTkButton(frame4_barra_botones, text="Menú",fg_color="Royalblue4",hover_color="Red",font=font
            ,height=95,width=100,corner_radius=0,command=lambda:show_frame(frame2))
frame4_historial_c.pack_configure(fill="y",side="left")
frame4_clientes.pack_configure(fill="y",side="left")
frame4_boton.pack_configure(fill="y",side="right")

#========================================================#
#===================Frame 5 code (crear usuario)=========#
crear_usuarios = CTkFrame(frame5,width=400,height=400,corner_radius=15,fg_color="mediumpurple1"
    ,border_color="darkorchid4",border_width=5)
crear_usuarios.place_configure(x=100,y=100)

label5_1 = CTkLabel(frame5,bg_color="transparent",font=OpenBig,text="Ingresa los datos y \ncrea tu cuenta")
label5_1.place_configure(x=200,y=42)

entry5_1 = CTkEntry(crear_usuarios,width=150,height=30,placeholder_text=" Nombre de usuario",corner_radius=5,state=DISABLED)
entry5_2 = CTkEntry(crear_usuarios,width=150,height=30,placeholder_text=" Contraseña",corner_radius=5,state=DISABLED)
entry5_3 = CTkEntry(crear_usuarios,width=150,height=30,placeholder_text=" Comprobar contraseña",corner_radius=5,state=DISABLED)
entry5_4 = CTkEntry(crear_usuarios,width=150,height=30,placeholder_text=" Nombre y apellido",corner_radius=5,state=DISABLED)
entry5_5 = CTkEntry(crear_usuarios,width=150,height=30,placeholder_text=" Cedula",corner_radius=5,state=DISABLED)

entry5_1.place_configure(x=120,y=50)
entry5_2.place_configure(x=120,y=90)
entry5_3.place_configure(x=120,y=130)
entry5_4.place_configure(x=120,y=170)
entry5_5.place_configure(x=120,y=210)

crear_5 = CTkButton(crear_usuarios,width=120,height=40,border_color="darkorchid4",border_width=3,corner_radius=10,
    font=font, text="Crear cuenta",hover_color="mediumpurple1",text_color=darkblack,fg_color="darkorchid4",command=lambda:crear_usuario())
crear_5.place_configure(x=180,y=280)
salir_5 = CTkButton(crear_usuarios,width=120,height=40,border_color="darkorchid4",border_width=3,corner_radius=10,
    font=font, text="Regresar",hover_color="mediumpurple1",text_color=darkblack,fg_color="darkorchid4",command=lambda:salir_crear())
salir_5.place_configure(x=50,y=280)

cliente1.limpiar_carrito()
show_frame(frame1)
ventana.mainloop()
