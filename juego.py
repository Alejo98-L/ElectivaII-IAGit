import math
import random
tablero = [] #Nuestro tablero inicialmente tiene casillas vacias
casillasvacias = []
Tablero_Filas = 3
Tablero_Columnas = 3

# Inicializamos el tablero
for i in range(9):
    tablero.append(' ')
    casillasvacias.append(i)

# Coloca una ficha en el tablero
def numero(literal, inferior, superior):
    while True:
     Valor = input(literal)
     while(not Valor.isnumeric()):
        print("Solo se admiten numeros entre {0} y {1}".format(inferior, superior))
        Valor = input(literal)
     coor = int(Valor)
     if(coor >= inferior and coor<= superior):
        return coor
     else:
         print("El valor es incorrecto, introduzca un numero entre {0} y {1}".format(inferior, superior))

def colocarficha(ficha):
    print("Dame la posicion de una ficha")
    while True:
        fila = numero("Fila entre [1 y 3]: ", 1, 3)-1 #Restamos 1 ya que el rango esta entre 0 y 2
        columna = numero("Columna entre [1 y 3]: ", 1, 3)-1
        # Como el tablero es de 3x3
        casilla = fila*3 + columna
        if(tablero[casilla] != ' '):
            print("La casilla esta ocupada")
            # Esa casilla esta cubierta
        else:
            tablero[casilla] = ficha
            return casilla

def colocarfichaMaquina(ficha, fichaContricante):
   random.shuffle(casillasvacias)
   for casilla in casillasvacias:
      if(hemosGanado(casilla,ficha)):
         tablero[casilla] = ficha
         return casilla
      if(hemosGanado(casilla,fichaContricante)):
         tablero[casilla] = ficha
         return casilla
   for casilla in casillasvacias:
      tablero[casilla] = ficha
      return casilla

def pintarTablero():
    pos = 0
    print(("-" * 18))
    for fila in range (3):
        for columna in range (3):
         print("| ", tablero[pos]," ", end ="")
         pos += 1
        print("|\n", ("-" *18))

def numeroHermanos(casilla, ficha, v, h):
   f = math.floor(casilla/Tablero_Columnas)
   c = casilla % Tablero_Columnas
   fila_nueva = f+v
   if(fila_nueva<0 or fila_nueva>= Tablero_Filas):
      return 0
   columna_nueva = c+h
   if(columna_nueva<0 or columna_nueva>= Tablero_Columnas):
      return 0
   pos = (fila_nueva*Tablero_Columnas + columna_nueva)
   if(tablero[pos]!=ficha):
      return 0
   else:
      return 1 + numeroHermanos(pos, ficha, v, h)

def hemosGanado(casilla, ficha):
   hermanos = numeroHermanos(casilla,ficha,-1,-1) + numeroHermanos(casilla,ficha, 1 , 1)
   if(hermanos == 2):
      return True
   hermanos = numeroHermanos(casilla,ficha,1,-1) + numeroHermanos(casilla,ficha, -1 , 1)
   if(hermanos == 2):
      return True
   hermanos = numeroHermanos(casilla,ficha,-1,0) + numeroHermanos(casilla,ficha, 1 , 0)
   if(hermanos == 2):
      return True
   hermanos = numeroHermanos(casilla,ficha,0,-1) + numeroHermanos(casilla,ficha, 0 , 1)
   if(hermanos == 2):
      return True

jugadores = []
numerojugadores = numero("Numero de jugadores",0,2)
for i in range(numerojugadores):
   jugadores.append({"nombre":input("Nombre del jugador: "+str(i+1)+": "),"tipo":"H"})
for i in range(2-numerojugadores):
   jugadores.append({"nombre":"Maquina "+str(i+1),"tipo":"M"})

print("\n Empezamos la partida con los jugadores")
for jugador in jugadores:
   print("\t", jugador["nombre"])

empieza = numero("¿Que jugador empieza? [1="+jugadores[0]["nombre"]+",2="+jugadores[1]["nombre"]+"]: ",1,2)
if(empieza==2):
   jugadores.reverse()
# Iniciamos el juego
continuar = True
fichasentablero = 0
while continuar:
    #Pedimos posicion de la ficha
    pintarTablero()
    numjugador = (fichasentablero&1)
    ficha = 'X' if numjugador == 1 else 'O'
    if(jugadores[numjugador]["tipo"]=="H"): 
      casilla = colocarficha(ficha)
    else:
     casilla = colocarfichaMaquina(ficha,'X' if numjugador==0 else 'O')
    casillasvacias.remove(casilla)
    if(hemosGanado(casilla, ficha)):
       continuar = False
       print(jugadores[numjugador]["nombre"], "!!!!Has ganado¡¡¡¡")
    fichasentablero += 1
    if(fichasentablero ==9 and continuar):
        continuar = False
        print("Tablas")
pintarTablero()