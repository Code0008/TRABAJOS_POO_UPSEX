import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Pregunta2:
    def __init__(self) -> None:
        self.__dataframe = pd.DataFrame()

    @property
    def dataframe(self):
        return self.__dataframe
    
    def leer_y_monstrar(self):
        self.__dataframe= pd.read_excel("entradas.xlsx", sheet_name="entradas")
        self.__dataframe.set_index("IDENTRADA", inplace=True)
        print(self.__dataframe.to_string())
    def mostrar_total_de_ventas_por_edad(self):
        agrupamos_por_edad = self.__dataframe[["Edad", "TotalVenta"]].groupby(by="Edad").sum() # contemplamos si hay edades repetidas
        print(agrupamos_por_edad.to_string())
    def mostrar_grafico_pastel(self):
        agrupamos_por_edad = self.__dataframe[["Edad", "TotalVenta"]].groupby(by="Edad").sum() # contemplamos si hay edades repetidas
        labels = [f"Edad-{edad}" for edad in agrupamos_por_edad.index]
        plt.figure(figsize=(15,15))
        plt.title("GRAFICO PASTEL PORCENTAJE VENTAS EDAD")
        plt.pie(agrupamos_por_edad["TotalVenta"], labels=labels, autopct='%1.1f%%')
        plt.legend()
        plt.show()
    def  mostrar_total_ventas_por_tipo_entrada(self):
        agrupamos = self.__dataframe[["TipoDeEntrada", "TotalVenta"]].groupby(by="TipoDeEntrada").sum()
        print(agrupamos.to_string())

    def generar_archivo_csv(self):
        self.__dataframe[["TipoDeEntrada","TotalVenta"]].to_csv("entradas.csv")


    def menu(self):
        opcion = -1
        while not (opcion=='6'):
            print(F"""
                1. leer y mostar  datos
                2. mostrar total de ventas por edad
                3. mostrar pastelaso
                4. mostrar total ventas por tipo entrada
                5. generar archivo csv
                6. salir del programa
                    """)    
            opcion = input("[+] Ingrese su seleccion : ")
            if self.dataframe.empty:
                print("No olvide cargar los datos primero")
            try:
                match opcion:
                    case '1':
                        self.leer_y_monstrar()
                    case '2':
                        self.mostrar_total_de_ventas_por_edad()
                    case '3':
                        self.mostrar_grafico_pastel()
                    case '4':
                        self.mostrar_total_ventas_por_tipo_entrada()
                    case '5':
                        self.generar_archivo_csv()
                    case _:
                        print("Opcion incorrecta")
            except Exception:
                pass
preg = Pregunta2()
preg.menu() 
