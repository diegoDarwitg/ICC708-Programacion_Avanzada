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

def dfs(matriz, inicio, fin):
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
            return visitados, ruta, max(0, len(ruta) - 1)
        for v in _vecinos(matriz, *nodo):
            if v not in visitados:
                padre[v] = nodo
                pila.append(v)

    return visitados, [], 0