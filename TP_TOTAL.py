tablero = [['.', '.', '.'] for _ in range(3)]

def instrucciones_del_juego_tres_en_raya():
    print("""
    //////////////// TRES EN RAYA //////////////
          EL JUEGO CONSISTE EN EL CONOCIDO JUEGO DE "MICHI"
          EN EL QUE AQUEL QUE COMPLETE UNA LÍNEA O DIAGONAL GANA EL JUEGO 

          Reglas:
          -> Si un usuario ingresa una posición que ya está ocupada, pierde su siguiente turno 
          -> El juego terminará con una fila, columna o diagonal completada
          -> EL FORMATO PARA INGRESAR SU POSICIÓN ES FILA:COLUMNA (1:1) 
          -> Si todas las casillas están completas sin ganador, será un empate.

    """)

def impresion():
    print(f"Columna  1     2     3")
    for indice, fila in enumerate(tablero, start=1):
        print(f"Fila {indice}: {fila}")

def ingreso_de_jugador(jugador):
    entrada = []
    while not (entrada and len(entrada) == 2 and 1<=entrada[0] <4 and 1<=entrada[1]<4):
        try:
            entrada = list(map(int, input(f"""
                            Ingrese jugador {jugador} las coordenadas en el siguiente formato:
                            'FILA:COLUMNA' -> EJEMPLO: 1:2 
                            """).split(":")))
        except Exception as e:
            continue
    return  (entrada[0]-1, entrada[1]-1) # Ajustar para índice del tablero

def validador_filas_columnas_diagonales(caracter):
    # Verificar filas
    if [caracter]*3 in tablero:
        return True
              
    # Verificar columnas
    for columna in range(3):
        if [tablero[fila][columna] for fila in range(3)] == [caracter] * 3:
            return True
    
    # Verificar diagonales
    diagonal_normal = [tablero[i][i] for i in range(3)]
    diagonal_inversa = [tablero[i][2-i] for i in range(3)]

    if [caracter]*3 in (diagonal_inversa, diagonal_normal):
        return True
    
    return False

def actualizar_casilla(entrada, caracter):
    if tablero[entrada[0]][entrada[1]] != '.':
        return False
    else:
        tablero[entrada[0]][entrada[1]] = caracter
        return True

def menu_tres_en_raya():
    sanciones = [False, False]  # Sanciones para jugador 1 y 2
    turno = 1  # Empieza el jugador 1
    movimientos_restantes = 9  # Hay 9 casillas disponibles
    
    while movimientos_restantes > 0:
        impresion()  # Mostrar el tablero antes de cada jugada
        
        # Determinar el símbolo del jugador
        caracter = 'X' if turno == 1 else 'O'
        
        if sanciones[turno - 1]:
            print(f"Jugador {turno} pierde su turno por sanción.")
            sanciones[turno - 1] = False  # Eliminar sanción
        else:
            entrada = ingreso_de_jugador(turno)
            impresion()
            if not actualizar_casilla(entrada, caracter):
                print(f"Jugador {turno}, la casilla ya está ocupada. Sanción aplicada.")
                impresion()
                sanciones[turno - 1] = True  # Sancionar si la casilla está ocupada
            else:
                movimientos_restantes -= 1  # Reducir el número de movimientos restantes
                
                # Verificar si el jugador ha ganado
                if validador_filas_columnas_diagonales( caracter):
                    impresion()
                    print(f"¡Jugador {turno} ha ganado!")
                    return turno

        # Cambiar de turno (Jugador 1 -> 2 o Jugador 2 -> 1)
        turno = 2 if turno == 1 else 1
    
    impresion()  # Mostrar el tablero final en caso de empate
    print("El juego ha terminado en empate.")
    return False

from random import *

def instrucciones_juego_adivinar_numero():
    print(f"""
    ////////////BIENVENIDO AL JUEGO DE ADIVINAR EL NUMERO////////////
          REGLAS:
          -> Usted tiene 6 intentos de poder hallar el numeor 
          -> si pasa el tiempo usted perdio 
          -> Se le dara instrucciones de cuando usted este cerca o no de hallar el numero 

        """)

def descubrir_numero_aleatorio():
    numero_a_descubrir = randint(0,10)
    intentos =  6
    while intentos>0:
        try:
            entrada = int(input("Ingrese numero: "))
            if entrada < numero_a_descubrir:
                print("ES MENOR")
            else:
                print("ES MAYOR")
            if entrada == numero_a_descubrir:
                print(F"GANASTE EN EL INTENTO {6-intentos}")
                return True
        except Exception as e:
            continue
        finally:
            intentos-=1
    return False


def impresios_de_grafico(*data_partidas):
    tamano =  max(data_partidas)+3
    grafico = [['.' for _ in range(len(data_partidas)+1)] for _ in range(tamano)]
    for indice, victorias in enumerate(data_partidas):
        for fila in range(tamano-1, (tamano-victorias)-1, -1):
            grafico[fila][indice]='*'
    promedio = sum(data_partidas) // len(data_partidas)
    for fila in range(tamano-1, (tamano-promedio)-1, -1):
        grafico[fila][3]= '*'
    for indice,fila in enumerate(grafico):
        print(f"{tamano-indice}: {fila}")

def filtrar_perdidas(*data_partidas):
    data_pasable = [informacion for informacion in data_partidas if informacion>=0]
    impresios_de_grafico(data_pasable)

def porcentajes(data_partidas): 
    try:
        porcentaje_tres_en_raya =  (data_partidas[0][1]+data_partidas[0][2])*100 / sum(data_partidas[0])
        procentaje_adivinar_numero = (data_partidas[1][0])*100 / sum(data_partidas[0])
        porcentaje_ganar_en_algun_juego = (data_partidas[0][1]+data_partidas[0][2]+data_partidas[1][0])*100 / sum(data_partidas[0])+ sum(data_partidas[1])
        print(f"""
        //// REPORTE PORCENTUAL:
          PORCENTAJE DE GANADAS EN TRES EN RAYA: {porcentaje_tres_en_raya}  
          PORCENTAJE ADIVINAR NUMERO: {procentaje_adivinar_numero}
          PORCENTAJE DE GANAR ALGUN JUEGO : {porcentaje_ganar_en_algun_juego}
        
        """)
    except ZeroDivisionError:
        print(f"Asegurense que no halla algun valor 0 ")
def estadisticas(valores_contadores):
    entrada= 0
    while not (1<=entrada<=4):
        print(f"""
            //////// BIENVENIDO AL MENU DE REPORTES //////
            1. grafico de barras de partidas ganadas 
            2. grafico de barras de partidas perdidas
            3. porcentajes de victorias y derrotas en los juegos  
            4. regresar        
            """)
        try:
            entrada = int(input(f"Ingrese opcion: "))
        except Exception as e:
            continue
        match entrada:
            case 1:
                impresios_de_grafico(valores_contadores[0][1], # victorias jugador uno
                                     valores_contadores[0][2], # vicrtorias jugador dos
                                     valores_contadores[1][0]) # victorias en adivinar numero
                print("""
                      Primera columna: victorias jugador uno (tres en raya)
                      Segunda columna: victorias jugador dos (tres en raya) 
                      Tercera columna: victorias en adivinar numero 
                      Cuarta columna: promedio de victorias en los juegos       
                    """)
            case 2:
                impresios_de_grafico(valores_contadores[1][1], # derrotas en adinivar numero
                                    valores_contadores[0][2] - valores_contadores[0][1], # diferencia que muestra cuantas veces pierde el jugador uno 
                                    valores_contadores[0][1] - valores_contadores[0][2] # diferencia de periddas de jugador dos 
                                    )
                print(""" Primera columna : derrotas de adivinar el numero
                          Segunda columna: derrotas del  jugador  uno (tres en raya) 
                          Tercer columna: derrotas del jugador dos (tres en raya)
                          Cuarta columna: promedio de derrotas en partidas
                            """)
            case 3:
                porcentajes(valores_contadores.copy())
            case _:
                continue
            
        entrada = -1
def menu_general():
    mensaje = """
    //////// BIENVENIDO AL MENU GENERAL :V //////////   
    1. ingrese al tres en raya 
    2. ingrese al detectector de numero aleatorio 
    3. estadisticas
    4. 

    """
    entrada = -1
    contadores_victorias_perdidas = [
        [
            0, # Empates
            0, # jugador 1
            0, # jugador 2
        ], # tres en raya
        [
            0, # victorias
            0, # derrotas

        ]
    ]
    while not (1<=entrada<4):
        print(mensaje)
        entrada =  int(input("Ingrese su seleccion: "))

        match entrada:
            case 1: 
                instrucciones_del_juego_tres_en_raya()
                resultado = menu_tres_en_raya()
                if not (resultado):
                    contadores_victorias_perdidas[0][0]+=1
                elif resultado==1:
                    contadores_victorias_perdidas[0][1]+=1
                else:
                    contadores_victorias_perdidas[0][2]+=1
            case 2:
                instrucciones_juego_adivinar_numero()

                resultado = descubrir_numero_aleatorio() 
                if resultado:
                    contadores_victorias_perdidas[1][0]+=1
                else: 
                    contadores_victorias_perdidas[1][1]+=1

            case 3: 
                estadisticas(contadores_victorias_perdidas.copy())
            case 4:
                exit(1)
        entrada=-1

if __name__ == "__main__":
    menu_general()