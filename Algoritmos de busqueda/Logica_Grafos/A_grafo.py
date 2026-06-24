import heapq
import math


def _reconstruir(padre, inicio, fin):
    ruta = []
    nodo = fin
    while nodo is not None:
        ruta.append(nodo)
        nodo = padre[nodo]
    ruta.reverse()
    return ruta if ruta and ruta[0] == inicio else []


def _heuristica(coordenadas, a, b):
    xa, ya = coordenadas[a]
    xb, yb = coordenadas[b]
    return math.dist((xa, ya), (xb, yb))


def a_estrella_grafo(adyacencia, coordenadas, inicio, fin):

    visitados = []
    padre = {inicio: None}
    g = {inicio: 0}
    heap = [(_heuristica(coordenadas, inicio, fin), 0, inicio)]

    while heap:
        _, costo_g, nodo = heapq.heappop(heap)
        if nodo in visitados:
            continue
        visitados.append(nodo)
        if nodo == fin:
            ruta = _reconstruir(padre, inicio, fin)
            return visitados, ruta, costo_g

        for vecino, peso in adyacencia.get(nodo, []):
            nuevo_g = costo_g + peso
            if vecino not in g or nuevo_g < g[vecino]:
                g[vecino] = nuevo_g
                padre[vecino] = nodo
                f = nuevo_g + _heuristica(coordenadas, vecino, fin)
                heapq.heappush(heap, (f, nuevo_g, vecino))

    return visitados, [], 0
