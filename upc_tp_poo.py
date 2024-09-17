class tres_en_raya():
    """
    //////////////// TRES EN RAYA //////////////
          EL JUEGO CONSISTE EN EL CONOCIDO JUEGO DE "MICHI"
          EN EL QUE AQUEL QUE COMPLETE UNA LÍNEA O DIAGONAL GANA EL JUEGO 

          Reglas:
          -> Si un usuario ingresa una posición que ya está ocupada, pierde su siguiente turno 
          -> El juego terminará con una fila, columna o diagonal completada
          -> EL FORMATO PARA INGRESAR SU POSICIÓN ES FILA:COLUMNA (1:1) 
          -> Si todas las casillas están completas sin ganador, será un empate.

    """
    tablero = [['.', '.', '.'] for _ in range(3)]

    def __init__(self) -> None:
        self._ganadas_jugador_uno = 0
        self._ganadas_jugador_dos = 0
        self._partidas_empates = 0

    @property
    def ganadas_jugador_uno(self):
        return self._ganadas_jugador_uno 
    @property
    def ganadas_jugador_dos(self):
        return self._ganadas_jugador_dos
    @property
    def empates(self):
        return self._partidas_empates
    
    @ganadas_jugador_uno.setter
    def incrementar_ganadas_uno(self, valor):
        self._ganadas_jugador_uno+= valor
    @ganadas_jugador_dos.setter
    def incrementar_ganadas_dos(self, valor):
        self._ganadas_jugador_dos+=valor

    def incrementar_ganadas(self, jugador):
        match jugador:
            case 1: self.incrementar_ganadas_uno=1
            case 2: self.incrementar_ganadas_dos=1

    def impresion(self):
        print(f"Columna  1     2     3")
        for indice, fila in enumerate(self.tablero, start=1):
            print(f"Fila {indice}: {fila}")


    def ingreso_de_jugador(self, jugador):
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
    def menu(self):
        sanciones = [False, False]  # Sanciones para jugador 1 y 2
        turno = 1  # Empieza el jugador 1
        movimientos_restantes = 9  # Hay 9 casillas disponibles
        
        while movimientos_restantes > 0:
            self.impresion()  # Mostrar el tablero antes de cada jugada
            
            # Determinar el símbolo del jugador
            caracter = 'X' if turno == 1 else 'O'
            
            if sanciones[turno - 1]:
                print(f"Jugador {turno} pierde su turno por sanción.")
                sanciones[turno - 1] = False  # Eliminar sanción
            else:
                entrada = self.ingreso_de_jugador(turno)
                self.impresion()
                if not self.actualizar_casilla(entrada, caracter):
                    print(f"Jugador {turno}, la casilla ya está ocupada. Sanción aplicada.")
                    self.impresion()
                    sanciones[turno - 1] = True  # Sancionar si la casilla está ocupada
                else:
                    movimientos_restantes -= 1  # Reducir el número de movimientos restantes
                    
                    # Verificar si el jugador ha ganado
                    if self.validar_filas_columnas_diagonales( caracter):
                        self.impresion()
                        print(f"¡Jugador {turno} ha ganado!")
                        self.incrementar_ganadas(turno)
                        return None

            # Cambiar de turno (Jugador 1 -> 2 o Jugador 2 -> 1)
            turno = 2 if turno == 1 else 1
        
        self.impresion()  # Mostrar el tablero final en caso de empate
        self._partidas_empates+=1
        print("El juego ha terminado en empate.")

from random import randint

class Adivinar_numero():
    """
    ////////////BIENVENIDO AL JUEGO DE ADIVINAR EL NUMERO////////////
          REGLAS:
          -> Usted tiene 6 intentos de poder hallar el numeor 
          -> si pasa el tiempo usted perdio 
          -> Se le dara instrucciones de cuando usted este cerca o no de hallar el numero 

        """
    numero_a_descubrir= randint(0,10)

    def __init__(self) -> None:
        self._veces_perdidas = 0
        self._veces_ganadas = 0

    @property
    def veces_ganadas(self):
        return self._veces_ganadas
    @property
    def veces_perdidas(self):
        return self._veces_perdidas
    
    def descubrir_numero(self):
        intentos = 6
        while intentos>0:
            try:
                entrada = int(input("Ingrese numero: "))
                if entrada < self.numero_a_descubrir:
                    print("ES MENOR")
                else:
                    print("ES MAYOR")
                if entrada == self.numero_a_descubrir:
                    print(F"GANASTE EN EL INTENTO {6-intentos}")
                    self.veces_ganadas+=1
                    return None
            except Exception as e:
                continue
            finally:
                intentos-=1
        self.veces_perdidas+=1
        
class estadisticas():
        def __init__(self, tres_en_raya, adivinar_numero ) -> None:
            self._contadores = [
                [
                tres_en_raya.ganadas_jugador_uno,
                tres_en_raya.ganadas_jugador_dos,
                tres_en_raya.empates
                ],
                [
                    adivinar_numero.veces_ganadas,
                    adivinar_numero.veces_perdidas
                ]
            ]
            self._graficos = []
            self._porcentajes = {
                "ganadas_tres_en_raya":0,
                "adivinar_numero": 0,
                "ganar_algun_juego":0
            }

        @property
        def graficos(self):
            return self._graficos
        @property
        def porcentajes(self):
            return self._porcentajes    
        @property
        def contadores(self):
            return self._contadores
        @graficos.setter
        def set_graficos (self, valor):
            self.graficos = valor

        
        def graficos_creador(self):
            def creacion_grafico(*data_partidas):
                tamano =  max(data_partidas)+3
                grafico = [['.' for _ in range(len(data_partidas)+1)] for _ in range(tamano)]
                for indice, victorias in enumerate(data_partidas):
                    for fila in range(tamano-1, (tamano-victorias)-1, -1):
                        grafico[fila][indice]='*'
                promedio = sum(data_partidas) // len(data_partidas)
                for fila in range(tamano-1, (tamano-promedio)-1, -1):
                    grafico[fila][3]= '*'
                return grafico
            graficos = [
                creacion_grafico(# victorias
                self.contadores[0][1], 
                self.contadores[0][2],
                self.contadores[1][0]
                ),
                creacion_grafico(# perdidas
                    self.contadores[1][1],
                    self.contadores[0][2],
                    self.contadores[0][1]
                )
                
            ]    
            self.set_graficos = [grafico for grafico in graficos]
    
        def porcentajes_calcular_imprimir(self):
            def porcentaje(*numeros):
                return sum(numeros[0])*100/sum(self.contadores[1])

            self.porcentajes["ganadas_tres_en_raya"] =porcentaje(
                        (self.contadores[0][1],self.contadores[0][0])
                    , self.contadores[0]
                    )            
            self.porcentajes["adivinar_numero"]=porcentaje(# adivinar numero
                                        self.contadores[1][0] if not self.contadores[1][0]==0 else 1 , 
                                        self.contadores[1] )
                                        
            self.porcentajes["ganar_algun_juego"]= porcentaje(# porcentaje de ganar en algun juego 
                                    (self.contadores[0][1],self.contadores[0][2],self.contadores[1][0]),
                                    (self.contadores[0],self.contadores[1])
                                    )

            

            for estadistica,valor in self.porcentajes.items():
                print(f"porcentaje {estadistica}:{valor}")


        def impresion(self):
            def imprimir_grafico(grafico):
                for indice,fila in enumerate(grafico):
                    print(f"{len(grafico)-indice}: {fila}")
            
            self.graficos_creador()
            self.porcentajes_calcular_imprimir()
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
                        imprimir_grafico(self.graficos[0])            
                        print("""
                            Primera columna: victorias jugador uno (tres en raya)
                            Segunda columna: victorias jugador dos (tres en raya) 
                            Tercera columna: victorias en adivinar numero 
                            Cuarta columna: promedio de victorias en los juegos       
                            """)
                    case 2:
                        imprimir_grafico(self.graficos[1])
                        print(""" Primera columna : derrotas de adivinar el numero
                                Segunda columna: derrotas del  jugador  uno (tres en raya) 
                                Tercer columna: derrotas del jugador dos (tres en raya)
                                Cuarta columna: promedio de derrotas en partidas
                                    """)
                    case 3:
                        self.porcentajes_calcular_imprimir()
                entrada = -1


        
class Consola():
    def __init__(self) -> None:
        self._tres_en_Raya = tres_en_raya()
        self._adivinar_numero = Adivinar_numero()
    @property
    def tres_en_raya_g(self):
        return self._tres_en_Raya
    @property
    def adivinar_numero_g(self):
        return self._adivinar_numero

    def menu(self):
        
        entrada = -1
        while not (1<=entrada<4):
            print(
                        """
                //////// BIENVENIDO AL MENU GENERAL :V //////////   
                1. ingrese al tres en raya 
                2. ingrese al detectector de numero aleatorio 
                3. estadisticas

                """)
            entrada =  int(input("Ingrese su seleccion: "))
            match entrada:
                case 1: 
                    print(self.tres_en_raya_g.__doc__)
                    self.tres_en_raya_g.menu()                        
                case 2:
                    print(self.adivinar_numero_g.__doc__)
                    self.adivinar_numero_g.descubrir_numero()
                case 3: 
                    estadistica = estadisticas(tres_en_raya=self.tres_en_raya_g, adivinar_numero=self.adivinar_numero_g )
                    estadistica.impresion()
                case 4:
                    exit(1)
            entrada=-1

if __name__ == "__main__":
    juego =  Consola()
    juego.menu()