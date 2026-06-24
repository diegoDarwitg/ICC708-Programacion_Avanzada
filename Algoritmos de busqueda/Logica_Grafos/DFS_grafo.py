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


def dfs_grafo(adyacencia, inicio, fin):
    visitados = []
    padre = {inicio: None}
    pila = [inicio]

    while pila:
        nodo = pila.pop()
        if nodo in visitados:
            continue
        visitados.append(nodo)
        if nodo == fin:
            ruta = _reconstruir(padre, inicio, fin)
            return visitados, ruta, _costo_ruta(adyacencia, ruta)
        for vecino, _peso in adyacencia.get(nodo, []):
            if vecino not in visitados:
                padre[vecino] = nodo
                pila.append(vecino)

    return visitados, [], 0
