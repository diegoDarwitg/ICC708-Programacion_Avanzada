from collections import deque

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

def bfs(matriz, inicio, fin):
    visitados = []
    padre = {inicio: None}
    cola = deque([inicio])

    while cola:
        nodo = cola.popleft()
        visitados.append(nodo)
        if nodo == fin:
            ruta = _reconstruir(padre, inicio, fin)
            return visitados, ruta, max(0, len(ruta) - 1)
        for v in _vecinos(matriz, *nodo):
            if v not in padre:
                padre[v] = nodo
                cola.append(v)

    return visitados, [], 0