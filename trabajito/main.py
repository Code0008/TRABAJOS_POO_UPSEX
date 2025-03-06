from funciones_principales import *
import pandas as pd

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
    def validarString(cls, rangoA, rangoB, mensaje):
        entrada = ""
        while not ((rangoA < len(entrada) <= rangoB ) and not any([char.isdigit() for char in entrada])):
            entrada = input(f"{mensaje}")
            print(len(entrada))
        return entrada
    
    @classmethod
    def validar_opciones_multiples_int(cls, opciones, mensaje):
        entrada = -1

        while not (entrada in opciones):
            try:
                entrada = int(input(mensaje))
            except ValueError:
                pass
        return entrada
        
    @classmethod
    def validar_opciones_multiples_str(cls, opciones, mensaje):
        entrada = ""

        while not (entrada in opciones):
            try:
                entrada = input(mensaje)
            except ValueError:
                pass
        return 
    @classmethod
    def validar_año(cls,datos, cantidad=2):
        año_a,año_b = min(datos.rendimiento["Año"]),max(datos.rendimiento["Año"])
        años = [int(Validadores.validarEntero(año_a,año_b, mensaje=f"[!] Ingrese el año en el rango {año_a}-{año_b}: ")) for _ in range(cantidad)]
        return años 
    @classmethod
    def validar_universidad(cls,datos):
        universidades =datos.rendimiento["Universidad"].unique().tolist()
        for indice, univ in enumerate(universidades):
            print(indice, univ)
        indice = Validadores.validar_opciones_multiples_int(list(range(len(universidades))), "[+] Ingrese la universidad: ")      
        return universidades[indice]
    
def sub_menu_dos(datos):
    analizador = AnalisisDataframes(datos)
    while True:
        print(f"""

            1. grafico lineas rendimiento academico 
            2. grafico barras comparativo de satisfaccion y taza de retencion
            3. grafico dispersion para relacion entre uso de videojuegos y rendimiento
            4. grafico pastel para distribucion de satisfaccion en un año X
            """)
        match Validadores.validar_opciones_multiples_int([1,2,3,4], "[+] Seleccione: "):
            case 1:
                años = Validadores.validar_año(datos)
                analizador.GrafLinRenAc(años[0], años[1])
            case 2:
                años = Validadores.validar_año(datos)
                universidades = [Validadores.validar_universidad(datos)  for _ in range(2)]
                analizador.GrafBarCompSatisTasa(años[0],años[1], universidades)
            case 3:
                universidad = Validadores.validar_universidad(datos)
                analizador.GrafDispRelVidjuegRend(universidad)
            case 4: 
                año = Validadores.validar_año(datos, 1)
                analizador.GrafPasterlDistrSatis(año[0])
            case 5:
                return 
                
def sub_menu_tres(datos):
    estadisticas = OperacionesEstadisticas(datos)
    while True:
        print(f"""

            1. Medidas De tendencia Central
            2. Medidas de dispersion
            3. Correlacion y covarianza
            4. distribucion
            5. salir
            """)
        match Validadores.validar_opciones_multiples_int([1,2,3,4], "[+] Seleccione: "):
            case 1:
                rendimiento, satisfaccion = estadisticas.tendencia_central()     
                for key in ["Mediana","Media","Moda"]:
                    print(f"""
                    Rendimiento-{key}:{rendimiento[key]}
                    Satisfaccion-{key}: {satisfaccion[key]}
                    """)
            case 2:
                rendimiento, satisfaccion = estadisticas.dispersion()
                for key in ["Varianza", "Desviacion"]:
                    print(f"""
                    Rendimiento-{key}:{rendimiento[key]}
                    Satisfaccion-{key}: {satisfaccion[key]}
                    """)
            case 3:
                estadisticas.correlacion_covarianza()
            case 4: 
                estadisticas.analisis_distribucion()
            case 5:
                return
def sub_menu_cuatro(datos):

    modelos = AnalisisModelosPredictivos(datos)
    while True:
        print(f"""

            1. Regresion Lineal
            2. Arbol
            3. salir
            """)
        match Validadores.validar_opciones_multiples_int([1,2,3,4], "[+] Seleccione: "):
            case 1:
                universidad = Validadores.validar_universidad(datos)
                modelos.regresion_lineal(universidad)
            case 2:
                universidad = Validadores.validar_universidad(datos)
                modelos.arbol(universidad)
            case 3: 
                return

def agregar_datos(df, tipo_datos):

    
    if tipo_datos == "satisfaccion":
        columnas = ["Año", "Universidad", "Videojuego Educativo", "Satisfacción (%)", "Tasa de Retención (%)"]
    elif tipo_datos == "rendimiento":
        columnas = ["Año", "Universidad", "Videojuego Educativo", "Estudiantes (n)", "Rendimiento Promedio (%)"]

    nuevo_dato = {}
    año_min, año_max = 2000, 2025  # Ajusta según sea necesario
    nuevo_dato["Año"] = Validadores.validarEntero(año_min, año_max, "[!] Ingrese el año (2000-2025): ")
    universidades_existentes = df["Universidad"].unique().tolist() if "Universidad" in df.columns else []
    print("\nUniversidades disponibles:")
    for i, uni in enumerate(universidades_existentes):
        print(f"{i + 1}. {uni}")

    if universidades_existentes:
        indice_uni = Validadores.validar_opciones_multiples_int(list(range(len(universidades_existentes))),
                                                                 "[+] Seleccione la universidad (número): ")
        nuevo_dato["Universidad"] = universidades_existentes[indice_uni]
    else:
        nuevo_dato["Universidad"] = input("[+] Ingrese el nombre de la universidad: ")

    nuevo_dato["Videojuego Educativo"] = Validadores.validarString(1, 30, "[+] Ingrese el videojuego educativo: ")

    if tipo_datos == "satisfaccion":
        nuevo_dato["Satisfacción (%)"] = Validadores.validarEntero(0, 100, "[+] Ingrese el porcentaje de satisfacción (0-100%): ")
        nuevo_dato["Tasa de Retención (%)"] = Validadores.validarEntero(0, 100, "[+] Ingrese la tasa de retención (0-100%): ")

    elif tipo_datos == "rendimiento":
        nuevo_dato["Estudiantes (n)"] = Validadores.validarEntero(1, 10000, "[+] Ingrese el número de estudiantes: ")
        nuevo_dato["Rendimiento Promedio (%)"] = Validadores.validarEntero(0, 100, "[+] Ingrese el rendimiento promedio (0-100%): ")

    nuevo_df = pd.DataFrame([nuevo_dato])
    df_actualizado = pd.concat([df, nuevo_df], ignore_index=True)

    print("\nDatos agregados exitosamente")
    return df_actualizado


def sub_menu_cinco(datos):
    while True:
        print(f"""

            1. Satisfaccion
            2. Rendimiento
            3. salir
            """)
        match Validadores.validar_opciones_multiples_int([1,2], "[+] Seleccione: "):
            case 1:
                datos.actualizar_rend = agregar_datos(datos.rendimiento, "rendimiento")
            case 2:
                datos.actualizar_satis = agregar_datos(datos.rendimiento, "satisfaccion")
            case 3: 
                return 
        
def sub_menu_seis(datos):
    while True:
        print(f"""

            Desea selecionar nombre?:
            1. si
            2. no
            
            """)
        match Validadores.validar_opciones_multiples_int([1,2], "[+] Seleccione: "):
            case 1:
                nombre_rend = Validadores.validarString(0,100,"[!] Ingrese nombre de rendimiento: ")
                nombre_satis = Validadores.validarString(0,100,"[!] Ingrese nombre de satisfaccion: ")
                datos.exportar_datos(nombre_rend, nombre_satis)
            case 2:
                datos.exportar_datos()
def menu():
    datos = ImportarDatos()
    datos.cargar_datos()
    while True:
        print(f"""

            1. Ver datos
            2. Analisar Dataframes
            3. Operaciones Estadisticas
            4. Analisis Modelos predictivos
            5. agregar datos
            7. salir
            """)
        match Validadores.validar_opciones_multiples_int([1,2,3,4,5,6,7], "[+] Seleccione: "):
            case 1:
                pass
            case 2:
                sub_menu_dos(datos)
            case 3:
                sub_menu_tres(datos)
            case 4:
                sub_menu_cuatro(datos)
            case 5: 
                sub_menu_cinco(datos)
            case 6:
                sub_menu_seis(datos)
            case 7:
                exit()

    

if __name__ == '__main__':
    menu()