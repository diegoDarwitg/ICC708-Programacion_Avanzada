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

def _heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_estrella(matriz, inicio, fin):
    visitados = []
    padre = {inicio: None}
    g = {inicio: 0}
    heap = [(_heuristica(inicio, fin), 0, inicio)]

    while heap:
        _, costo_g, nodo = heapq.heappop(heap)
        if nodo in visitados:
            continue
        visitados.append(nodo)
        if nodo == fin:
            return visitados, _reconstruir(padre, inicio, fin), costo_g
        for v in _vecinos(matriz, *nodo):
            nuevo_g = costo_g + 1
            if v not in g or nuevo_g < g[v]:
                g[v] = nuevo_g
                padre[v] = nodo
                f = nuevo_g + _heuristica(v, fin)
                heapq.heappush(heap, (f, nuevo_g, v))

    return visitados, [], 0