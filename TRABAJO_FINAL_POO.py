import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from abc import ABC, abstractmethod


class Lector_Datos(ABC):
    def __init__(self):
        _migracion_internacional = pd.read_excel("caso9_migracion_internacional_clear.xlsx", sheet_name="hoja1", usecols=np.arange(0,21)).dropna().reset_index(drop=True) 

        self._dataframes = {
            "base_poblacion_proyectada": pd.read_csv("base_poblacion_proyectada2021.csv", sep=";") ,
            "salidas_segun_continente":  _migracion_internacional.iloc[1:12,:].set_axis(self.columnas(), axis="columns").reset_index(drop=True).drop([0], axis=0).reset_index(drop=True),
            "entradas_segun_continente":_migracion_internacional.iloc[12:,:].set_axis(self.columnas(), axis="columns").reset_index(drop=True).drop([0], axis=0).reset_index(drop=True) ,
        }

    def columnas(self, limite_A=2004, limite_B=2024):
        lista = np.arange(limite_A,limite_B).tolist()
        lista.insert(0, "Contenido")
        return lista
    
    @property
    def base_poblacional_proyectada(self):
        return self._dataframes["base_poblacion_proyectada"]
    @property
    def salidas_segun_continente(self):
        return self._dataframes["salidas_segun_continente"]
    @property
    def entradas_segun_continente(self):
        return self._dataframes["entradas_segun_continente"]
    @property
    def dataframes(self):
        return self._dataframes

class Exportador_de_Datos(Lector_Datos):
    def __init__(self):
        super().__init__()
        self.__validadores = Validadores()
        
        
    def exportar_salidas(self, *columnas):
        self.salidas_segun_continente.to_csv("Salidas_mod.csv")
    
    def ver_todos_los_dataframes(self):
        for dataframe in self.dataframes.values():
            print(dataframe)
class Reportes_Graficos(Lector_Datos):
    __fig, __axs = plt.subplots(1,3, figsize=(21,20))
    __fig.set_size_inches(80,14)
    __descripciones_graficos =  """
                1. Lineas tendencia (Entradas Salidas):
                    Muestra las lineas de tendencia de salida o entrada de los continentes de acuerdo a un rango de años
                2. Grafico de barras continente:
                    representa las entradas y salidad del año 2023 de continente que eligamos
                3. Grafico de barras horizontales continente:
                    representa las entradas y salidad del año 2021 de continente que eligamos
                """

    def __init__(self):
        [self.__axs[indice].set_visible(False) for indice in range(0, 3) ]
        super().__init__()
    @property
    def descripciones_graficos(self):
        return self.__descripciones_graficos        
    def graficador_lineas_tendencias(self, dataframe, ano_A, ano_B, ):
        # soe = 0 -> salida
        # soe = 1-> entrada
        match dataframe:
            case 'S':
                self.__axs[0].set_title(f"SALIDAS")
                dataframe = self.salidas_segun_continente
            case 'E':
                self.__axs[0].set_title(f"ENTRADA")
                dataframe = self.entradas_segun_continente
        # al ser funciones de unica diferencia los dataframe haremos una unica funcion para graficar ambos reportes (1,2)
        indices = list(range(dataframe.columns.to_list().index(ano_A), dataframe.columns.to_list().index(ano_B)+1))
        filtracion_datos = dataframe.iloc[:,indices]
        valores_continentes = [ filtracion_datos.where(dataframe["Contenido"]==valor).dropna().iloc[0]/100 for valor in dataframe.iloc[np.arange(0,7).tolist(), 0]]
        leyenda = []
        for indice, valor in enumerate(valores_continentes):
            self.__axs[0].plot(np.arange(ano_A, ano_B+1).tolist(),valor)
            leyenda.append(f"{dataframe.iloc[indice, 0]}")
        self.__axs[0].legend(leyenda)
        self.__axs[0].set_ylabel("Milliones de salida")
        self.__axs[0].set_xlabel("Año")
        self.__axs[0].set_visible(True)
    def graficar_barras_continente(self,continente):
        datos = [
            [self.salidas_segun_continente.where(self.salidas_segun_continente["Contenido"]==continente).dropna()[2023],
            self.entradas_segun_continente.where(self.entradas_segun_continente["Contenido"]==continente).dropna()[2023] ],
            ["Salidas", 
            "Entradas" ]
        ]
        for indice in range(len(datos)):
            self.__axs[2].bar(datos[1][indice], datos[0][indice])
        self.__axs[2].legend(["Salida", "Entrada"])
        self.__axs[2].set_visible(True)

    def graficar_barras_continente_diago(self, continente):
        ano = 2021
        salidas_continente = self.salidas_segun_continente.where(self.salidas_segun_continente["Contenido"]==continente).dropna()
        entradas_continente = self.entradas_segun_continente.where(self.entradas_segun_continente["Contenido"]==continente).dropna()
        #axs[2].bar(x= salidas_continente.columns,  height = salidas_continente.iloc[0:, :] )
        self.__axs[3].barh("Salidas",  salidas_continente[ano])
        self.__axs[3].barh("Entradas",  entradas_continente[ano])
        self.__axs[3].set_visible(True)



class Reportes_Estadisticos(Lector_Datos):
    def __init__(self):
        super().__init__()

class Validadores:
    def validar_enteros(self, limite_a, limite_b, mensaje):
        entrada = -1

        while not((limite_a<= entrada <= limite_b ) and type(entrada)==int):
            entrada = int(input(f"[!] Ingrese {mensaje}"))

        return entrada

    def validar_opciones_multiples(self, *opciones, mensaje, mensaje_opciones):
        
        entrada = -1
        while not (entrada in opciones):
            for indice, msg in enumerate(mensaje_opciones):
                print(f"{msg} : {opciones[indice]}")
            entrada = input(f"Ingrese {mensaje}")
        return entrada
    
class Menu_Principal:
    __NOMBRE_TRABAJO_FINAL = "INSANINES"
    def __init__(self) -> None:
        self.__reporte_graficos = Reportes_Graficos()
#        self.__reporte_estadisticos = Reportes_Estadisticos()
        self.__exportador_de_datos = Exportador_de_Datos()
        self.__validadores = Validadores()

    def menu_mostrar_datasets(self):

        entrada = -1
        while not (entrada == 3 ):
                print(f"""
            Actualmente tenemos {len(self.__exportador_de_datos.dataframes)} datasets
            con las opcioens de {self.__exportador_de_datos.dataframes.keys()}
            1. Selecciona dataframe
            2. Ver todos los dataframes
            3. Salir pe telen                
        """)    
                entrada = self.__validadores.validar_enteros(limite_a=1, limite_b=3, mensaje="seleccione opcion a visualizar: ")
                match entrada:
                    case 1:
                        entrada = self.__validadores.validar_opciones_multiples('BSP',"SSC", "ESC" ,mensaje="Seleccione una opcion: ", mensaje_opciones=self.__exportador_de_datos.dataframes.keys())
                        match entrada:
                            case 'BSP':
                                print(self.__exportador_de_datos.base_poblacional_proyectada)
                            case 'SSC':
                                print(self.__exportador_de_datos.salidas_segun_continente)
                            case 'ESC':
                                print(self.__exportador_de_datos.salidas_segun_continente)
                    case 2:
                        self.__exportador_de_datos.ver_todos_los_dataframes()

    def menu_graficos(self):
        print(f"""
        {self.__reporte_graficos.descripciones_graficos}
                        """)
        entrada =  -1
        while not(entrada == 5):
            print(f"""
                1. Lineas salida
                2. Linea entrada 
                3. Barras continente
                4 Barras horizontales
                5. salir
                    """)    
            entrada  =  self.__validadores.validar_enteros(limite_a=1, limite_b=4, mensaje="Seleccion grafico: ")
            match entrada:
                case 1:
                    pass


    def menu_principal(self):
        opcion = -1
        while not ( opcion == 5):
            print(f"""
        Bienvenido al proyecto {self.__NOMBRE_TRABAJO_FINAL}:
        opciones:
            1. Mostrar Datasets disponibles
            2. Menu Graficos
            3. Menu Estadisticas
            4. Menu Exportar datos
            5. Salir programa 
                """)
            opcion =  self.__validadores.validar_enteros(limite_a=0, limite_b=5, mensaje="Ingrese opcion: ")

            match opcion:
                case 1:
                    self.menu_mostrar_datasets()
                case 2:
                    pass



plt.show()
