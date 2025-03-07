import streamlit as st
import pandas as pd
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
            self.__rendimiento.to_csv(nombre_rendimiento, index=False)
            print(f"Datos de rendimiento exportados a: {nombre_rendimiento}")

            self.__satisfacion.to_excel(nombre_satisfaccion, sheet_name="Sheet1", index=False)
            print(f" Datos de satisfacción exportados a: {nombre_satisfaccion}")

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
                legend.append(f"satisfaccion-{key}-{anio_a+indice}")
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


def agregar_datos(df, tipo_datos):
    st.subheader(" Agregar Nuevos Datos")

    if tipo_datos == "satisfaccion":
        columnas = ["Año", "Universidad", "Videojuego Educativo", "Satisfacción (%)", "Tasa de Retención (%)"]
    elif tipo_datos == "rendimiento":
        columnas = ["Año", "Universidad", "Videojuego Educativo", "Estudiantes (n)", "Rendimiento Promedio (%)"]

    nuevo_dato = {}
    nuevo_dato["Año"] = st.number_input(" Año 2015-2021", min_value=2015, max_value=2021, value=2021, step=1)

    universidades_existentes = df["Universidad"].unique().tolist() if "Universidad" in df.columns else []
    if universidades_existentes:
        nuevo_dato["Universidad"] = st.selectbox(" Seleccione una Universidad:", universidades_existentes + ["Otro"])
        if nuevo_dato["Universidad"] == "Otra":
            nuevo_dato["Universidad"] = st.text_input(" Ingrese el nombre de la nueva universidad:")
    else:
        nuevo_dato["Universidad"] = st.text_input(" Ingrese el nombre de la universidad:")

    juegos_existentes = df[df["Universidad"]==nuevo_dato["Universidad"]]["Videojuego Educativo"].unique().tolist() 
    if juegos_existentes:
        nuevo_dato["Videojuego Educativo"] = st.selectbox("Seleccione Videojuego", juegos_existentes+ ["Otro"])
        if nuevo_dato["Videojuego Educativo"] == "Otro":
            nuevo_dato["Videojuego Educativo"] = st.text_input(" Nombre del nuevo Videojuego Educativo:")
    else:
        nuevo_dato["Videojuego Educativo"] = st.text_input(" Nombre del Videojuego Educativo:")

    if tipo_datos == "satisfaccion":
        nuevo_dato["Satisfacción (%)"] = st.number_input(" Porcentaje de Satisfacción:", 0, 100, 50)
        nuevo_dato["Tasa de Retención (%)"] = st.number_input(" Tasa de Retención (%):", 0, 100, 70)

    elif tipo_datos == "rendimiento":
        nuevo_dato["Estudiantes (n)"] = st.number_input(" Número de Estudiantes:", 1, 10000, 100)
        nuevo_dato["Rendimiento Promedio (%)"] = st.number_input(" Rendimiento Promedio (%):", 0, 100, 75)
    if st.button(" Agregar Datos"):
        nuevo_df = pd.DataFrame([nuevo_dato])
        df_actualizado = pd.concat([df, nuevo_df], ignore_index=True)
        return df_actualizado
    return df
    
def main():
    st.title(" Análisis de Datos Educativos")

    # Cargar datos
    datos = ImportarDatos()
    datos.cargar_datos()

    # Menú en la barra lateral
    menu_opcion = st.sidebar.radio(
        " Menú Principal", 
        ["Ver Datos", "Análisis de Dataframes", "Operaciones Estadísticas", 
         "Modelos Predictivos", "Agregar Datos", "Exportar Datos"]
    )

    if menu_opcion == "Ver Datos":
        st.subheader(" Datos Cargados")
        st.write("###  Rendimiento Académico")
        st.dataframe(datos.rendimiento)
        st.write("###  Satisfacción Estudiantil")
        st.dataframe(datos.satisfaccion)

    elif menu_opcion == "Análisis de Dataframes":
        analizador = AnalisisDataframes(datos)
        opcion = st.selectbox(" Seleccione un análisis:", [
            "Gráfico de Líneas - Rendimiento",
            "Gráfico de Barras - Satisfacción y Retención",
            "Gráfico de Dispersión - Videojuegos vs Rendimiento",
            "Gráfico de Pastel - Distribución de Satisfacción"
        ])
        
        if opcion == "Gráfico de Líneas - Rendimiento":
            años = st.slider(" Seleccione el rango de años:", 2015, 2021, (2015, 2021))
            analizador.GrafLinRenAc(años[0], años[1])

        elif opcion == "Gráfico de Barras - Satisfacción y Retención":
            años = st.slider(" Seleccione el rango de años:", 2015, 2021, (2015, 2021))
            universidades = st.multiselect(" Seleccione universidades:", datos.rendimiento["Universidad"].unique())
            if universidades:
                analizador.GrafBarCompSatisTasa(años[0], años[1], universidades)

        elif opcion == "Gráfico de Dispersión - Videojuegos vs Rendimiento":
            universidad = st.selectbox(" Seleccione una universidad:", datos.rendimiento["Universidad"].unique())
            analizador.GrafDispRelVidjuegRend(universidad)

        elif opcion == "Gráfico de Pastel - Distribución de Satisfacción":
            año = st.slider(" Seleccione un año:", 2015, 2021, 2015)
            analizador.GrafPasterlDistrSatis(año)

    elif menu_opcion == "Operaciones Estadísticas":
        estadisticas = OperacionesEstadisticas(datos)
        opcion = st.selectbox(" Seleccione una operación:", [
            "Medidas de Tendencia Central",
            "Medidas de Dispersión",
            "Correlación y Covarianza",
            "Distribución de Datos"
        ])

        if opcion == "Medidas de Tendencia Central":
            rendimiento, satisfaccion = estadisticas.tendencia_central()
            st.write(" **Medidas de Tendencia Central**")
            st.write(f" **Rendimiento:** Media: {rendimiento['Media']}, Mediana: {rendimiento['Mediana']}, Moda: {rendimiento['Moda']}")
            st.write(f" **Satisfacción:** Media: {satisfaccion['Media']}, Mediana: {satisfaccion['Mediana']}, Moda: {satisfaccion['Moda']}")

        elif opcion == "Medidas de Dispersión":
            rendimiento, satisfaccion = estadisticas.dispersion()
            st.write(" **Medidas de Dispersión**")
            st.write(f" **Rendimiento:** Varianza: {rendimiento['Varianza']}, Desviación Estándar: {rendimiento['Desviacion Estandar']}")
            st.write(f" **Satisfacción:** Varianza: {satisfaccion['Varianza']}, Desviación Estándar: {satisfaccion['Desviacion Estandar']}")

        elif opcion == "Correlación y Covarianza":
            estadisticas.correlacion_covarianza()

        elif opcion == "Distribución de Datos":
            estadisticas.analisis_distribucion()

    elif menu_opcion == "Modelos Predictivos":
        modelos = AnalisisModelosPredictivos(datos)
        opcion = st.selectbox(" Seleccione un modelo:", ["Regresión Lineal", "Árbol de Decisión"])

        universidad = st.selectbox(" Seleccione una universidad:", datos.rendimiento["Universidad"].unique())

        if opcion == "Regresión Lineal":
            modelos.regresion_lineal(universidad)
        elif opcion == "Árbol de Decisión":
            modelos.arbol(universidad)

    elif menu_opcion == "Agregar Datos":
        tipo_datos = st.radio(" ¿Qué datos desea agregar?", ["Satisfacción", "Rendimiento"])
        if tipo_datos == "Satisfacción":
            datos.actualizar_rend = agregar_datos(datos.rendimiento, "satisfaccion")

        else:
            datos.actualizar_satis = agregar_datos(datos.satisfaccion, "rendimiento")
        
    elif menu_opcion == "Exportar Datos":
        nombre_rend = st.text_input(" Nombre del archivo de rendimiento:", "rendimiento_exportado.csv")
        nombre_satis = st.text_input(" Nombre del archivo de satisfacción:", "satisfaccion_exportado.xlsx")

        if st.button("Exportar Datos"):
            datos.exportar_datos(nombre_rend, nombre_satis)

if __name__ == '__main__':
    main()
