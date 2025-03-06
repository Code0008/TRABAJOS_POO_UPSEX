import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.tree import  DecisionTreeRegressor
from sklearn.tree import plot_tree
from sklearn.preprocessing import LabelEncoder 


class ImportarDatos:
    def __init__(self):
        self.__rendimiento = pd.DataFrame()
        self.__satisfacion = pd.DataFrame()
        

    def cargar_datos(self):
        self.__rendimiento =  pd.read_csv("rendimiento.csv")
        self.__satisfacion = pd.read_excel("satisfaccion.xlsx", sheet_name="Sheet1")
        
    @property
    def rendimiento(self):
        return self.__rendimiento
    @property
    def satisfaccion(self):
        return self.__satisfacion
    @rendimiento.setter
    def actualizar_rend(self, nuevodf):
        self.__rendimiento = nuevodf    
    @satisfaccion.setter
    def actualizar_satis(self, nuevodf):
        self.__satisfacion = nuevodf
    def exportar_datos(self, nombre_rendimiento="rendimiento.csv", nombre_satisfaccion="satisfaccion.xlsx"):
        try:
            # Exportar rendimiento a CSV
            self.__rendimiento.to_csv(nombre_rendimiento, index=False)
            print(f"Datos de rendimiento exportados a: {nombre_rendimiento}")

            # Exportar satisfacción a Excel
            self.__satisfacion.to_excel(nombre_satisfaccion, sheet_name="Sheet1", index=False)
            print(f"[✔] Datos de satisfacción exportados a: {nombre_satisfaccion}")

        except Exception as e:
            print(f"Error al exportar los datos: {e}")
    
class OperacionesEstadisticas:
    def __init__(self, datos):
        self.__datos =  datos


    @property
    def datos(self):
        return self.__datos
    
    def tendencia_central(self):
        def calcular_medidas(columna):
            return { "Media": round(columna.mean(),2),
                    "Mediana":round(columna.median(),2),
                    "Moda": columna.mode().values.tolist()}
        datos_rendimiento = self.datos.rendimiento
        datos_satis = self.datos.satisfaccion
        return calcular_medidas(datos_rendimiento["Rendimiento Promedio (%)"]), calcular_medidas(datos_satis["Satisfacción (%)"])
      
    
    def dispersion(self):
        def calcular_dispercion(columna):
            return {"Varianza": columna.var() , 
                    "Desviacion Estandar": columna.std}
        datos_rendimiento = self.datos.rendimiento
        datos_satis = self.datos.satisfaccion

        return calcular_dispercion(datos_rendimiento["Rendimiento Promedio (%)"]),  calcular_dispercion(datos_satis["Satisfacción (%)"])

    
    def correlacion_covarianza(self):
        plt.title("Matriz de Correlación - Heatmap")
        datos_rendimiento = self.datos.rendimiento[['Estudiantes (n)',
       'Rendimiento Promedio (%)']]
        sns.heatmap( datos_rendimiento.corr(), annot=True, cmap="coolwarm")
        plt.show()

    def analisis_distribucion(self):
        datos_rendimiento = self.datos.rendimiento[['Rendimiento Promedio (%)']]
        datos_rendimiento.hist(grid=True)
        plt.show()


class AnalisisDataframes:
    def __init__(self, datos):
        self.__datos =  datos
    @property
    def datos(self):
        return self.__datos
    
    def GrafLinRenAc(self, anio_a, anio_b):
        plt.title(f"GRAFICO DE LINEA DE {anio_a}-{anio_b}")
        data = self.datos.rendimiento.where((self.datos.rendimiento["Año"]<=anio_b) & (self.datos.rendimiento["Año"]>=anio_a)).dropna()
        
        for juego in data["Videojuego Educativo"].unique().tolist():
            juego_dat = data[data["Videojuego Educativo"]==juego]
            plt.plot(juego_dat["Año"], juego_dat["Rendimiento Promedio (%)"], label=juego_dat["Universidad"].unique())
        plt.legend()
        plt.show()

    def GrafBarCompSatisTasa(self, anio_a,anio_b, universidades):
        plt.title(f"COMPARACION SATISFACCION Y RETENCION UNIVERSIDADES {', '.join(universidades)} del año {anio_a} - {anio_b}")
        data = self.datos.satisfaccion.where((self.datos.rendimiento["Año"]<=anio_b) & (self.datos.rendimiento["Año"]>=anio_a)).dropna()
        legend = []
        for  key in universidades:
            universidad =  data[data["Universidad"]==key][["Año","Universidad","Satisfacción (%)","Tasa de Retención (%)"]]
            años =  universidad["Año"].unique().tolist()[::-1]
            for indice,valor in enumerate(universidad["Satisfacción (%)"].values.tolist()[::-1]):
                plt.bar(f"satisfaccion-{key}", valor)
                legend.append(f"satisfaccion-{key}-{años[indice]}")
        plt.legend(legend)
        plt.show()
        
    def GrafDispRelVidjuegRend(self, universidad):
        plt.title(f"COMPARACION NUMERO ESTUDIANTES Y RENDIMIENTO EN {universidad}")
        data = self.datos.rendimiento[self.datos.rendimiento["Universidad"]==universidad][["Estudiantes (n)", "Rendimiento Promedio (%)"]]
        plt.scatter(data["Estudiantes (n)"], data["Rendimiento Promedio (%)"])
        plt.show()

    def GrafPasterlDistrSatis(self, año):
        plt.title(f" DISTRIBUCION DE SATISFACCION EN EL {año}")
        data = self.datos.satisfaccion[self.datos.satisfaccion["Año"]==año]
        plt.pie(data["Satisfacción (%)"],labels=data["Universidad"].tolist(), autopct="%1.1f%%")
        plt.legend()
        plt.show()

class AnalisisModelosPredictivos:
    def __init__(self, datos):
        self.__datos =  datos
    @property
    def datos(self):
        return self.__datos

    def regresion_lineal(self, universidad):
        plt.title(f"""PREDICION DE SATISFACCION EN RELACION A LA 
                  CANTIDAD ALUMNOS EN LA {universidad} en los años
                                 2021-2025""")
        lin_reg = LinearRegression()
        datos = self.datos.rendimiento[self.datos.rendimiento["Universidad"]==universidad]
        ejeX= datos["Estudiantes (n)"].tolist()
        ejeY = datos["Rendimiento Promedio (%)"].tolist()
        lin_reg.fit(np.array(ejeX).reshape(-1,1), 
                    np.array(ejeY).reshape(-1,1))
        estudiantes = [np.random.randint(100,270) for _ in range(2021,2025 )]
        predecir = lin_reg.predict(np.array(estudiantes).reshape(-1,1)).tolist()
        plt.scatter(estudiantes, [round(valor[0]) for valor in predecir], label="PREDICCION", c="r")
        plt.scatter(ejeX, ejeY, label="DATA ORIGINALES")
        plt.plot(ejeX+estudiantes, lin_reg.predict(np.array(ejeX+estudiantes).reshape(-1,1)).tolist(),label="linea ajustada", c="b")
        plt.legend()
        plt.show()

    def arbol(self, universidad):
        tokenizadorAño = LabelEncoder()
        tokenizadorUni = LabelEncoder()
        tokenizadorVid = LabelEncoder()
        datos = self.datos.satisfaccion[self.datos.satisfaccion["Universidad"]==universidad]
        ejeX= datos.drop(columns=["Tasa de Retención (%)"])
        ejeX["Año"] = tokenizadorAño.fit_transform(ejeX["Año"])
        ejeX["Universidad"] = tokenizadorUni.fit_transform(ejeX["Universidad"])
        ejeX["Videojuego Educativo"] = tokenizadorVid.fit_transform(ejeX["Videojuego Educativo"])
        ejeY = datos["Tasa de Retención (%)"]
        modelo_arbol = DecisionTreeRegressor( random_state=42)
        modelo_arbol.fit(ejeX, ejeY)
        plot_tree(modelo_arbol, filled=True, feature_names=ejeX.columns.tolist())
        plt.show()
        

