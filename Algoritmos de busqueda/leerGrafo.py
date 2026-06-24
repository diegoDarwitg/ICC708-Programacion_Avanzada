import csv


def cargar_grafo(ruta_archivo):
    coordenadas = {}
    adyacencia = {}

    try:
        with open('grafo.csv', 'r') as archivo:
            lector = list(csv.reader(archivo))
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_archivo}")
        return None, None

    modo = 'nodos'
    for fila in lector:
        if not fila:
            continue
        primero = fila[0].strip().lower()

        if primero == 'nodo':
            modo = 'nodos'
            continue
        if primero == 'aristas':
            modo = 'aristas'
            continue

        if modo == 'nodos':
            nombre, x, y = fila[0].strip(), float(fila[1]), float(fila[2])
            coordenadas[nombre] = (x, y)
            adyacencia.setdefault(nombre, [])
        elif modo == 'aristas':
            origen, destino, peso = fila[0].strip(), fila[1].strip(), float(fila[2])
            adyacencia.setdefault(origen, []).append((destino, peso))
            adyacencia.setdefault(destino, []).append((origen, peso))  # grafo no dirigido

    return coordenadas, adyacencia
