import numpy as np
import pandas as pd
import json
clientes = {}


#R3000 = {"Nombre":"Jorge Castillo","Edad":36,"Telefono":"041459852","Direccion":" Calle 22","Preferente":True}
#R2000 = {"Nombre":"Claudia Mora","Edad":28,"Telefono":"042459854","Direccion":" Calle 13","Preferente":False}
#R = {"Nombre":"Roberto rojas","Edad":32,"Telefono":"042451835","Direccion":" Calle 42","Preferente":True}
programa = 0

while programa < 6:
    
        if programa == 1:
            nif = input("Introduce el nif del cliente ")
            nombre = input("Introduce el nombre del cliente ")
            edad = int(input("Introduce la edad del cliente "))
            correo = input("Introduce el correo del cliente")
            direccion = input(" Introduce la direccion del cliente ")
            telefono = input("Introduce el telefono del cliente")
            entrada = (input("¿Es cliente vip? (S/N) "))
            vip = entrada
            cliente = {"Nombre":nombre,"Edad":edad,"Correo":correo,"Direccion":direccion,"Telefono":telefono,"VIP":vip=="S"}
            clientes[nif] = cliente
        elif programa == 2:
            nif = input("Introduzca el NIF del cliente que quiere eliminar ")
            for i in clientes:
                if nif == clientes[nombre]:
                    print(f"Cliente {clientes[nombre]} Eliminado")
            del clientes[nif]
        elif programa == 3:
            nif = input("Indique el NIF del cliente:  ")
            if nif in clientes:
                print('NIF:', nif)
                for clave, valor in clientes[nif].items():
                    print(clave.title() + ':', valor)
            else:
                print("No existe un cliente con el NIF ", nif)
        elif programa == 4:
            print("####-- Lista de Clientes --####\n")
            registro = open("registro_clientes.txt", "r")
            for i in clientes:
                print("\n",clientes[i])
            registro.close()
        elif programa == 5:
            print("\n###-- Lista de clientes V.I.P --### \n")
            for clave, valor in clientes.items():
                if valor['VIP']:
                    print(clave, valor["Nombre"])
        else:
            exit
        print("\n ##- Presione 1 si quiere agregar un cliente nuevo\n"
            " ##-Presione 2 si quiere eliminar un cliente\n"
            " ##-Presione 3 si quiere ver los datos de un cliente\n"
            " ##-Presione 4 si quiere ver todos los clientes\n"
            " ##-Presione 5 si quiere ver los clientes V.I.P\n"
            " ##-Presione 6 si quiere salir del programa")
        programa = int(input("#: "))


pd.Series = clientes

print(pd.Series)
