import Aplicacion_con_sqlo as app
from tkinter import ttk
import sqlite3 as sql
import numpy as np
import pandas as pd
import os
import tkinter.messagebox
from tkinter import *

def ventana_clientes():
    global ventana2
    ventana2 = Toplevel(app.ventanaa1) #crear una ventana siguiente de la ventana1
    ventana2.geometry("500x500")
    ventana2.title("ventana2")

    ventana2.mainloop()