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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.Algorithms.Graphs import bfs as at
from DISClib.Algorithms.Graphs import dfo as wt
from DISClib.Algorithms.Graphs import dfs as xt
from DISClib.DataStructures import graphstructure as mt
from DISClib.DataStructures import mapentry as me
from itertools import zip_longest
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador
   graph: Grafo para representar las rutas entre estaciones
    """
    try:
        citibike = {
                    'graph': None, 
                    'Num': 0,
                    "arrivals":None

                    }

        citibike['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=1000,
                                              comparefunction=compareStations) 

        citibike["salida"] = m.newMap(numelements=2000,
                                              maptype="PROBING",
                                              comparefunction=compareStations) 
        citibike["llegada"] = m.newMap(numelements=2000,
                                              maptype="PROBING",
                                              comparefunction=compareStations)
          
        return citibike
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo

def addTrip (citibike, trip):
    """
    """
    origin = trip["start station id"]
    destination = trip["end station id"]
    duration = int(trip["tripduration"])
    addStation(citibike,origin)
    addStation(citibike,destination)
    addConnection(citibike,origin,destination,duration)
    citibike['Num'] += 1

def addStation (citibike,stationId):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex (citibike["graph"], stationId):
        gr.insertVertex( citibike["graph"],stationId)
    if not m.contains(citibike["salida"],stationId):
        m.put(citibike["salida"],stationId,{"salidas":0})
    if not m.contains(citibike["llegada"],stationId):
        m.put(citibike["llegada"],stationId,{"llegadas":0})
    return citibike

def addConnection (citibike,origin,destination,duration):
    """
    Adiciona un arco entre dos estaciones 
    """
    originEntry= me.getValue(m.get(citibike["salida"],origin))
    originEntry["salidas"]+=1
    destinyEntry=me.getValue(m.get(citibike["llegada"],destination))
    destinyEntry["llegadas"] +=1
    edge = gr.getEdge(citibike ["graph"], origin, destination)
    if edge is None:
        weight = [duration, 1]
        gr.addEdge(citibike["graph"], origin, destination, weight)
    else:
        edge['weight'][0] = (edge['weight'][0]*edge['weight'][1] + duration)/(edge['weight'][1] + 1)
        edge['weight'][1] += 1

    return citibike

def addtrips (citibke,stationId):
     try:
        if not gr.containsVertex(citibke['graph'], stationId):
            gr.insertVertex(citibke['graph'], stationId)
        return analyzer
     except Exception as exp:
        error.reraise(exp, 'model:addstop')
# ==============================
# Funciones de consulta
# ==============================

def totalTrips(citibike):
    return citibike['Num']

def totalConnections(citibike):
    graph = citibike["graph"]
    return gr.numEdges(graph)

def totalStations(citibike):
    graph = citibike["graph"]
    return gr.numVertices(graph)

def req1(citibike, station1, station2):
    clusters = scc.KosarajuSCC(citibike['graph'])
    num = numClusters(clusters)
    connected = sameCluster(clusters, station1, station2)
    return (num, connected)

def numClusters(clusters):
    return scc.connectedComponents(clusters)

def sameCluster(clusters, station1, station2):
    return scc.stronglyConnected(clusters, station1, station2)

def req3primero (citibike):
    lista=[]
    lista2=[]
    lista3=[]
    llaves=m.keySet(citibike["salida"])
    valores=m.valueSet(citibike["salida"])
    iterator_llaves=it.newIterator(llaves)
    iterator_valores=it.newIterator(valores)
    while it.hasNext(iterator_llaves) and it.hasNext(iterator_valores):
        key = it.next(iterator_llaves)
        value = it.next(iterator_valores)
        lista.append(value)
        lista2.append([key,value])

    for i in lista:
        valor=i
        for k in valor:
            numeros=valor[k]
            lista3.append(numeros)
    lista3.sort()
    mayor=max(lista3)
    eliminacion=lista3.remove(mayor)
    mayor1=max(lista3)
    eliminacion1=lista3.remove(mayor1)
    mayor2=max(lista3)

    for i in lista:
        valor=i
        for k in valor:
            numeros=valor[k]
            if numeros==mayor:
                respuesta=valor
            elif numeros==mayor1:
                respuesta1=valor
            elif numeros==mayor2:
                respuesta2=valor

    final=respuesta
    final1=respuesta1
    final2=respuesta2

    for u in lista2:
        valor=u
        for v in valor:
            solucion=v
            opcion=final
            opcion1=final1
            opcion2=final2
            if solucion==opcion:
                ultima=valor
            elif solucion==opcion1:
                ultima1=valor
            elif solucion==opcion2:
                ultima2=valor
    return (ultima[0],ultima1[0],ultima2[0])

def req3segundo (citibike):
    lista=[]
    lista2=[]
    lista3=[]
    llaves=m.keySet(citibike["llegada"])
    valores=m.valueSet(citibike["llegada"])
    iterator_llaves=it.newIterator(llaves)
    iterator_valores=it.newIterator(valores)
    while it.hasNext(iterator_llaves) and it.hasNext(iterator_valores):
        key = it.next(iterator_llaves)
        value = it.next(iterator_valores)
        lista.append(value)
        lista2.append([key,value])

    for i in lista:
        valor=i
        for k in valor:
            numeros=valor[k]
            lista3.append(numeros)
    lista3.sort()
    mayor=max(lista3)
    eliminacion=lista3.remove(mayor)
    mayor1=max(lista3)
    eliminacion1=lista3.remove(mayor1)
    mayor2=max(lista3)

    for i in lista:
        valor=i
        for k in valor:
            numeros=valor[k]
            if numeros==mayor:
                respuesta=valor
            elif numeros==mayor1:
                respuesta1=valor
            elif numeros==mayor2:
                respuesta2=valor

    final=respuesta
    final1=respuesta1
    final2=respuesta2

    for u in lista2:
        valor=u
        for v in valor:
            solucion=v
            opcion=final
            opcion1=final1
            opcion2=final2
            if solucion==opcion:
                ultima=valor
            elif solucion==opcion1:
                ultima1=valor
            elif solucion==opcion2:
                ultima2=valor
    return (ultima[0],ultima1[0],ultima2[0])
  
def req3tercero (citibike):
    dic={}
    lista=[]
    lista2=[]
    lista5=[]
    llaves=m.keySet(citibike["llegada"])
    valores=m.valueSet(citibike["llegada"])
    iterator_llaves=it.newIterator(llaves)
    iterator_valores=it.newIterator(valores)
    while it.hasNext(iterator_llaves) and it.hasNext(iterator_valores):
        key = it.next(iterator_llaves)
        value = it.next(iterator_valores)
        lista.append(value)
        lista2.append([key,value])

    for i in lista:
        valor=i
        for k in valor:
            numeros=valor[k]
            lista5.append(numeros)

    lista3=[]
    lista4=[]
    lista6=[]
    llaves1=m.keySet(citibike["salida"])
    valores1=m.valueSet(citibike["salida"])
    iterator_llaves1=it.newIterator(llaves1)
    iterator_valores1=it.newIterator(valores1)
    while it.hasNext(iterator_llaves1) and it.hasNext(iterator_valores1):
        key1 = it.next(iterator_llaves1)
        value1 = it.next(iterator_valores1)
        lista3.append(value1)
        lista4.append([key1,value1])

    for i in lista:
        valor=i
        for k in valor:
            numeros=valor[k]
            lista6.append(numeros)
    
    mayor, menor = (lista5, lista6) if len(lista5) >= len(lista6) else (lista6, lista5)
    lista7=[]
    for i, _ in enumerate(mayor):
        if i + 1 > len(menor):
            lista7.append(mayor[i])
        else:
            lista7.append(mayor[i] + menor[i])

    lista8=[]
    for i in lista7:
        dic[key]=dic.get(key,i)
        lista8.append(dic)
    
    return lista8

            

# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def compareStations (stop,
keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1