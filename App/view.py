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
from DISClib.ADT import stack
import timeit
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
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

def optionFive():
    info1=controller.req3primero(cont)
    info2=controller.req3segundo(cont)

    print("Las estaciones con más viajes de salida son: "+str(info1)+" "+"Y las estaciones con mas viajes de llegada son: "+str(info2))

def optionSix():
    station = input("Estación de salida: ")
    tiempo = int(input("Tiempo de resistencia: "))
    info = controller.req4(cont, station, tiempo)
    infoIterator = it.newIterator(info)
    con = 1
    while it.hasNext(infoIterator):
        elemento = it.next(infoIterator)
        print('Opción', con)
        print(elemento)
        print('*************************')
        con +=1

def optionSeven():
    age = int(input("Edad de consulta: "))
    info = controller.req5(cont, age)
    if info is None:
        print("No hay información de esa edad.")
    elif info[0]:
        print("Primera estación:", info[1]['first']["vertexA"])
        print("Última estación:", info[1]['last']["vertexB"])
        iterator = it.newIterator(info[1]['route'])
        print("Ruta:")
        while it.hasNext(iterator):
            elem = it.next(iterator)
            print("\t", elem['vertexA'])
        print("\t", info[1]['last']["vertexB"])
    else:
        print("Noy hay camino entre las estaciones más populares. Estas son:", info[1],"-",info[2])

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
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        print()

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 6:
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    
    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))


    else:
        sys.exit(0)
sys.exit(0)