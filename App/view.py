"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import stack
from DISClib.DataStructures import listiterator as it
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

citibikeFile1 = "201801-1-citibike-tripdata.csv"
citibikeFile2 = "201801-2-citibike-tripdata.csv"
citibikeFile3 = "201801-3-citibike-tripdata.csv"
citibikeFile4 = "201801-4-citibike-tripdata.csv"

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de Citibke")
    print("3- Requerimento 1")
    print("4- Requerimento 2")
    print("5- Requerimento 3")
    print("6- Requerimento 4")
    print("7- Requerimento 5")
    print("8- Requerimiento 6")
    print("0- Salir")
    print("*******************************************")

def optionTwo1():
    controller.loadTrips(cont)
    viajes = controller.totalTrips(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStations(cont)
    print('Total viajes cargados: ' + str(viajes))
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))

def optionTwo2():
    controller.loadFile(cont, citibikeFile4)
    viajes = controller.totalTrips(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStations(cont)
    print('Total viajes cargados: ' + str(viajes))
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))

def optionThree():
    station1 = input("Primera estación: ")
    station2 = input("Segunda estación: ")
    info = controller.req1(cont, station1, station2)
    print("El número de componentes es:",info[0])
    if info[1] == True:
         print("Las estaciones "+station1+" y "+station2+" sí estan conectadas.")
    else:
         print("Las estaciones "+station1+" y "+station2+" no estan conectadas.")

def optionEight():
    mapa = controller.req6(cont, lon1, lat1, lon2, lat2)
    startStation = controller.estacionMasCercanaStart(mapa)
    endStation = controller.estacionMasCercanaEnd(mapa)
    tiempo = controller.tiempoRecorrido(mapa)
    estaciones = controller.estacionesRecorrido(mapa)
    print("\nLa estación de inicio más cercana es: " + startStation)
    print("La estación de destino más cercana es: " + endStation)
    print("Las estaciones recorridas, en orden, son: ")
    if estaciones != None:
        iterator = it.newIterator(estaciones)
        while it.hasNext(iterator):
            station = it.next(iterator)
            station = station["vertexA"] + " --> " + station["vertexB"]
            print(" " + station)
    else:
        print("No existe un recorrido")
    print("El tiempo del recorrido es: " + tiempo + " segundos")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo1, number=1)
        print("Tiempo de ejecución: " + str(executiontime) + " segundos")

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime) + " segundos")

    elif int(inputs[0]) == 4:
        print()

    elif int(inputs[0]) == 5:
        print()

    elif int(inputs[0]) == 6:
        print()

    elif int(inputs[0]) == 7:
        print()
    
    elif int(inputs[0]) == 8:
        lon1 = input("\nInserte la longitud geográfica del usuario: ")
        lat1 = input("Inserte la latitud geográfica del usuario: ")
        lon2 = input("Inserte la longitud geográfica del lugar a visitar: ")
        lat2 = input("Inserte la latitud geográfica del lugar a visitar: ")
        executiontime = timeit.timeit(optionEight, number=1)
        print("Tiempo de ejecución: " + str(executiontime) + " segundos")

    else:
        sys.exit(0)
sys.exit(0)