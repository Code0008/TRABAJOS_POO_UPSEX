from abc import ABC, abstractmethod
from random import randint
class Ticket(ABC):
    def __init__(self, tipo, precio_base, asiento_elegido=False, seguro_des_viaje=False, ciudad_destino="", ciudad_origen="", nombre_cliente= "", numero_vuelo=0) -> None:
        self._tipo = tipo
        self._precio_base = precio_base
        self._asiento_elegido = asiento_elegido
        self._seguro_des_viaje = seguro_des_viaje
        self._ciudad_destino = ciudad_destino
        self._ciudad_origen = ciudad_origen
        self._nombre_cliente = nombre_cliente
        self._numero_vuelo = numero_vuelo
    def get_tipo(self):
        return self._tipo
    def get_precio_base(self):
        return self._precio_base
    def get_asiento_elegido(self):
        return self._asiento_elegido if self._asiento_elegido !=None  else -1
        # contemplando caso de full :V
    def get_seguro_des_viaje(self):
        return self._seguro_des_viaje

    def get_ciudad_destino(self):
        return self._ciudad_destino
    def get_ciudad_origen(self):
        return self._ciudad_origen
    def get_nombre_cliente(self):
        return self._nombre_cliente
    def get_numero_vuelo(self):
        return self._numero_vuelo
    
    @abstractmethod
    def mostrar_ticket(self) -> str:
        pass
    @abstractmethod
    def calcular_precio(self):
        pass
    
class Ligero(Ticket):
    def __init__(self, tipo="Ligero", equipaje_de_bodega = False, asiento_elegido=False, seguro_des_viaje=False, ciudad_destino="", ciudad_origen="", nombre_cliente="", numero_vuelo=0) -> None:
        super().__init__( tipo=tipo, precio_base=80, asiento_elegido=asiento_elegido, seguro_des_viaje=seguro_des_viaje, ciudad_destino=ciudad_destino, ciudad_origen=ciudad_origen, nombre_cliente= nombre_cliente, numero_vuelo= numero_vuelo)
        self.__equipaje_de_bodega = equipaje_de_bodega

    def get_equipaje_en_bodega(self):
            return self.__equipaje_de_bodega
    
    def calcular_precio(self):
        return self._precio_base + ( 50 if self._asiento_elegido else 0 ) + (100 if self.__equipaje_de_bodega else 0) + (100 if self._seguro_des_viaje else 0)
    
    def mostrar_ticket(self) -> str:
        return f"""
            Tipo: {self.get_tipo()}
            Nombre cliente: {self._nombre_cliente}
            Precio base: {self._precio_base}
            Asiento elegido: {"Si" if self._asiento_elegido else 'No'}
            Seguro des viaje: {"Si" if self._seguro_des_viaje  else "No"}
            Equipaje en bodega: {"Si" if self.__equipaje_de_bodega else 'No'}
            Ciudad destino: {self._ciudad_destino}
            Costo: {self.calcular_precio()}    

            """    
class Smart(Ticket):
    def __init__(self, tipo="Smart", asiento_elegido=False, seguro_des_viaje = False, ciudad_destino="", ciudad_origen="", nombre_cliente="",  numero_vuelo=0) -> None:
        super().__init__(tipo=tipo, precio_base=120, asiento_elegido=asiento_elegido, seguro_des_viaje=seguro_des_viaje, ciudad_destino=ciudad_destino, ciudad_origen=ciudad_origen, nombre_cliente= nombre_cliente, numero_vuelo= numero_vuelo)

    def calcular_precio(self):
        return self._precio_base+ (30 if self._asiento_elegido else 0) + (100 if self._seguro_des_viaje else 0)
    def mostrar_ticket(self) -> str:
        return f"""
            Tipo: {self.get_tipo()}
            Nombre cliente: {self._nombre_cliente}
            Precio base: {self._precio_base}
            Asiento elegido: {"Si" if self._asiento_elegido else 'No'}
            Seguro des viaje: {"Si" if self._seguro_des_viaje  else "No"}
            Ciudad destino: {self._ciudad_destino}
            Costo: {self.calcular_precio()}    
            """

class Full(Ticket):
    def __init__(self, tipo="Full", asiento_elegido=None, seguro_des_viaje=False, comida_vegana=False, ciudad_destino="", ciudad_origen="", nombre_cliente="",  numero_vuelo=0) -> None:
        super().__init__( tipo=tipo, precio_base=180, asiento_elegido=asiento_elegido, seguro_des_viaje=seguro_des_viaje, ciudad_destino=ciudad_destino, ciudad_origen=ciudad_origen, nombre_cliente= nombre_cliente, numero_vuelo= numero_vuelo)
        self.__comida_vegana = comida_vegana

    def get_comida_vegana(self):
        return self.__comida_vegana
    def calcular_precio(self):
        return self._precio_base+ (30 if self.__comida_vegana else 0) +  (100 if self._seguro_des_viaje else 0)
    def mostrar_ticket(self) -> str:
        return f"""
            Tipo: {self.get_tipo()}
            Nombre cliente: {self._nombre_cliente}
            Precio base: {self._precio_base}
            Seguro des viaje: {"Si" if self._seguro_des_viaje  else "No"}
            Comida vegana: {"Si" if self.__comida_vegana else 'No'}
            Ciudad destino: {self._ciudad_destino}
            Costo: {self.calcular_precio()}    
            """


class Manejador:
    def __init__(self) -> None:
        self.__lista_tickets = []

    def agregar_tickets(self, ticket):
        self.__lista_tickets.append(ticket)  # agrego  objeto :v 

    def listar_todos_los_datos(self): # reporte uno V:
        for ticket in self.__lista_tickets:
            print(ticket.mostrar_ticket())
        

    def ingreso_total_por_ticket(self): # reporte dos :v
        contadores = [
            0, # Ligero
            0, # Smart 
            0 # Full
        ]
        for ticket in self.__lista_tickets:
            match ticket.get_tipo():
                case "Ligero":
                    contadores[0]+= ticket.calcular_precio()
                case "Smart":
                    contadores[1]+= ticket.calcular_precio()
                case "Full":
                    contadores[2]+= ticket.calcular_precio()
        print(f"""
            Ingreso total por ligero:  {contadores[0]}
            Ingreso total por smart:  {contadores[1]}
            Ingreso total por Full:  {contadores[2]}
            """)
    
    def mostrar_porcentaje_tickets_comida_vegana(self):  # reporte 3 :v
        contadores = [0, # total tickets de Full:v
                      0] # cuantos con comida vegana

        for ticket in self.__lista_tickets:
            match ticket.get_tipo():
                case "Full":
                    contadores[0]+=1
                    if ticket.get_comida_vegana():
                        contadores[1]+=1

        operacion = (contadores[1]*100) / (contadores[0] if contadores[0] != 0 else 1)
        print(f"""
        Porcentaje de tickets que solicitan comida vegana tipo full: {operacion}%
            """)
        

    def listar_tickets_ordenados_por_ciudad_de_destino(self):
        for indice, ticket in enumerate(self.__lista_tickets): # ordenando :V
            ticket_actual = ticket
            salto = indice-1

            while (salto>=0) and (ord(self.__lista_tickets[salto].get_ciudad_destino()[0]) > ord(ticket_actual.get_ciudad_destino()[0])):
                self.__lista_tickets[salto+1] = self.__lista_tickets[salto]
                salto-=1
            
            self.__lista_tickets[salto+1]= ticket_actual

        self.listar_todos_los_datos()   # listado 



man = Manejador()
man.agregar_tickets(Ligero(equipaje_de_bodega=True, asiento_elegido=False, seguro_des_viaje=True, ciudad_destino="Lima", ciudad_origen="Puno", nombre_cliente="Bill", numero_vuelo=randint(100, 100)))
man.agregar_tickets(Ligero(equipaje_de_bodega=False, asiento_elegido=True, seguro_des_viaje=True, ciudad_destino="Puno", ciudad_origen="Cajamarca", nombre_cliente="Ellis", numero_vuelo=randint(100, 100)))
man.agregar_tickets(Ligero(equipaje_de_bodega=True, asiento_elegido=True, seguro_des_viaje=True, ciudad_destino="Tacna", ciudad_origen="Arequipa", nombre_cliente="Rochelle", numero_vuelo=randint(100, 100)))

man.agregar_tickets(Smart(asiento_elegido=True, seguro_des_viaje=False, ciudad_destino="Arequipa", ciudad_origen="Lima", nombre_cliente="Zoey", numero_vuelo=randint(100, 100)))
man.agregar_tickets(Smart(asiento_elegido=False, seguro_des_viaje=True, ciudad_destino="Chota", ciudad_origen="Lima", nombre_cliente="Coach", numero_vuelo=randint(100, 100)))
man.agregar_tickets(Smart(asiento_elegido=False, seguro_des_viaje=False, ciudad_destino="Iquitos", ciudad_origen="Lima", nombre_cliente="Nick", numero_vuelo=randint(100, 100)))

man.agregar_tickets(Full(seguro_des_viaje=True, comida_vegana=True, ciudad_destino="Iquiqe", ciudad_origen="Lima", nombre_cliente="Virgil", numero_vuelo=randint(100, 100)))
man.agregar_tickets(Full(seguro_des_viaje=True, comida_vegana=False, ciudad_destino="Moskou", ciudad_origen="Lima", nombre_cliente="Louis", numero_vuelo=randint(100, 100)))
man.agregar_tickets(Full(seguro_des_viaje=False, comida_vegana=False, ciudad_destino="Buenos Aires", ciudad_origen="Lima", nombre_cliente="Yupanqui", numero_vuelo=randint(100, 100)))

man.listar_todos_los_datos()
print("/"*50)
man.ingreso_total_por_ticket()
print("/"*50)
man.mostrar_porcentaje_tickets_comida_vegana()
print("/"*50)
man.listar_tickets_ordenados_por_ciudad_de_destino()
print("/"*50)
