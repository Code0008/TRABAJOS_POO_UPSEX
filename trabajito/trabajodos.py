import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
    def validar_opciones_multiples_int(cls, opciones, mensaje):
        entrada = -1
        for indice, opcion  in enumerate(opciones):
             print(indice,"|",opcion)
        while not (entrada in opciones):
            try:
                entrada = int(input(mensaje))
            except ValueError:
                pass
        return entrada
        

class CargaDatos():
    def __init__(self):
        self.__data = pd.read_excel("Metas_ODS6_Transformado.xlsx")
    
    @property
    def data(self):
        return self.__data
    
    def exportar_datos(self, nombre_archivo):
        self.__data.to_excel(nombre_archivo, index=False)
        print(f"Datos exportados a {nombre_archivo}")

class AnalisisAgua:
    def __init__(self, data_agua=pd.DataFrame()):
        self.__data_agua = data_agua
        #
    @property
    def data_agua(self):
        return self.__data_agua
    @data_agua.setter
    def set_data_agua(self, dataframe):
        self.__data_agua = dataframe
        self.__data_agua = self.__data_agua.fillna(np.nan)

    def graficar_lineas(self, anio_a, anio_b):
        data_agua_filtrado = self.__data_agua[["N° Meta", "Indicador", f"Año-{anio_a}", f"Año-{anio_b}"]].dropna()
        
        plt.figure(figsize=(10, 5))
        for _, fila in data_agua_filtrado.iterrows():
            plt.plot([anio_a, anio_b], [fila[f"Año-{anio_a}"], fila[f"Año-{anio_b}"]], marker='o', label=fila["Indicador"])
        
        plt.xlabel("Año")
        plt.ylabel("Porcentaje/Valor")
        plt.title("Tendencia del Agua y Saneamiento")
        plt.legend()
        plt.show()
    
    def graficar_barras_vertical(self):
        año = Validadores.validar_opciones_multiples_int([2015, 2019, 2022], "[!]Ingrese el año a ver:")
        data_agua_promedios = self.__data_agua[["N° Meta", "Indicador", f"Año-{str(año)}"]].dropna()
        data_agua_promedios.set_index("Indicador").plot(kind='bar', figsize=(20,20))
        plt.title("Comparación por Año - Barras Verticales")
        plt.ylabel("Porcentaje/Valor")
        plt.xlabel("Indicadores")
        plt.tick_params("y",  rotation=45)
        plt.xticks(rotation=90)
        plt.show()
    
    def graficar_barras_horizontal(self):
        año = Validadores.validar_opciones_multiples_int([2015, 2019, 2022], "[!]Ingrese el año a ver:")
        data_agua_promedios = self.__data_agua[["N° Meta", "Indicador", f"Año-{año}"]].dropna()
        data_agua_promedios.set_index("Indicador").plot(kind='barh', figsize=(20,20))
        plt.tick_params("y",  rotation=45)
        plt.title("Comparación por Año - Barras Horizontales")
        plt.xlabel("Porcentaje/Valor")
        plt.ylabel("Indicadores")
        plt.show()
    
    def regresion_lineal(self, indicador):
     
        datos = self.__data_agua[self.__data_agua["Indicador"] == indicador][["Año-2015", "Año-2019", "Año-2022"]].dropna(axis=1).values.flatten()
        anios = np.array([2015, 2019, 2022])
        
        n = len(anios)
        sum_x,sum_y  = sum(anios),sum(datos)
        sum_xy,sum_x2  = sum(anios * datos),sum(anios ** 2)
        
        pendiente = ((n * sum_xy) - (sum_x * sum_y)) / ((n * sum_x2) - (sum_x ** 2))
        intercepto = (sum_y - pendiente * sum_x) / n

        anios_prediccion = np.array(range(2023, 2028))
        predicciones = pendiente * anios_prediccion + intercepto

        datos_linea = pendiente * anios + intercepto
        print(anios, datos)
        plt.figure(figsize=(8, 5))
        plt.scatter(anios, datos, color='red', label="Datos")
        plt.plot([2015,2019,2022]+anios_prediccion.tolist(), datos_linea.tolist()+predicciones.tolist(), color='blue', label="Linea ajustada")
        plt.scatter(anios_prediccion, predicciones, color='purple', label="datos predichoos")

        plt.xlabel("Año")
        plt.ylabel("Porcentaje/Valor")
        plt.title(f"Regresión Lineal - {indicador}- predicciones 2023-2028")
        plt.legend()
        plt.grid(True, linestyle='--')
        plt.show()

    

    def analisis_distribucion(self):
        anio = Validadores.validar_opciones_multiples_int([2015,2019,2022], "[!!] Ingrese año que quiera ver: ")
        anio =  "Año-"+str(anio)
        
        data_anio = self.__data_agua[anio].dropna()
            
        plt.figure(figsize=(8, 5))
        plt.hist(data_anio, bins=10, alpha=0.75, color='blue', edgecolor='black')
        plt.xlabel("Porcentaje/Valor")
        plt.ylabel("Frecuencia")
        plt.title(f"Distribución de valores - {anio}")
        plt.grid(axis="y", linestyle="--")
        plt.show()

    def graficar_lineas_salida(self, anio_a, anio_b):
        data_filtrado = self.__data_agua[["Indicador", f"Año-{anio_a}", f"Año-{anio_b}"]].dropna()
        
        plt.figure(figsize=(10, 5))
        for _, fila in data_filtrado.iterrows():
            plt.plot([anio_a, anio_b], [fila[f"Año-{anio_a}"], fila[f"Año-{anio_b}"]], marker='s', linestyle='dashed', label=fila["Indicador"])
        
        plt.xlabel("Año")
        plt.ylabel("Porcentaje de Salida")
        plt.title("Tendencia de Salida del Agua")
        plt.legend()
        plt.show()
 
    def graficar_lineas_entrada(self, anio_a, anio_b):
        data_filtrado = self.__data_agua[["Indicador", f"Año-{anio_a}", f"Año-{anio_b}"]].dropna()
        
        plt.figure(figsize=(10, 5))
        for _, fila in data_filtrado.iterrows():
            plt.plot([anio_a, anio_b], [fila[f"Año-{anio_a}"], fila[f"Año-{anio_b}"]], marker='o', label=fila["Indicador"])
        
        plt.xlabel("Año")
        plt.ylabel("Porcentaje de Entrada")
        plt.title("Tendencia de Entrada del Agua")
        plt.legend()
        plt.show()

class Manejador():
    def __init__(self):
        self.__analizador_agua = AnalisisAgua()

    def Menu(self):
        #self.__analizador_agua.graficar_lineas(2015, 2019)
        try:
            carga = CargaDatos()
            self.__analizador_agua.set_data_agua = carga.data
            print(carga.data)
        except Exception as e:
            print(F"OCURRIO UN ERROR {e}")
        else:
            while True:
                print(f"""
                    1. Grafico de lineas por año
                    2. Grfico de barras vertical
                    3. Grafico de barras horizontal
                    4. Regresion lineal
                    5. analisis distribucion 
                    """)
                
                match Validadores.validarEntero(1,6,"[!] INGRESE SU OPCION: "):
                    case 1:
                        año_a =  Validadores.validar_opciones_multiples_int([2015,2019,2022], "[!] Ingrese año a: ")
                        año_b =  Validadores.validar_opciones_multiples_int([2015,2019,2022], "[!] Ingrese año b: ")
                        match Validadores.validar_opciones_multiples_int([1,2], "[!]Seleccione grafico de lineas 1.Entrada| 2.Salida: "):
                            case 1: self.__analizador_agua.graficar_lineas_entrada(año_a, año_b)
                            case 2: self.__analizador_agua.graficar_lineas_salida(año_a, año_b)

                    case 2: self.__analizador_agua.graficar_barras_vertical()
                    case 3:self.__analizador_agua.graficar_barras_horizontal()
                    case 4:self.__analizador_agua.regresion_lineal("Proporción de la población que dispone de agua por red pública")
                    case 5: self.__analizador_agua.analisis_distribucion()
                    case 6: 
                        try:
                            nombre = input("Solicitud del nuevo nombre de archivo: ")
                        except Exception:
                            print("Ocurrio un eror en el ingreso")
                        else:
                            carga.exportar_datos(nombre)


# Uso del programa
mane = Manejador()
mane.Menu()
