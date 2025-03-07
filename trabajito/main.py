import streamlit as st
from funciones_principales import ImportarDatos, AnalisisDataframes, OperacionesEstadisticas, AnalisisModelosPredictivos
import pandas as pd
def agregar_datos(df, tipo_datos):
    st.subheader("📝 Agregar Nuevos Datos")

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
    if st.button("✅ Agregar Datos"):
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
