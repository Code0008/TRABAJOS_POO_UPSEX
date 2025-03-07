import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

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
            return {"Varianza": round(columna.var(),2) , 
                    "Desviacion Estandar": round(columna.std(),2)}
        datos_rendimiento = self.datos.rendimiento
        datos_satis = self.datos.satisfaccion

        return calcular_dispercion(datos_rendimiento["Rendimiento Promedio (%)"]),  calcular_dispercion(datos_satis["Satisfacción (%)"])

    
    def correlacion_covarianza(self):
        plt.title("Matriz de Correlación - Heatmap")
        datos_rendimiento = self.datos.rendimiento[['Estudiantes (n)',
       'Rendimiento Promedio (%)']]
        sns.heatmap( datos_rendimiento.corr(), annot=True, cmap="coolwarm")
        st.pyplot()

    def analisis_distribucion(self):
        datos_rendimiento = self.datos.rendimiento[['Rendimiento Promedio (%)']]
        datos_rendimiento.hist(grid=True)
        st.pyplot()


class AnalisisDataframes:
    def __init__(self, datos):
        self.__datos =  datos
    @property
    def datos(self):
        return self.__datos
    
    def GrafLinRenAc(self, anio_a, anio_b):
        fig,ax = plt.subplots()
        plt.title(f"GRAFICO DE LINEA DE {anio_a}-{anio_b}")
        data = self.datos.rendimiento.where((self.datos.rendimiento["Año"]<=anio_b) & (self.datos.rendimiento["Año"]>=anio_a)).dropna()
        
        for juego in data["Videojuego Educativo"].unique().tolist():
            juego_dat = data[data["Videojuego Educativo"]==juego]
            ax.plot(juego_dat["Año"], juego_dat["Rendimiento Promedio (%)"], label=juego_dat["Universidad"].unique())
        plt.legend()
        st.pyplot(fig)

    def GrafBarCompSatisTasa(self, anio_a,anio_b, universidades):
        fig,ax = plt.subplots()
        plt.title(f"COMPARACION SATISFACCION Y RETENCION UNIVERSIDADES {', '.join(universidades)} del año {anio_a} - {anio_b}")
        data = self.datos.satisfaccion.where((self.datos.rendimiento["Año"]<=anio_b) & (self.datos.rendimiento["Año"]>=anio_a)).dropna()
        legend = []
        for  key in universidades:
            universidad =  data[data["Universidad"]==key][["Año","Universidad","Satisfacción (%)","Tasa de Retención (%)"]]
            años =  universidad["Año"].unique().tolist()[::-1][0]
            for indice,valor in enumerate(universidad["Satisfacción (%)"].values.tolist()[::-1]):
                ax.bar(f"satisfaccion-{key}", valor)
                legend.append(f"satisfaccion-{key}-{años+indice}")
        plt.legend(legend)
        st.pyplot(fig)   

    def GrafDispRelVidjuegRend(self, universidad):
        fig,ax = plt.subplots()
        plt.title(f"COMPARACION NUMERO ESTUDIANTES Y RENDIMIENTO EN {universidad}")
        data = self.datos.rendimiento[self.datos.rendimiento["Universidad"]==universidad][["Estudiantes (n)", "Rendimiento Promedio (%)"]]
        ax.scatter(data["Estudiantes (n)"], data["Rendimiento Promedio (%)"])
        st.pyplot(fig)

    def GrafPasterlDistrSatis(self, año):
        fig,ax = plt.subplots()
        plt.title(f" DISTRIBUCION DE SATISFACCION EN EL {año}")
        data = self.datos.satisfaccion[self.datos.satisfaccion["Año"]==año]
        ax.pie(data["Satisfacción (%)"],labels=data["Universidad"].tolist(), autopct="%1.1f%%")
        plt.legend()
        st.pyplot(fig)

class AnalisisModelosPredictivos:
    def __init__(self, datos):
        self.__datos =  datos
    @property
    def datos(self):
        return self.__datos

    def regresion_lineal(self, universidad):
        fig,ax = plt.subplots()

        plt.title(f"""PREDICCIÓN DE SATISFACCIÓN EN RELACIÓN A LA 
                  CANTIDAD DE ALUMNOS EN {universidad} (2021-2025)""")

        datos = self.datos.rendimiento[self.datos.rendimiento["Universidad"] == universidad]
        ejeX = datos["Estudiantes (n)"].tolist()
        ejeY = datos["Rendimiento Promedio (%)"].tolist()

        X = np.array(ejeX)
        y = np.array(ejeY)

        X_mean = np.mean(X)
        y_mean = np.mean(y)

        numerador = np.sum((X - X_mean) * (y - y_mean))
        denominador = np.sum((X - X_mean) ** 2)
        angulo_uno = numerador / denominador
        angulo_cero = y_mean - angulo_uno * X_mean

        y_pred = angulo_cero + angulo_uno * X

        estudiantes_nuevos = [np.random.randint(100, 270) for _ in range(5)]
        y_pred_nuevos = [angulo_cero + angulo_uno * estudiante for estudiante in estudiantes_nuevos]

        ax.scatter(X, y, label="Data Orignal", color="blue")
        ax.plot(X, y_pred, label="Linea regresion", color="green")    
        ax.scatter(estudiantes_nuevos, y_pred_nuevos, label="Prediccion año 2021-2025", color="purple")
        ax.plot(estudiantes_nuevos, y_pred_nuevos, label="Linea predichos", color="red")

        plt.legend()
        st.pyplot(fig)

