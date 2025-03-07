import pandas as pd
import numpy as np
from datetime import datetime
import random

class Validadores():
    @classmethod
    def validarEntero(cls, rangoA, rangoB, mensaje):
        entrada = -1
        while not (rangoA <= entrada <= rangoB):
            try:
                entrada = int(input(mensaje))
            except ValueError:
                pass
        return entrada
    
    @classmethod
    def validarString(cls, rangoA, rangoB, mensaje):
        entrada = ""
        while not ((rangoA < len(entrada) <= rangoB ) and not any([char.isdigit() for char in entrada])):
            entrada = input(f"{mensaje}: ")
            print(len(entrada))
        return entrada
    
    @classmethod
    def validar_opciones_multiples_int(cls, opciones, mensaje):
        entrada = -1

        while not (entrada in opciones):
            try:
                entrada = int(input(mensaje))
            except ValueError:
                pass
        return entrada
        
    @classmethod
    def validar_opciones_multiples_str(cls, opciones, mensaje):
        entrada = ""

        while not (entrada in opciones):
            try:
                entrada = input(mensaje)
            except ValueError:
                pass
        return entrada
    
    @classmethod
    def validar_correo(cls, mensaje):
        entrada = ""
        while not ('@' in entrada and '.' in entrada):
            try:
                entrada = input(mensaje)
            except ValueError:
                pass
        return entrada
    
    @classmethod
    def validar_numero(cls, mensaje):
        numero = ""
        while not (all([char.isdigit() for char in numero]) and len(numero)==9):
            try:
                numero = input(mensaje)
            except ValueError:
                pass
        return numero 
    
    @classmethod
    def validar_fechas(cls, mensaje):
        def validar(fecha ):
            formato = "%Y-%m-%d"
            try:
                fecha =datetime.strptime(fecha, formato)            
                return fecha
            except Exception:
                return False
        entrada = ""
        while True:
            entrada = input(mensaje)
            fecha = validar(entrada)
            if fecha:
                return fecha

class Habitacion:
    tipos_habitacion = {
        0: ("Individual",100),
        1:("Doble",160),
        2:("Suite",300)
    }

    def __init__(self,id,  numero, precio, tipo=1, disponible =True):
        self.__id = id
        self.__numero = numero
        self.__precio = precio
        self.__tipo = tipo
        self.__disponible = disponible
        
    @property
    def numero(self):
        return self.__numero
    @property
    def precio(self):
        return self.__precio 
    @property
    def tipo(self):
        return self.__tipo
    @property
    def disponible(self):
        return self.__disponible
    @property
    def id(self):
        return self.__id
    @disponible.setter
    def set_disponible(self, nuevo):
        self.__disponible = nuevo
            
    def __str__(self):
        return f"""
            ID habitacion: {self.id}
            Numero de habitacion: {self.numero}
            Precio:  {self.precio}
            Tipo: {self.tipos_habitacion[self.tipo][0]}
            Disponible: {"Si" if self.disponible else False}
            """

class Cliente:
    def __init__(self,id, nombre, correo, telefono):
        self.__id = id
        self.__nombre =nombre
        self.__correo = correo
        self.__telefono = telefono
    @property
    def id(self):
        return self.__id
    @property
    def nombre(self):
        return self.__nombre
    @property
    def correo(self):
        return self.__correo
    @property
    def telefono(self):
        return self.__telefono
    @property
    def reservas(self):
        return self.__reservas


    
    def __str__(self):
        return f"""
        ID: {self.id}
        Nombre: {self.nombre}
        Correo: {self.correo}
        Telefono: {self.telefono}
        """

class Reserva:
    def __init__(self, id, cliente, habitaciones_reservadas=[],fecha_llegada = "", fecha_salida = ""):
        self.__id = id
        self.__cliente = cliente
        self.__habitaciones_reservadas = habitaciones_reservadas
        self.__fecha_llegada = fecha_llegada
        self.__fecha_salida = fecha_salida
        self.__monto = 0
        self.__pagado =  False
        
    @property
    def cliente(self):
        return self.__cliente
    @property
    def habitaciones_reservadas(self):
        return self.__habitaciones_reservadas
    @property
    def fecha_llegada(self):
        return self.__fecha_llegada
    @property
    def fecha_salida(self):
        return self.__fecha_salida
    @property
    def monto(self):
        return self.__monto
    @property
    def id(self):
        return self.__id
    @property
    def pagado(self):
        return self.__pagado
    @pagado.setter
    def set_pagado(self, nuevo):
        self.__pagado = nuevo
        
    def calular_monto(self):
        monto+=0
        noches=self.fecha_salida-self.fecha_llegada
        for habitacion in self.habitaciones_reservadas:
            monto += (habitacion.precio * noches.days)
        self.__monto = monto
        return monto
    def __str__(self):
        return f"""
        ID RESERVA: {self.id}
        Cliente: {self.cliente.nombre} | {self.cliente.id}
        Habitaciones reservadas {', '.join([habitacion.numero for habitacion in self.habitaciones_reservadas])}
        Fecha llegada : {self.fecha_llegada}
        fecha salida :{self.fecha_salida}
        monto {self.calular_monto()}
        pagado: {"SI" if self.pagado else 'NO'}
                    """

class Pago:
    def __init__(self, id_pago, id_reserva,fecha_pago, monto_total, metodo_pago):
        self.__fecha_pago = fecha_pago
        self.__monto_total = monto_total
        self.__metodo_de_pago= metodo_pago 
        self.__id_pago =id_pago
        self.__id_reserva = id_reserva

class Hotel:
    __num_habitacion = 100
    __id_cliente = 0
    __id_habitacion = 0
    __id_reservas =0
    __id_pago = 0
    def __init__(self):
        self.__habitaciones = []
        self.__reservas = []
        self.__clientes = []
        self.__pagos = []
    
    def seleccion_cliente(self):
            opciones_clien = []
            for cliente in self.__clientes:
                    opciones_clien.append(cliente.id)
                    print(cliente)
            id_cliente = Validadores.validar_opciones_multiples_int(opciones_clien, "[+] Ingrese el id de cliente:")
            return self.__clientes[id_cliente]
    
    def seleccion_habitacion(self):
            opciones_habi = []
            for  habitacion in self.__habitaciones:
                    if habitacion.disponible:
                        opciones_habi.append(habitacion.id)
                        print(habitacion)
            habitacion_id= Validadores.validar_opciones_multiples_int(opciones_habi, "[+] Ingrese el id de habitacion:")
            return self.__habitaciones[habitacion_id]
    def seleccion_reserva(self):
        opciones_reserva = []
        for reserva in self.__reservas:
            if not reserva.pagado:
                opciones_reserva.append(reserva.id)
                print(reserva)
        id_reserva = Validadores.validar_opciones_multiples_int(opciones_reserva, "[+] Ingrese el id de reserva a pagar")
        return self.__reservas[id_reserva]
        
    def agregar_habitacion(self):
        diccionario_habitaciones = Habitacion.tipos_habitacion
        while True:
            for key, (tipo, monto) in diccionario_habitaciones.items():
                print(f"{key+1}. {tipo} - S./{monto}" )
            match Validadores.validar_opciones_multiples_int([1,2,3] , "[!] Ingrese opcion de habitacion: ")        :
                case 1:key=0
                case 2:key=1
                case 3:key=2
            self.__habitaciones.append(Habitacion(self.__id_habitacion, self.__num_habitacion,diccionario_habitaciones[key][0], key))
            self.__num_habitacion+=1;self.__id_habitacion+=1
            match Validadores.validar_opciones_multiples_int([0,1], "[!!] Desea agregar otra habitacino? 1.SI, 0.NO: "):
                case 0:return
                case 1: continue
    def creacion_cliente(self):
        while True:
            self.__clientes.append(Cliente(
                    self.__id_cliente,
                    Validadores.validarString(3,40, "[+] Ingrese su nmobre: "),
                    Validadores.validar_correo("[+] Ingrese correo del cliente: "),
                    Validadores.validar_numero("[+] Ingrese numero del cliente: "),
                      ))
            self.__id_cliente+=1
            match Validadores.validar_opciones_multiples_int([0,1], "[!!] Desea agregar otro cliente?: 1.SI, 0.NO: "):
                case 0: return
                case 1: continue

    def realizar_reserva(self):
        habitaciones_reserva = []
        while True:
            cliente = self.seleccion_cliente()
            while True:
                habitacion = self.seleccion_habitacion()
                habitacion.set_disponible = False
                habitaciones_reserva.append(habitacion)
                match Validadores.validar_opciones_multiples_int([0,1], "[!!] Desea agregar otra habitacion? 1.SI, 0.NO: "):
                    case 0:break
                    case 1:continue
            while True:
                fecha_ingreso = Validadores.validar_fechas("[!] Ingrese fecha entrada ej 2025-01-01: ")
                fecha_salida =  Validadores.validar_fechas("[!] Ingrese fecha salida ej 2025-01-01: ")
                diferencia=fecha_salida-fecha_ingreso
                if diferencia.days>=0:break
            reserva = Reserva(self.__id_reservas, cliente,habitaciones_reserva,fecha_ingreso, fecha_salida)
            self.__reservas.append(reserva)
            self.__id_reservas+=1
            match Validadores.validar_opciones_multiples_int([0,1], "[!!] Desea agregar otra reserva?: 1.SI, 0.NO: "):
                case 0:return
                case 1:continue

    def procesamiento_de_pagos(self):
        while True:
            reserva = self.seleccion_reserva()      
            print(reserva)
            reserva.set_pagado = True
            while True:
                print(f"""
                    METODOS DE PAGO:
                    1. tarjeta
                    2. efectivo
                    3. poto
                    """)
                metodo = Validadores.validarEntero(1,2, "[!] Ingese metodo de pago")
                if 1==metodo  or metodo==2:
                    break
            self.__pagos.append(Pago(self.__id_pago, reserva.id , Validadores.validar_fechas("[!]Ingrese fecha ej 2025-01-01: "), reserva.monto, metodo))
            match Validadores.validar_opciones_multiples_int([0,1], "[!!] Desea agregar otro pago?: 1.SI, 0.NO: "):
                case 0:return
                case 1:continue
    def menu(self):
        while True:
            print("""
            1. registro de habitaciones
            2. creacion de clientes
            3. realizacion de reservas
            4. procesamiento de pagos
            5 cancelacion de reservas
            6. generaciond de reportes
            7. analisis estadistico
            8. eventos aleatorio
            """)

            match Validadores.validarEntero(1,6, "[+] Ingre su opcion: " ):
                case 1:
                    self.agregar_habitacion()
                case 2:
                    self.creacion_cliente()
                case 3:
                    self.realizar_reserva()
                case 4:
                    self.procesamiento_de_pagos()
                case 6:
                    exit()

ot = Hotel()
ot.menu()
