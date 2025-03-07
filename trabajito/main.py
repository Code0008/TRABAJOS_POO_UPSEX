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
            print(f" Datos de satisfaccion exportados a: {nombre_satisfaccion}")

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
        return calcular_medidas(datos_rendimiento["Rendimiento Promedio (%)"]), calcular_medidas(datos_satis["Satisfaccion (%)"])
      
    
    def dispersion(self):
        def calcular_dispercion(columna):
            return {"Varianza": round(columna.var(),2) , 
                    "Desviacion Estandar": round(columna.std(),2)}
        datos_rendimiento = self.datos.rendimiento
        datos_satis = self.datos.satisfaccion

        return calcular_dispercion(datos_rendimiento["Rendimiento Promedio (%)"]),  calcular_dispercion(datos_satis["Satisfaccion (%)"])

    
    def correlacion_covarianza(self):
        st.subheader("MATRIZ DE CORRELACION - HEAT MAP")

        datos_rendimiento = self.datos.rendimiento[['Estudiantes (n)',
       'Rendimiento Promedio (%)']]
        plt.figure(figsize=(6,4))
        sns.heatmap( datos_rendimiento.corr(), annot=True, cmap="coolwarm")
        st.pyplot(plt)

    def analisis_distribucion(self):
        datos_rendimiento = self.datos.rendimiento[['Rendimiento Promedio (%)']]
        datos_rendimiento.hist(grid=True)
        st.pyplot(plt)


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
        fig,ax = plt.subplots(figsize=(15,15))
        plt.title(f"COMPARACION SATISFACCION Y RETENCION UNIVERSIDADES {', '.join(universidades)} del año {anio_a} - {anio_b}")
        data = self.datos.satisfaccion.where((self.datos.rendimiento["Año"]<=anio_b) & (self.datos.rendimiento["Año"]>=anio_a)).dropna()
        legend = []
        for  key in universidades:
            universidad =  data[data["Universidad"]==key][["Año", "Universidad", "Satisfaccion (%)", "Tasa de Retencion (%)"]]
            for indice,valor in enumerate(universidad["Satisfaccion (%)"].values.tolist()[::-1]):
                ax.bar(f"satisfaccion-{key}", valor)
                legend.append(f"satisfaccion-{key}-{anio_a+indice}")
        ax.legend(legend)
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
        ax.pie(data["Satisfaccion (%)"],labels=data["Universidad"].tolist(), autopct="%1.1f%%")
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

        plt.title(f"""PREDICCIoN DE SATISFACCIoN EN RELACIoN A LA 
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
    def media_movil(self, datos, ventana_años, universidad):
        data  = datos.satisfaccion[datos.satisfaccion["Universidad"]==universidad]
        años =  np.array(data["Año"].tolist()+[2021])
        random_satis = np.random.randint(80,100)
        satisfaccion = np.array(data["Satisfaccion (%)"].tolist()+[random_satis])
        
        media_movil = [np.mean(satisfaccion[i-ventana_años:i]) if i >=ventana_años else None for i in range(len(satisfaccion)+1)]
        prediccion_siguiente = media_movil[-1]
        año_predicho=  años[-1]+1
        st.text(F"PREDICCION PARA EL 2022 CON UNA SATISFACCION DE {random_satis} ")
        plt.figure(figsize=(15,15))
        plt.plot(años, satisfaccion, marker='x', label = "Satisfaccion Real")
        plt.plot(años[ventana_años-1:], media_movil[ventana_años-1:-1], marker="s", label = f"Prediccion {año_predicho}: {round(prediccion_siguiente, 2)}% ")
        plt.xlabel("Año")
        plt.ylabel("Satisfaccion (%)")
        plt.legend()
        st.pyplot(plt)
        
        


def agregar_datos(df, tipo_datos):
    st.subheader(" Agregar Nuevos Datos")

    if tipo_datos == "satisfaccion":
        columnas = ["Año", "Universidad", "Videojuego Educativo", "Satisfaccion (%)", "Tasa de Retencion (%)"]
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
        nuevo_dato["Satisfaccion (%)"] = st.number_input(" Porcentaje de Satisfaccion:", 0, 100, 50)
        nuevo_dato["Tasa de Retencion (%)"] = st.number_input(" Tasa de Retencion (%):", 0, 100, 70)

    elif tipo_datos == "rendimiento":
        nuevo_dato["Estudiantes (n)"] = st.number_input(" Numero de Estudiantes:", 1, 10000, 100)
        nuevo_dato["Rendimiento Promedio (%)"] = st.number_input(" Rendimiento Promedio (%):", 0, 100, 75)
    if st.button(" Agregar Datos"):
        nuevo_df = pd.DataFrame([nuevo_dato])
        df_actualizado = pd.concat([df, nuevo_df], ignore_index=True)
        return df_actualizado
    return df
    



class MenuManejador():
    def __init__(self):
        pass
    def main(self):
        st.title(" Analisis de Datos Educativos")

        # Cargar datos
        datos = ImportarDatos()
        datos.cargar_datos()

        # Menu en la barra lateral
        menu_opcion = st.sidebar.radio(
            " Menu Principal", 
            ["Ver Datos", "Analisis de Dataframes", "Operaciones Estadisticas", 
            "Modelos Predictivos", "Agregar Datos", "Exportar Datos"]
        )

        if menu_opcion == "Ver Datos":
            st.subheader(" Datos Cargados")
            st.write("###  Rendimiento Acadamico")
            st.dataframe(datos.rendimiento)
            st.write("###  Satisfaccion Estudiantil")
            st.dataframe(datos.satisfaccion)

        elif menu_opcion == "Analisis de Dataframes":
            analizador = AnalisisDataframes(datos)
            opcion = st.selectbox(" Seleccione un analisis:", [
                "Grafico de Lineas - Rendimiento",
                "Grafico de Barras - Satisfaccion y Retencion",
                "Grafico de Dispersion - Videojuegos vs Rendimiento",
                "Grafico de Pastel - Distribucion de Satisfaccion"
            ])
            
            if opcion == "Grafico de Lineas - Rendimiento":
                años = st.slider(" Seleccione el rango de años:", 2015, 2021, (2015, 2021))
                analizador.GrafLinRenAc(años[0], años[1])

            elif opcion == "Grafico de Barras - Satisfaccion y Retencion":
                años = st.slider(" Seleccione el rango de años:", 2015, 2021, (2015, 2021))
                universidades = st.multiselect(" Seleccione universidades:", datos.rendimiento["Universidad"].unique())
                if universidades:
                    analizador.GrafBarCompSatisTasa(años[0], años[1], universidades)

            elif opcion == "Grafico de Dispersion - Videojuegos vs Rendimiento":
                universidad = st.selectbox(" Seleccione una universidad:", datos.rendimiento["Universidad"].unique())
                analizador.GrafDispRelVidjuegRend(universidad)

            elif opcion == "Grafico de Pastel - Distribucion de Satisfaccion":
                año = st.slider(" Seleccione un año:", 2015, 2021, 2015)
                analizador.GrafPasterlDistrSatis(año)

        elif menu_opcion == "Operaciones Estadisticas":
            estadisticas = OperacionesEstadisticas(datos)
            opcion = st.selectbox(" Seleccione una operacion:", [
                "Medidas de Tendencia Central",
                "Medidas de Dispersion",
                "Correlacion y Covarianza",
                "Distribucion de Datos"
            ])

            if opcion == "Medidas de Tendencia Central":
                rendimiento, satisfaccion = estadisticas.tendencia_central()
                st.write(" **Medidas de Tendencia Central**")
                st.write(f" **Rendimiento:** Media: {rendimiento['Media']}, Mediana: {rendimiento['Mediana']}, Moda: {rendimiento['Moda']}")
                st.write(f" **Satisfaccion:** Media: {satisfaccion['Media']}, Mediana: {satisfaccion['Mediana']}, Moda: {satisfaccion['Moda']}")

            elif opcion == "Medidas de Dispersion":
                rendimiento, satisfaccion = estadisticas.dispersion()
                st.write(" **Medidas de Dispersion**")
                st.write(f" **Rendimiento:** Varianza: {rendimiento['Varianza']}, Desviacion Estandar: {rendimiento['Desviacion Estandar']}")
                st.write(f" **Satisfaccion:** Varianza: {satisfaccion['Varianza']}, Desviacion Estandar: {satisfaccion['Desviacion Estandar']}")

            elif opcion == "Correlacion y Covarianza":
                estadisticas.correlacion_covarianza()

            elif opcion == "Distribucion de Datos":
                estadisticas.analisis_distribucion()

        elif menu_opcion == "Modelos Predictivos":
            modelos = AnalisisModelosPredictivos(datos)
            opcion = st.selectbox(" Seleccione un modelo:", ["Regresion Lineal", "Media Movil"])

            universidad = st.selectbox(" Seleccione una universidad:", datos.rendimiento["Universidad"].unique())

            if opcion == "Regresion Lineal":
                modelos.regresion_lineal(universidad)
            elif opcion == "Media Movil":
                ventana_años =  st.number_input("Ingrese ventana_años", 3, 5, step=1)
                modelos.media_movil(datos,ventana_años,universidad)

        elif menu_opcion == "Agregar Datos":
            tipo_datos = st.radio(" ¿Que datos desea agregar?", ["Satisfaccion", "Rendimiento"])
            if tipo_datos == "Satisfaccion":
                datos.actualizar_rend = agregar_datos(datos.rendimiento, "satisfaccion")

            else:
                datos.actualizar_satis = agregar_datos(datos.satisfaccion, "rendimiento")
            
        elif menu_opcion == "Exportar Datos":
            nombre_rend = st.text_input(" Nombre del archivo de rendimiento:", "rendimiento_exportado.csv")
            nombre_satis = st.text_input(" Nombre del archivo de satisfaccion:", "satisfaccion_exportado.xlsx")

            if st.button("Exportar Datos"):
                datos.exportar_datos(nombre_rend, nombre_satis)

if __name__ == '__main__':
    manejador = MenuManejador()
    manejador.main()
