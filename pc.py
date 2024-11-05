from abc import ABC, abstractmethod 


class Producto(ABC):
    def __init__(self, costo, cantidad_inventario, detalles, nombre, marca , id) -> None:
        self.__costo =  costo
        self.__cantidad_inventario = cantidad_inventario
        self.__detalles = detalles
        self.__nombre = nombre
        self.__marca = marca
        self.__id = id
    @property
    def costo(self):
        return self.__costo
    @property
    def cantidad_inventario(self):
        return self.__cantidad_inventario
    @property
    def detalles(self):
        return self.__detalles
    @property
    def nombre(self):
        return self.__nombre
    @property
    def id(self):
        return self.__id
    @property
    def marca(self):
        return self.__marca
    @costo.setter
    def set_costo(self, nuevo_valor):
        self.__costo = nuevo_valor

    @cantidad_inventario.setter
    def set_cantidad_inventario(self, nuevo_valor):
        self.__cantidad_inventario = nuevo_valor

    @detalles.setter
    def set_detalles(self, nuevo_valor):
        self.__detalles =nuevo_valor

    @abstractmethod
    def generarReporte(self):
        pass

class Celular(Producto):
    def __init__(self, costo, cantidad_inventario, detalles, nombre, marca , id) -> None:
        super().__init__(self, costo, cantidad_inventario, detalles, nombre, marca , id)

    def generarReporte(self):
        pass

class Laptop(Producto):
    def __init__(self, costo, cantidad_inventario, detalles, nombre, marca , id) -> None:
        super().__init__(self, costo, cantidad_inventario, detalles, nombre, marca , id)

    def generarReporte(self):
        pass


class Accesorio(Producto):
    def __init__(self, costo, cantidad_inventario, detalles, nombre, marca , id) -> None:
        super().__init__(self, costo, cantidad_inventario, detalles, nombre, marca , id)

    def generarReporte(self):
        pass


class Funciones_Invetario:
    def registrar_producto(self, lista_productos):
        lista_productos.append()

    def actualizar_producto(self, lista_productos, id):
        for producto in lista_productos:
            if producto.id==id: 
                producto.costo = 200000
                producto.cantidad_inventario = 20
                break
    def eliminar_producto(self, lista_productos, id):
        indice = 0
        for indice_p, producto in enumerate(lista_productos):
            if producto.id==id: 
                indice = indice_p   
                break
        self.__lista_productos.pop(indice)

            
class Inventario:
    def __init__(self) -> None:
        self.__lista_productos=  []
        self.__funciones_adm_inventario = Funciones_Invetario()

    def menu(self):
        entrada = 0
        match entrada:
            case 1:
                self.__funciones_adm_inventario.registrar_producto(self.__lista_productos)
            case 2:
                self.__funciones_adm_inventario.actualizar_producto(self.__lista_productos)
            case 3:
                self.__funciones_adm_inventario.eliminar_producto(self.__lista_productos)
    
