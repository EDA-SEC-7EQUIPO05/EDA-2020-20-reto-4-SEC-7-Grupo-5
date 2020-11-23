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
                    'Num': 0
                    }

        citibike['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=1000,
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
    return citibike

def addConnection (citibike,origin,destination,duration):
    """
    Adiciona un arco entre dos estaciones 
    """
    edge = gr.getEdge(citibike ["graph"], origin, destination)
    if edge is None:
        weight = [duration, 1]
        count=1
        gr.addEdge(citibike["graph"], origin, destination, weight,count)
    else:
        edge['weight'][0] = (edge['weight'][0]*edge['weight'][1] + duration)/(edge['weight'][1] + 1)
        edge['weight'][1] += 1

    return citibike

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

def indegreereq3 (citibike):
    lista=[]
    vertices=gr.vertices(citibike["graph"])
    iterator=it.newIterator(vertices)
    while it.hasNext(iterator):
        element=it.next(iterator)
        valor=gr.indegree(citibike["graph"],element)
        lista.append(valor)
    orden=sorted(lista)
    return orden

def outdegreereq3 (citibike):
    lista1=[]
    vertices=gr.vertices(citibike["graph"])
    iterator=it.newIterator(vertices)
    while it.hasNext(iterator):
        element=it.next(iterator)
        valor=gr.outdegree(citibike["graph"],element)
        lista1.append(valor)
    orden1=sorted(lista1)
    return orden1

def degreereq3 (citibike):
    lista2=[]
    vertices=gr.vertices(citibike["graph"])
    iterator=it.newIterator(vertices)
    while it.hasNext(iterator):
        element=it.next(iterator)
        valor=gr.degree(citibike["graph"],element)
        lista2.append(valor)
    orden2=sorted(lista2)
    return orden2


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