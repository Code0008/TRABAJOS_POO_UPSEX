

class Investigador:
    def __init__(self, id, nombre) -> None:
        self.__id_investigador = id
        self.__nombre = nombre
        self.__descrubrimiento = "ningnuno"
    @property
    def id(self):
        return self.__id_investigador
    @property
    def nombre(self):
        return self.__nombre
    @id.setter
    def set_id(self, nuevo):
        self.__id_investigador = nuevo
    @nombre.setter
    def set_nombre(self, nuevo):
        self.__nombre = nuevo
    @property
    def descubrimiento(self):
        return self.__descrubrimiento

    def registrarDescubrimiento(self, nombre_cultura):
        self.__descrubrimiento = nombre_cultura

class Arqueologo(Investigador):
    def __init__(self, id, nombre, campamentos) -> None:
        super().__init__(id, nombre)
        self.__campamentos = campamentos

    @property
    def campamentos(self):
        return self.__campamentos
    
    @campamentos.setter
    def set_campamentos(self, campamentos):
        self.__campamentos = campamentos
    
    def __str__(self) -> str:
        return f"""
        campamentos : {self.campamentos}
        Nombre: {self.nombre}
        Id: {self.id}
        Descubrimiento : {self.descubrimiento}
        """
    

class AtributoCultural:
    def __init__(self, id, nombre) -> None:
        self.__idatributo = id
        self.__nombre  = nombre
    @property
    def id(self):
        return self.__idatributo
    @property
    def nombre(self):
        return self.__nombre
    
    @id.setter
    def set_id(self, nuevo):
        self.__idatributo = nuevo
    @nombre.setter
    def set_nombre(self, nuevo):
        self.__nombre = nuevo

    def __str__(self) -> str:
        return f"""
        id de atributo cultura: {self.id}
        nombre: {self.nombre}
        """
class Cultura:
    __id_aributo = 0
    def __init__(self, id, nombre, nombre_arqueologo, campamentos) -> None:
        self.__atributos_culturales = {} # 
        self.__arqueologo   = Arqueologo(0,  nombre_arqueologo, campamentos)
        self.__arqueologo.registrarDescubrimiento(nombre)
        self.__idCultura = id
        self.__nombre = nombre
#////////////////////////////////////////////////////////   
    @property
    def atributos_cultural(self):
        return self.__atributos_culturales.values()
    @property
    def id(self):
        return self.__idCultura
    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def set_nombre(self, nuevo):
        self.__arqueologo.registrarDescubrimiento(nuevo)
        self.__nombre = nuevo
    @id.setter
    def set_id(self, nuevo):
        self.__idCultura = nuevo
    #////////////////////////////////////////////////////////
    def agregar_atributos_culturales(self): # agregar 
        nombre_aributo = input("Nombre del atributo cultural: ")+str(self.__id_aributo)
        self.__atributos_culturales[self.__id_aributo]= AtributoCultural(self.__id_aributo, nombre_aributo)
        self.__id_aributo += 1
    def acceder_atributo(self, id_buscar):  # buscaqr
        return self.__atributos_culturales[id_buscar]
        
    def elmininar_atributo(self, id_eliminar): # eliminar
        self.__atributos_culturales.pop(id_eliminar)
    #////////////////////////////////////////////////////////

    @property
    def arqueologo(self):
        return  self.__arqueologo
    def __str__(self) -> str:
        print("atributos culturales: ")
        [print(cultura) for cultura in self.atributos_cultural]
        return f"""
            id cultura: {self.id}
            nombre:  {self.nombre}
            Arqueologo: {self.arqueologo.nombre}
            """
class PiezaArqueologica:
    def __init__(self, id, nombre, nombre_cultura, id_cultura, nombre_arqueologo, campamentos) -> None:
        self.__idPieza = id
        self.__nombre = nombre
        self.__cultura = Cultura(id_cultura, nombre_cultura, nombre_arqueologo, campamentos)
    
    
    @property
    def id(self):
        return self.__idPieza
    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def set_nombre(self, nuevo):
        self.__nombre = nuevo
    @property
    def cultura(self):
        return self.__cultura
    def __str__(self) -> str:
        return f"""
        id : {self.id}
        nomrbe :{self.nombre}
        """
class Museo:
    __id_piesas = 0
    __id_culturas = 0
    def __init__(self, id, Nombre) -> None:
        self.__piezas_arqueologicas = {}
        self.__idMuseo = id
        self.__nombre = Nombre

    @property
    def id(self):
        return self.__idMuseo
    @property
    def nombre(self):
        return self.__nombre
    @property
    def piezas_arqueologicas(self):
        return self.__piezas_arqueologicas.values()
#////////////////////////////////////////////////////////
    def agregar_pieza(self): # agregar
        nombre_pieza=  input("Ingrese nombre pieza: ")
        cultura = input("Nombre cultura: ")
        nombre_arqueologo = input("Nombre arqueologo: ")
        capamentos = input("Campamentos del arqueologo: ")
        self.__piezas_arqueologicas[self.__id_piesas]= PiezaArqueologica(self.__id_piesas, nombre_pieza,cultura,
                                                                          self.__id_culturas, nombre_arqueologo, capamentos)
        self.__id_piesas+=1 
        self.__id_culturas+=1
    def eliminar_pieza(self, id_eliminar): # eliminar

        self.__piezas_arqueologicas.pop(id_eliminar)

    def acceder_pieza(self, id_buscar): # buscar
        return self.__piezas_arqueologicas[id_buscar]
#////////////////////////////////////////////////////////
        
class Manejador:
    __idmuseo = 0
    def __init__(self) -> None:
        self.__museos = {}

    def agregar_museo(self):
        self.__museos[self.__idmuseo]= Museo(self.__idmuseo, f"museo-{self.__idmuseo}")

    def menu_cultura(self, cultura):
        opcion= -1
        while not (opcion=='6'): 
            print("""
         1. modificar nombre cultura
         2. mostrar atributos culturales
         3. modificar nombre atributos culturales 
         4.  agregar atributo cultural
         5. acceder al arqueologo
        6. salir
                  
""") 
            opcion= input("[!]Ingrese su alternativa: ")
            match opcion:
                case '1':
                    cultura.set_nombre = input("Ingrese el nombre de la cultura: ")
                case '2':
                    for atributo in cultura.atributos_cultural:
                        print(atributo)
                case '3':
                    id_buscar = int(input("Ingrese el id del atributo: "))
                    try:
                        atributo = cultura.acceder_atributo(id_buscar)
                        atributo.set_nombre=  input("Ingrese nombre nuevo pal atributo: ")
                    except KeyError:
                        print("No existe el id agregar o verificar si existen ")
                case '4':
                    cultura.agregar_atributos_culturales()
                case '5':
                    arqueologo = cultura.arqueologo
                    print(arqueologo)
                    if input("Desea mdificar sus atributos?  S|N ").upper() == 'S':
                        arqueologo.set_name = input("Ingrese nombre del arqueologo: ")
                        try:
                            arqueologo.set_campamentos = int(input("Ingrese numero de campamentos"))
                        except Exception:
                            pass

    def menu_pieza(self, pieza):
        opcion= -1
        while not (opcion=='3'): 
            print("""
         1. modificar nombre
         2. acceder a cultura de la pieza
        3. Salir
""")
            opcion= input("[!]Ingrese su alternativa: ")
            match opcion:
                case '1':
                    pieza.set_nombre= input("Ingrese nombre de la pieza")
                case '2':
                    self.menu_cultura(pieza.cultura)
                    

    def usar_museo(self, id_museo):
        museo_trabajar = None
        for  museo in self.__museos.values():
            if id_museo == museo.id:
                museo_trabajar = museo
                break
        opcion= -1
        while not (opcion=='4'):
            print("""
            1. agregar_pieza
            2. acceder_pieza 
            3. eliminar_pieza
            4. Salir
                  """)
            opcion= input("[!]Ingrese su alternativa: ")
            match opcion:
                case '1':
                    museo_trabajar.agregar_pieza()
                case '2':
                    for pieza in museo_trabajar.piezas_arqueologicas:
                        print(pieza)
                        
                    id_buscar = int(input("Ingrese el id de la pieza: "))
                    pieza = museo_trabajar.acceder_pieza(id_buscar)
                    self.menu_pieza(pieza)
                case '3':
                    id_buscar = int(input("Ingrese el id de la pieza: "))
                    museo_trabajar.eliminar_pieza(id_buscar)
        
man = Manejador()
man.agregar_museo()
man.usar_museo(0) # agrego 0 ya que es el id del unico museo delmanejado
