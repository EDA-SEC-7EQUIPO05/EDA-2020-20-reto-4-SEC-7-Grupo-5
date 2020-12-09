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
from DISClib.ADT import stack as st
from DISClib.ADT import queue as q
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
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
                    'trips': None,
                    'id-name': None
                    }

        citibike['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=1000,
                                              comparefunction=compareStations)

        citibike['trips'] = m.newMap(numelements=1000,
                                        maptype='CHAINING',
                                        comparefunction=compareStations)
                                        
        citibike['id-name'] = m.newMap(numelements=1000,
                                        maptype='CHAINING',
                                        comparefunction=compareStations)
        return citibike
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo

def addTrip (citibike, trip):
    """
    """
    originid = trip["start station id"]
    destinationid = trip["end station id"]
    origin = trip["start station name"]
    destination = trip["end station name"]
    if origin != destination:
        duration = int(trip["tripduration"])
        birthDate = int(trip['birth year'])
        user = trip["usertype"]
        if user == 'Customer':
            user = True
        else:
            user = False
        age = ageCalculator(birthDate)
        addStation(citibike,origin,originid)
        addStation(citibike,destination, destinationid)
        addConnection(citibike,origin,destination,duration,age, user)
        addAgeTrip(citibike, origin, destination, age)
        citibike['Num'] += 1

def addStation (citibike,stationId, stationId_2):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex (citibike["graph"], stationId):
        gr.insertVertex( citibike["graph"],stationId)
    if not m.contains(citibike["trips"], stationId):
        originAgeMap = m.newMap(numelements=10, maptype='CHAINING', comparefunction=compareAges)
        destinyAgeMap = m.newMap(numelements=10, maptype='CHAINING', comparefunction=compareAges)
        m.put(citibike["trips"], stationId, {'salidas': {'num': 0, 'age': originAgeMap}, 'llegadas':  {'num': 0, 'age': destinyAgeMap}})
    if not m.contains(citibike["id-name"], stationId_2):
        m.put(citibike["id-name"], stationId_2, stationId)
    return citibike

def addConnection (citibike,origin,destination,duration,age, user):
    """
    Adiciona un arco entre dos estaciones 
    """
    originEntry = me.getValue(m.get(citibike['trips'], origin))
    originEntry['salidas']['num'] += 1
    destinyEntry = me.getValue(m.get(citibike['trips'], destination))
    destinyEntry['llegadas']['num'] += 1
    edge = gr.getEdge(citibike ["graph"], origin, destination)
    if edge is None:
        weight = [duration, 1]
        ageMap = newAgeMap()
        gr.addEdge(citibike["graph"], origin, destination, weight)
        edge = gr.getEdge(citibike["graph"], origin, destination)
        edge['age'] = ageMap
        if user:
            edge_1 = gr.getEdge(citibike["graph"], origin, destination)
            Entry = m.get(edge_1['age'], representativeAge(age))
            Value = Entry['value']
            Value['num'] += 1
    else:
        edge['weight'][0] = (edge['weight'][0]*edge['weight'][1] + duration)/(edge['weight'][1] + 1)
        edge['weight'][1] += 1
        if user:
            ageMapEntry = me.getValue(m.get(edge['age'], representativeAge(age)))
            ageMapEntry['num'] += 1
    return citibike

def newAgeMap():
    ageMap = m.newMap(numelements=8,maptype='CHAINING',loadfactor=2,comparefunction=compareAges)
    for i in range(5,75,10):
        m.put(ageMap, representativeAge(i), {'num': 0})
    return ageMap

def addAgeTrip(citibike, origin, destination, age):
    rep_age = representativeAge(age)
    originAgeMap = me.getValue(m.get(citibike['trips'], origin))['salidas']['age']
    destinyAgeMap = me.getValue(m.get(citibike['trips'], destination))['llegadas']['age']
    if not m.contains(originAgeMap, rep_age):
        m.put(originAgeMap, rep_age, {'num': 1})
    else:
        me.getValue(m.get(originAgeMap, rep_age))['num'] += 1
    if not m.contains(destinyAgeMap, rep_age):
        m.put(destinyAgeMap, rep_age,{'num': 1})
    else:
        me.getValue(m.get(destinyAgeMap, rep_age))['num'] += 1

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

def req2(citibike, station, low_time, high_time):
    kosaraju = scc.KosarajuSCC(citibike['graph'])
    rev_citibike = scc.reverseGraph(citibike['graph'])
    adjs = gr.adjacents(rev_citibike, station, cmpfunction=compareVertex)
    if lt.isEmpty(adjs):
        return None
    component = me.getValue(m.get(kosaraju['idscc'], station))
    paths = circularPathSearch(citibike['graph'], kosaraju, component, station, adjs, low_time, high_time)
    return paths



def req4(citibike, station, time):
    search = dfsParcial(citibike["graph"], station, time)
    return routeList(citibike["graph"], search, station)

def req5(citibike, age):
    max_in = 0
    max_in_st = None
    max_in_2 = 0
    max_in_st_2 = None
    max_out = 0
    max_out_st = None
    rep_age = representativeAge(age)
    stations = m.keySet(citibike['trips'])
    stationIterator = it.newIterator(stations)
    while it.hasNext(stationIterator):
        elem = it.next(stationIterator)
        salidaEntry = m.get(me.getValue(m.get(citibike['trips'], elem))['salidas']['age'], rep_age)
        llegadaEntry = m.get(me.getValue(m.get(citibike['trips'], elem))['llegadas']['age'], rep_age)
        if salidaEntry is None:
            salida = 0
        else: 
            salida = me.getValue(salidaEntry)['num']
        if llegadaEntry is None:
            llegada = 0
        else:
            llegada = me.getValue(llegadaEntry)['num']
        if salida > max_out:
            max_out = salida
            max_out_st = elem
        if llegada > max_in:
            max_in_2 = max_in
            max_in_st_2 = max_in_st
            max_in = llegada
            max_in_st = elem
    if max_in_st == max_out_st:
        max_in_st = max_in_st_2
    if max_in_st is None or max_out_st is None:
        return None
    elif shortRoute(citibike, max_out_st, max_in_st) is not None:
        return True, shortRoute(citibike, max_out_st, max_in_st)
    else:
        return False, max_out_st, max_in_st
    
def req7(citibike, ageRange):
    maxEdges = lt.newList()
    maxEdgeNum = 0
    edges = gr.edges(citibike['graph'])
    edgeIterator = it.newIterator(edges)
    while it.hasNext(edgeIterator):
        edge = it.next(edgeIterator) 
        ageMap = edge['age']
        ageMapEntry = m.get(ageMap, ageRange)
        num = ageMapEntry['value']['num']
        if num == maxEdgeNum:
            lt.addLast(maxEdges, edge)
        elif num > maxEdgeNum:
            maxEdgeNum = num
            maxEdges = lt.newList()
            lt.addLast(maxEdges, edge)
    if maxEdgeNum == 0:
        return None
    else:
        return maxEdges




# ==============================
# Funciones Helper
# ==============================

def dijsktra(citibike, station):
    return djk.Dijkstra(citibike, station)

def circularPathSearch(graph, kosaraju, component, station, adjacents, low_time, high_time):
    circularPaths = lt.newList()
    verts = m.keySet(kosaraju['idscc'])
    vertIterator = it.newIterator(verts)
    while it.hasNext(vertIterator):
        elem = it.next(vertIterator)
        comp = me.getValue(m.get(kosaraju['idscc'], elem))
        edge = gr.getEdge(graph, station, elem)
        if comp == component and edge is not None:
            search = circularDepthSearch(graph, kosaraju, station, elem, component, adjacents, high_time)
            adjIterator = it.newIterator(adjacents)
            while it.hasNext(adjIterator):
                adj = it.next(adjIterator)
                entry = m.get(search['visited'], adj)
                if entry is not None:
                    time = me.getValue(entry)['time'] + gr.getEdge(graph, adj, station)['weight'][0]
                    if time >= low_time and time <= high_time:
                        lt.addLast(circularPaths,routeBuild_2(graph, search, station, adj, m.keySet(search['visited']), control=True))
    return circularPaths

def circularDepthSearch(graph, kosaraju, source, station, component, adjacents, high_time):
    search = {
                  'visited': None,
                  'source': source
                  }
    search['visited'] = m.newMap(numelements=gr.numVertices(graph),
                                       maptype='PROBING',
                                       comparefunction=graph['comparefunction']
                                       )
    m.put(search['visited'], source, {'marked': True, 'edgeTo': None, 'time': 0})
    edge = gr.getEdge(graph, source, station)
    if edge is not None:
        m.put(search['visited'], station, {'marked': True, 'edgeTo': source, 'time': edge['weight'][0]})
        vertexCircularDepthSearch(search, kosaraju, component, graph, adjacents, station, high_time)
        return search
    

def vertexCircularDepthSearch(search, kosaraju, component, graph, adjacents, station, high_time):
    adjlst = gr.adjacents(graph, station)
    adjslstiter = it.newIterator(adjlst)
    while (it.hasNext(adjslstiter)):
            w = it.next(adjslstiter)
            if me.getValue(m.get(kosaraju['idscc'], w)) == component:
                visited = m.get(search['visited'], w)
                if visited is None:
                    root = me.getValue(m.get(search['visited'], station))
                    temp = gr.getEdge(graph, station, w)["weight"][0]
                    if (root['time'] + temp+20) <= high_time:
                        m.put(search['visited'],
                            w, {'marked': True, 'edgeTo': station, 'time': (root["time"] + temp+20)})
                        if lt.isPresent(adjacents, w):
                            continue
                        vertexCircularDepthSearch(search, kosaraju, component, graph, adjacents, w, high_time)

def dfsParcial(graph, source, time):
    search = {
                  'source': source,
                  'visited': None
                  }

    search['visited'] = m.newMap(numelements=gr.numVertices(graph),
                                       maptype='PROBING',
                                       comparefunction=graph['comparefunction']
                                       )

    m.put(search['visited'], source, {'marked': True, 'edgeTo': None, 'time': 0})
    vertexDepthSearch(search, graph, source, time, True)
    return search

def vertexDepthSearch(search, graph, vertex, time, source):
    adjlst = gr.adjacents(graph, vertex)
    if source:
        adjslstiter = it.newIterator(adjlst)
        while (it.hasNext(adjslstiter)):
            w = it.next(adjslstiter)
            visited = m.get(search['visited'], w)
            if visited is None:
                temp = gr.getEdge(graph, vertex, w)["weight"][0]
                if (temp) <= time:
                    m.put(search['visited'],
                        w, {'marked': True, 'edgeTo': vertex, 'time': temp})
                    vertexDepthSearch(search, graph, w, time, False)
    else:
        if lt.size(adjlst) > 0:
            x = True
            adjslstiter = it.newIterator(adjlst)
            while x and it.hasNext(adjslstiter):
                w = it.next(adjslstiter)
                visited = m.get(search['visited'], w)
                if visited is None:
                    root = me.getValue(m.get(search['visited'], vertex))
                    temp = gr.getEdge(graph, vertex, w)["weight"][0]
                    if (root['time'] + temp) <= time:
                        x = False
                        m.put(search['visited'],
                            w, {'marked': True, 'edgeTo': vertex, 'time': (root["time"] + temp)})
                        vertexDepthSearch(search, graph, w, time, False)
    return search

def routeBuild_2(graph, search, vertexA, vertexB, keys, control=False):
    visited = search["visited"]
    iterator = it.newIterator(keys)
    ruta = ''
    if vertexA == vertexB:
        return ruta
    while it.hasNext(iterator):
        elemento = it.next(iterator)
        if me.getValue(m.get(visited, vertexB))["edgeTo"] == elemento:
            ruta = elemento + " --> " + vertexB + " costo: " + str(gr.getEdge(graph, elemento, vertexB)["weight"][0]) + "\n"+ruta
            ruta = routeBuild_2(graph, search, vertexA, elemento, keys) + ruta
            break
    if control:
        ruta += vertexB + " --> " + vertexA + " costo: " + str(gr.getEdge(graph, vertexB, vertexA)["weight"][0]) + "\n"
    return ruta

def routeBuild(graph, search, vertexA, vertexB, keys):
    visited = search["visited"]
    iterator = it.newIterator(keys)
    ruta = ''
    if vertexA == search['source']:
        ruta += vertexA + " --> " + vertexB + " costo: " + str(gr.getEdge(graph, vertexA, vertexB)["weight"][0]) + "\n"
    while it.hasNext(iterator):
        elemento = it.next(iterator)
        if me.getValue(m.get(visited, elemento))["edgeTo"] == vertexB:
            ruta += vertexB + " --> " + elemento + " costo: " + str(gr.getEdge(graph, vertexB, elemento)["weight"][0]) + "\n"
            ruta += routeBuild(graph, search, vertexB, elemento, keys)
    return ruta

def routeList(graph, search, source):
    routes = lt.newList(datastructure="SINGLE_LINKED")
    visited = search["visited"]
    keys = m.keySet(visited)
    iterator = it.newIterator(keys)
    while it.hasNext(iterator):
        elemento = it.next(iterator)
        if me.getValue(m.get(visited, elemento))["edgeTo"] == source:
            lt.addLast(routes, routeBuild(graph, search, source, elemento, keys))
    return routes



def representativeAge(age):
    if age >= 0 and age <= 10:
        return '0-10'
    elif age >= 11 and age <= 20:
        return '11-20'
    elif age >= 21 and age <= 30:
        return '21-30'
    elif age >= 31 and age <= 40:
        return '31-40'
    elif age >= 41 and age <= 50:
        return '41-50'
    elif age >= 51 and age <=60:
        return '51-60'
    else:
        return '60+'

def  ageCalculator(birth_year):
    return 2020-birth_year

def shortRoute(citibike, origin, destination):
    dijs = dijsktra(citibike['graph'], origin)
    path = djk.pathTo(dijs, destination)
    return routeFormat(path)

def routeFormat(path):
    if st.top(path) is None:
        return None
    else:
        listPath = lt.newList(datastructure = 'SINGLE_LINKED')
        while not st.isEmpty(path):
            lt.addLast(listPath, st.pop(path))
        first = lt.firstElement(listPath)
        last = lt.lastElement(listPath)
        route = {'first': first, 'last': last, 'route': listPath}
        return route


# ==============================
# Funciones de Comparacion
# ==============================

def compareStations (stop,keyvaluestop):
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

def compareAges(age, keyvalueage):
    agecode = keyvalueage['key']
    if age == agecode:
        return 0
    elif age > agecode:
        return 1
    else:
        return -1

def compareVertex(ver1, ver2):
    if ver1 == ver2:
        return 0
    elif ver1 > ver2:
        return 1
    else:
        return -1