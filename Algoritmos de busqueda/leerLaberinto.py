import csv
import numpy as np

def cargar_laberinto(ruta_archivo):
    laberinto = []
    try:
        with open('laberinto.csv', 'r') as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                if not fila:
                    continue
                fila_numeros = [int(celda) for celda in fila]
                laberinto.append(fila_numeros)
        return np.array(laberinto)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_archivo}")
        return None