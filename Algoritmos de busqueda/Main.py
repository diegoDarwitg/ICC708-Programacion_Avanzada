from leerLaberinto import cargar_laberinto
from leerGrafo import cargar_grafo
from ventanaPrincipal import visualizar_laberinto

if __name__ == "__main__":
    archivo_laberinto = 'laberinto.csv'
    archivo_grafo = 'grafo.csv'

    matriz = cargar_laberinto(archivo_laberinto)
    coordenadas, adyacencia = cargar_grafo(archivo_grafo)

    visualizar_laberinto(matriz, coordenadas, adyacencia)