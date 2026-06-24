from collections import deque

def _reconstruir(padre, inicio, fin):
    ruta = []
    nodo = fin
    while nodo is not None:
        ruta.append(nodo)
        nodo = padre[nodo]
    ruta.reverse()
    return ruta if ruta and ruta[0] == inicio else []


def _costo_ruta(adyacencia, ruta):
    if not ruta:
        return 0
    costo = 0
    for i in range(len(ruta) - 1):
        actual, siguiente = ruta[i], ruta[i + 1]
        for vecino, peso in adyacencia[actual]:
            if vecino == siguiente:
                costo += peso
                break
    return costo


def bfs_grafo(adyacencia, inicio, fin):

    visitados = []
    padre = {inicio: None}
    cola = deque([inicio])

    while cola:
        nodo = cola.popleft()
        visitados.append(nodo)
        if nodo == fin:
            ruta = _reconstruir(padre, inicio, fin)
            return visitados, ruta, _costo_ruta(adyacencia, ruta)
        for vecino, _peso in adyacencia.get(nodo, []):
            if vecino not in padre:
                padre[vecino] = nodo
                cola.append(vecino)

    return visitados, [], 0
