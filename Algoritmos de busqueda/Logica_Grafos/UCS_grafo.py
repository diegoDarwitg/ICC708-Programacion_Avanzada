import heapq


def _reconstruir(padre, inicio, fin):
    ruta = []
    nodo = fin
    while nodo is not None:
        ruta.append(nodo)
        nodo = padre[nodo]
    ruta.reverse()
    return ruta if ruta and ruta[0] == inicio else []


def ucs_grafo(adyacencia, inicio, fin):
    visitados = []
    padre = {inicio: None}
    costo = {inicio: 0}
    heap = [(0, inicio)]

    while heap:
        g, nodo = heapq.heappop(heap)
        if nodo in visitados:
            continue
        visitados.append(nodo)
        if nodo == fin:
            ruta = _reconstruir(padre, inicio, fin)
            return visitados, ruta, g

        for vecino, peso in adyacencia.get(nodo, []):
            nuevo_costo = g + peso
            if vecino not in costo or nuevo_costo < costo[vecino]:
                costo[vecino] = nuevo_costo
                padre[vecino] = nodo
                heapq.heappush(heap, (nuevo_costo, vecino))

    return visitados, [], 0
