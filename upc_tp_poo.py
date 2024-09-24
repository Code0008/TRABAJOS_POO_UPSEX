class tres_en_raya():
    instrucciones =      """
    //////////////// TRES EN RAYA //////////////
          EL JUEGO CONSISTE EN EL CONOCIDO JUEGO DE "MICHI"
          EN EL QUE AQUEL QUE COMPLETE UNA LÍNEA O DIAGONAL GANA EL JUEGO 
          Reglas:
          -> Si un usuario ingresa una posición que ya está ocupada, pierde su siguiente turno 
          -> El juego terminará con una fila, columna o diagonal completada
          -> EL FORMATO PARA INGRESAR SU POSICIÓN ES FILA:COLUMNA (1:1) 
          -> Si todas las casillas están completas sin ganador, será un empate.
    """
    def __init__(self) -> None:
        self.__ganadas_jugador_uno = 0
        self.__ganadas_jugador_dos = 0
        self.__partidas_empates = 0
        self.tablero = []

    def crear_tablero(self):
        self.tablero = [['.', '.', '.'] for _ in range(3)]
    def get_resultados_jugador_uno(self):
        return self.__ganadas_jugador_uno
    def get_resultados_jugador_dos(self):
        return self.__ganadas_jugador_dos
    def get_empates(self):
        return self.__partidas_empates
    
    def incrementar_ganadas(self, jugador):
        match jugador:
            case 1: self.__ganadas_jugador_uno+=1
            case 2: self.__ganadas_jugador_dos+=1

    def impresion_tablero(self):
        print(f"Columna  1     2     3")
        for indice, fila in enumerate(self.tablero, start=1):
           print(f"Fila {indice}: {fila}")

    def ingreso_de_jugador(self, jugador):
        entrada = []
        while not (entrada and len(entrada) == 2 and 1<=entrada[0] <4 and 1<=entrada[1]<4):
            try:
                entrada = list(map(int, input(f"""Ingrese jugador {jugador} las coordenadas en el siguiente formato:'FILA:COLUMNA' -> EJEMPLO: 1:2 """).split(":")))
            except Exception:
                continue
        return  (entrada[0]-1, entrada[1]-1) # Ajustar para índice del tablero
    
    
    def validar_filas_columnas_diagonales(self,caracter):
            if [caracter]*3 in self.tablero:
                return True
                
            # Verificar columnas
            for columna in range(3):
                if [self.tablero[fila][columna] for fila in range(3)] == [caracter] * 3:
                    return True
            # Verificar diagonales
            diagonal_normal = [self.tablero[i][i] for i in range(3)]
            diagonal_inversa = [self.tablero[i][2-i] for i in range(3)]

            if [caracter]*3 in (diagonal_inversa, diagonal_normal):
                return True
            
            return False
    
    def actualizar_casilla(self,entrada, caracter):
        if self.tablero[entrada[0]][entrada[1]] != '.':
            return False
        else:
            self.tablero[entrada[0]][entrada[1]] = caracter
            return True
        
    def menu_tres_en_raya(self):
        sanciones = [False, False]
        turno = 1
        movimientos_restantes = 9
        self.crear_tablero()

        while movimientos_restantes > 0:
            self.impresion_tablero()
            caracter = 'X' if turno == 1 else 'O'
            if sanciones[turno - 1]:
                print(f"Jugador {turno} pierde su turno por sanción.")
                sanciones[turno - 1] = False
            else:
                entrada = self.ingreso_de_jugador(turno)
                if not self.actualizar_casilla(entrada, caracter):
                    print(f"Jugador {turno}, la casilla ya está ocupada. Pierdes tu turno.")
                    sanciones[turno - 1] = True
                else:
                    movimientos_restantes -= 1
                    if self.validar_filas_columnas_diagonales(caracter):
                        self.impresion_tablero()
                        print(f"¡Jugador {turno} ha ganado!")
                        self.incrementar_ganadas(turno)
                        return
            turno = 2 if turno == 1 else 1
        self.impresion_tablero()
        print("El juego ha terminado en empate.")
        self.partidas_empates += 1

from random import randint
class adivinar_numero():
    instrucciones =    """
    //////////// ADIVINAR EL NÚMERO //////////
          REGLAS:
          -> Tiene 6 intentos para adivinar el número generado aleatoriamente.
          -> El juego indicará si el número a adivinar es mayor o menor.
    """
    def __init__(self) -> None:
        self.__veces_perdidas = 0
        self.__veces_ganadas = 0

    def get_veces_perdidas(self):
        return self.__veces_perdidas

    def get_veces_ganadas(self):
        return self.__veces_ganadas
    
    def descubrir_numero(self):
        numero_a_descubrir = randint(0, 20)
        intentos = 6
        while intentos>0:
            try:
                entrada = int(input("Ingrese numero: "))
                if entrada < numero_a_descubrir:
                    print("EL NUMERO ES MENOR")
                else:
                    print("EL NUMERO ES MAYOR")
                if entrada == numero_a_descubrir:
                    print(F"GANASTE EN EL INTENTO {6-intentos}")
                    self.veces_ganadas+=1
                    return None
            except Exception:
                continue
            finally:
                intentos-=1            
        print(f"El número era {numero_a_descubrir}. No adivinaste.")
        self.__veces_perdidas += 1

class reportes():
        def __init__(self, tres_en_raya, adivinar_numero) -> None:
            self.__contadores = [[tres_en_raya.get_resultados_jugador_uno(), tres_en_raya.get_resultados_jugador_dos(),tres_en_raya.get_empates()], [ adivinar_numero.get_veces_ganadas(),adivinar_numero.get_veces_perdidas()]]
            self.__graficos = []
            self.__porcentajes = {"ganadas_tres_en_raya":0,"adivinar_numero": 0,"ganar_algun_juego":0}

        def matriz_grafica(self, *data_partidas):
            tamano =  max(data_partidas)+3
            grafico = [['.' for _ in range(len(data_partidas)+1)] for _ in range(tamano)]
            for indice, victorias in enumerate(data_partidas):
                for fila in range(tamano-1, (tamano-victorias)-1, -1):
                        grafico[fila][indice]='*'
            promedio = sum(data_partidas) // len(data_partidas)
            for fila in range(tamano-1, (tamano-promedio)-1, -1):
                grafico[fila][3]= '*'
            return grafico
        def set_graficos(self, graficos):
            self.__graficos = [grafico for grafico in graficos]
        def graficos_creador(self):
            graficos = [self.matriz_grafica(self.__contadores[0][1], self.__contadores [0][2],self.__contadores[1][0]),
                        self.matriz_grafica(self.__contadores[1][1],self.__contadores[0][2],self.__contadores [0][1])]       
            self.set_graficos(graficos)

        def porcentaje(self, *numeros):
            try:
                return sum(numeros[0])*100/sum(self.__contadores[1])
            except Exception:
                return 0
        def porcentajes_calcular_imprimir(self):
            self.__porcentajes["ganadas_tres_en_raya"] =self.porcentaje( (self.__contadores [0][1],self.__contadores [0][0])  , self.__contadores[0] )            
            self.__porcentajes["adivinar_numero"]=self.porcentaje(self.__contadores [1][0] if not self.__contadores [1][0]==0 else 1 , self.__contadores[1] )
                                        
            self.__porcentajes["ganar_algun_juego"]= self.porcentaje((self.__contadores [0][1],self.__contadores [0][2],self.__contadores [1][0]),(self.__contadores[0],self.__contadores [1]) )
        
            for estadistica,valor in self.__porcentajes.items():
                print(f"porcentaje {estadistica}:{valor}")

        def imprimir_grafico(self, grafico):
                for indice,fila in enumerate(grafico):
                    print(f"{len(grafico)-indice}: {fila}")
        def impresion(self):

            self.graficos_creador()
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
                        self.imprimir_grafico(self.__graficos[0])            
                        print("""
                            Primera columna: victorias jugador uno (tres en raya)
                            Segunda columna: victorias jugador dos (tres en raya) 
                            Tercera columna: victorias en adivinar numero 
                            Cuarta columna: promedio de victorias en los juegos       
                            """)
                    case 2:
                        self.imprimir_grafico(self.__graficos[1])
                        print(""" Primera columna : derrotas de adivinar el numero
                                Segunda columna: derrotas del  jugador  uno (tres en raya) 
                                Tercer columna: derrotas del jugador dos (tres en raya)
                                Cuarta columna: promedio de derrotas en partidas
                                    """)
                    case 3:
                        if self.porcentajes_calcular_imprimir() != True:
                            print(f"Por favor llene los valores")
                    case 4:
                        return 
                entrada = -1


class consola():
    def __init__(self) -> None:
        self.__tres_en_raya =  tres_en_raya()
        self.__adivinar_numero = adivinar_numero()

    def menu_principal(self):
        entrada = -1
        while not (1<=entrada<4):
            print(
                        """
                //////// BIENVENIDO AL MENU GENERAL :V //////////   
                1. ingrese al tres en raya 
                2. ingrese al detectector de numero aleatorio 
                3. estadisticas
                4. salir
                
                """)
            entrada =  int(input("Ingrese su seleccion: "))
            match entrada:
                case 1: 
                    print(self.__tres_en_raya.instrucciones)
                    self.__tres_en_raya.menu_tres_en_raya()                        
                case 2:
                    print(self.__adivinar_numero.instrucciones)
                    self.__adivinar_numero.descubrir_numero()
                case 3: 
                    estadistica = reportes(tres_en_raya=self.__tres_en_raya, adivinar_numero= self.__adivinar_numero)
                    estadistica.impresion()
                case 4:
                    exit(1)
            entrada=-1   
        
Consola = consola()
Consola.menu_principal()
