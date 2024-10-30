import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
fig, axs = plt.subplots(1, 4)
fig = plt.figure(figsize=(21,10))

base_poblacion_proyectada2021 = pd.read_csv("base_poblacion_proyectada2021.csv", sep=";")
migracion_internacional = pd.read_excel("caso9_migracion_internacional_clear.xlsx", sheet_name="hoja1", usecols=np.arange(0,21)).dropna().reset_index(drop=True)
def columnas():
    lista = np.arange(2004,2024).tolist()
    lista.insert(0, "Contenido")
    return lista
columnas()
salidas_segun_continente = migracion_internacional.iloc[1:12,:].set_axis(columnas(), axis="columns").reset_index(drop=True).drop([0], axis=0)
entradas_segun_continente = migracion_internacional.iloc[12:,:].set_axis(columnas(), axis="columns").reset_index(drop=True).drop([0], axis=0)
def graficar_tendencias_salida_peruanos(ano_A, ano_B):
    axs[0].plot(entradas_segun_continente["Contenido"], entradas_segun_continente[ano_A]/1000, entradas_segun_continente["Contenido"], entradas_segun_continente[ano_B]/1000, marker= 'o')
    axs[0].legend([f"Año {ano_A}", f"año {ano_B}"])
    axs[0].set_ylabel("Milliones de salida")
    axs[0].set_xlabel("continente")

graficar_tendencias_salida_peruanos(2004, 2009)
def graficar_tendencias_entrada_peruanos(ano_A, ano_B):
    axs[1].plot(salidas_segun_continente["Contenido"], salidas_segun_continente.loc[:,ano_A]/1000, salidas_segun_continente["Contenido"], salidas_segun_continente[ano_B]/1000, marker= 'o')
    axs[1].legend([f"Año {ano_A}", f"año {ano_B}"])
    axs[1].set_ylabel("Milliones de salida")
    axs[1].set_xlabel("continente")
graficar_tendencias_entrada_peruanos(2004, 2005)
def graficar_barras_continente(continente):
    salidas_continente = salidas_segun_continente.where(salidas_segun_continente["Contenido"]==continente).dropna()
    entradas_continente = entradas_segun_continente.where(entradas_segun_continente["Contenido"]==continente).dropna()
    #axs[2].bar(x= salidas_continente.columns,  height = salidas_continente.iloc[0:, :] )
    axs[2].bar(salidas_continente.columns.tolist()[1:], [valor for valor in salidas_continente.iloc[0: ,1:].values.tolist()[0]])
    axs[2].bar(entradas_continente.columns.tolist()[1:], [valor for valor in entradas_continente.iloc[0: ,1:].values.tolist()[0]])
    axs[2].legend(["Salida", "Entrada"])

graficar_barras_continente("América")
def graficar_barras_continente(continente):
    ano = 2021
    salidas_continente = salidas_segun_continente.where(salidas_segun_continente["Contenido"]==continente).dropna()
    entradas_continente = entradas_segun_continente.where(entradas_segun_continente["Contenido"]==continente).dropna()
    #axs[2].bar(x= salidas_continente.columns,  height = salidas_continente.iloc[0:, :] )
    axs[3].barh("Salidas",  salidas_continente[ano])
    axs[3].barh("Entradas",  entradas_continente[ano])

graficar_barras_continente("América")

plt.show()
