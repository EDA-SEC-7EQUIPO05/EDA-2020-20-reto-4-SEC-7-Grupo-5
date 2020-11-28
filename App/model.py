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
from math import inf
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.calculos import distances as c
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
    Adiciona la información de un viaje al grafo
    """
    id_origin = str(trip["start station id"])
    id_destination = str(trip["end station id"])
    lat_origin = str(trip["start station latitude"])
    lon_origin = str(trip["start station longitude"])
    lat_destination = str(trip["end station latitude"])
    lon_destination = str(trip["end station longitude"])
    origin = id_origin + ";" + lon_origin +  ";" + lat_origin
    destination = id_destination + ";" + lon_destination +  ";" + lat_destination
    duration = int(trip["tripduration"])
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)
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
        gr.addEdge(citibike["graph"], origin, destination, weight)
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

def numClusters(clusters):
    return scc.connectedComponents(clusters)

def sameCluster(clusters, station1, station2):
    return scc.stronglyConnected(clusters, station1, station2)

def req1(citibike, station1, station2):
    clusters = scc.KosarajuSCC(citibike['graph'])
    num = numClusters(clusters)
    connected = sameCluster(clusters, station1, station2)
    return (num, connected)

def req6(citibike, lon1, lat1, lon2, lat2):
    mapa = {
        "masCercanaStart": None,
        "masCercanaEnd": None,
        "tiempo": 0,
        "estaciones": None
    }
    StartStation = estacionMasCercana(citibike, lon1, lat1)
    EndStation = estacionMasCercana(citibike, lon2, lat2)
    search = djk.Dijkstra(citibike["graph"], StartStation)
    if djk.hasPathTo(search, EndStation):
        mapa["tiempo"] = str(djk.distTo(search, EndStation))
        mapa["estaciones"] = djk.pathTo(search, EndStation)
    else:
        mapa["tiempo"] = "Infinito"
    mapa["masCercanaStart"] = StartStation.split(";")[0]
    mapa["masCercanaEnd"] = EndStation.split(";")[0]
    return mapa

def estacionMasCercanaStart(mapa):
    return mapa["masCercanaStart"]

def estacionMasCercanaEnd(mapa):
    return mapa["masCercanaEnd"]

def tiempoRecorrido(mapa):
    return mapa["tiempo"]

def estacionesRecorrido(mapa):
    return mapa["estaciones"]

# ==============================
# Funciones Helper
# ==============================

def estacionMasCercana(citibike, lon_user, lat_user):
    station = None
    estaciones = gr.vertices(citibike['graph'])
    iterator = it.newIterator(estaciones)
    menor = inf
    while it.hasNext(iterator):
        estacion = it.next(iterator)
        estacion = estacion.split(";")
        id_station = estacion[0]
        lon_station = estacion[1]
        lat_station = estacion[2]
        lon = abs(float(lon_station) - float(lon_user))
        lat = abs(float(lat_station) - float(lat_user))
        distance = c.calcularDistancia(1, lon, lat)
        if distance < menor:
            menor = distance
            station = ";".join(estacion)
    return station

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