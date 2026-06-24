import heapq

def _vecinos(matriz, f, c):
    filas, columnas = matriz.shape
    for df, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nf, nc = f + df, c + dc
        if 0 <= nf < filas and 0 <= nc < columnas and matriz[nf, nc] == 0:
            yield (nf, nc)

def _reconstruir(padre, inicio, fin):
    ruta = []
    nodo = fin
    while nodo is not None:
        ruta.append(nodo)
        nodo = padre[nodo]
    ruta.reverse()
    return ruta if ruta[0] == inicio else []

def ucs(matriz, inicio, fin):
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
            return visitados, _reconstruir(padre, inicio, fin), g
        for v in _vecinos(matriz, *nodo):
            nuevo_costo = g + 1
            if v not in costo or nuevo_costo < costo[v]:
                costo[v] = nuevo_costo
                padre[v] = nodo
                heapq.heappush(heap, (nuevo_costo, v))

    return visitados, [], 0