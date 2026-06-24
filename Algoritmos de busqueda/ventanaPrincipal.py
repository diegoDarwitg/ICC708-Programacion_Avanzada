import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button, RadioButtons, Slider
from Logica_Laberinto.BFS import bfs
from Logica_Laberinto.DFS import dfs
from Logica_Laberinto.UCS import ucs
from Logica_Laberinto.A import a_estrella
from Logica_Grafos.BFS_grafo import bfs_grafo
from Logica_Grafos.DFS_grafo import dfs_grafo
from Logica_Grafos.UCS_grafo import ucs_grafo
from Logica_Grafos.A_grafo import a_estrella_grafo
from leerGrafo import cargar_grafo

COLOR_PARED    = 'black'
COLOR_CAMINO   = 'white'
COLOR_INICIO   = '#00C853'
COLOR_FIN      = '#D50000'
COLOR_VISITADO = '#90CAF9'
COLOR_RUTA     = '#FFC107'
COLOR_NODO     = '#ECEFF1'
COLOR_ARISTA   = '#90A4AE'

ALGORITMOS_LABERINTO = {
    'BFS': bfs,
    'DFS': dfs,
    'UCS': ucs,
    'A*':  a_estrella,
}

ALGORITMOS_GRAFO = {
    'BFS': bfs_grafo,
    'DFS': dfs_grafo,
    'UCS': ucs_grafo,
    'A*':  a_estrella_grafo,
}

class VisualizadorLaberinto:
    def __init__(self, matriz, coordenadas_grafo=None, adyacencia_grafo=None):
        self.matriz  = np.array(matriz)
        self.filas, self.columnas = self.matriz.shape

        self.coordenadas_grafo = coordenadas_grafo or {}
        self.adyacencia_grafo  = adyacencia_grafo or {}
        self.hay_grafo = bool(self.coordenadas_grafo)

        self.modo = 'laberinto'
        self.inicio  = None
        self.fin     = None
        self.parches = {}
        self.nodos_parches = {}
        self.estado  = 'esperando_inicio'
        self.algoritmo_seleccionado = 'BFS'
        self.velocidad = 0.05
        self.animando  = False

        self._construir_ventana()
        self._dibujar_laberinto()
        self._actualizar_titulo()
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)
        plt.show()

    def _construir_ventana(self):
        self.fig = plt.figure(figsize=(12, 9))

        self.ax = self.fig.add_axes([0.05, 0.10, 0.65, 0.85])

        ax_modo = self.fig.add_axes([0.73, 0.88, 0.24, 0.10])
        ax_modo.set_title('Escenario', fontsize=10, pad=6)
        opciones_modo = ['Laberinto', 'Grafo'] if self.hay_grafo else ['Laberinto']
        self.radio_modo = RadioButtons(ax_modo, opciones_modo, activecolor='#1565C0')
        for label in self.radio_modo.labels:
            label.set_fontsize(10)
        self.radio_modo.on_clicked(self._cambiar_modo)
        if not self.hay_grafo:
            ax_modo.text(0.5, -0.6, '(sin datos de grafo)', transform=ax_modo.transAxes,
                         fontsize=7, ha='center', color='gray')

        ax_radio = self.fig.add_axes([0.73, 0.55, 0.24, 0.28])
        ax_radio.set_title('Algoritmo', fontsize=10, pad=6)
        self.radio = RadioButtons(ax_radio, list(ALGORITMOS_LABERINTO.keys()), activecolor='#1565C0')
        for label in self.radio.labels:
            label.set_fontsize(11)
        self.radio.on_clicked(self._cambiar_algoritmo)

        ax_slider = self.fig.add_axes([0.73, 0.44, 0.24, 0.04])
        self.slider = Slider(
            ax_slider, 'Velocidad',
            valmin=0.0, valmax=1.0,
            valinit=0.5,
            color='#1565C0'
        )
        self.slider.valtext.set_visible(False)
        ax_slider.text(0.0, -1.2, 'Rápido', transform=ax_slider.transAxes, fontsize=8, ha='left')
        ax_slider.text(1.0, -1.2, 'Lento',  transform=ax_slider.transAxes, fontsize=8, ha='right')
        self.slider.on_changed(self._cambiar_velocidad)
        self._cambiar_velocidad(0.5)

        ax_buscar = self.fig.add_axes([0.73, 0.33, 0.24, 0.08])
        ax_reset  = self.fig.add_axes([0.73, 0.23, 0.24, 0.08])
        self.btn_buscar = Button(ax_buscar, 'Buscar', color='#E8F5E9', hovercolor='#A5D6A7')
        self.btn_reset  = Button(ax_reset,  'Reset',  color='#FFEBEE', hovercolor='#EF9A9A')
        self.btn_buscar.label.set_fontsize(11)
        self.btn_reset.label.set_fontsize(11)
        self.btn_buscar.on_clicked(lambda e: self._ejecutar())
        self.btn_reset.on_clicked(lambda e: self._reset())

        ax_leyenda = self.fig.add_axes([0.73, 0.10, 0.24, 0.12])
        ax_leyenda.axis('off')
        items = [('#00C853','Inicio'), ('#D50000','Fin'),
                 ('#90CAF9','Visitado'), ('#FFC107','Ruta')]
        for i, (color, label) in enumerate(items):
            y = 0.85 - i * 0.28
            ax_leyenda.add_patch(patches.Rectangle(
                (0, y - 0.08), 0.18, 0.22, color=color,
                transform=ax_leyenda.transAxes))
            ax_leyenda.text(0.25, y + 0.02, label,
                            transform=ax_leyenda.transAxes, fontsize=9, va='center')

    def _cambiar_velocidad(self, val):
        self.velocidad = 0.001 + (val ** 2) * 0.3

    def _dibujar_laberinto(self):
        self.ax.clear()
        self.parches = {}
        for f in range(self.filas):
            for c in range(self.columnas):
                color = COLOR_PARED if self.matriz[f, c] == 1 else COLOR_CAMINO
                rect = patches.Rectangle(
                    (c, f), 1, 1,
                    linewidth=0.5, edgecolor='gray', facecolor=color)
                self.ax.add_patch(rect)
                self.parches[(f, c)] = rect
        self.ax.set_xlim(0, self.columnas)
        self.ax.set_ylim(0, self.filas)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.ax.invert_yaxis()

    def _dibujar_grafo(self):
        self.ax.clear()
        self.nodos_parches = {}

        radio = self._radio_nodo_grafo()

        ya_dibujadas = set()
        for nodo, vecinos in self.adyacencia_grafo.items():
            x1, y1 = self.coordenadas_grafo[nodo]
            for vecino, peso in vecinos:
                clave = frozenset((nodo, vecino))
                if clave in ya_dibujadas:
                    continue
                ya_dibujadas.add(clave)
                x2, y2 = self.coordenadas_grafo[vecino]
                self.ax.plot([x1, x2], [y1, y2], color=COLOR_ARISTA,
                             linewidth=1.5, zorder=1, solid_capstyle='round')

                dx, dy = x2 - x1, y2 - y1
                largo = max((dx ** 2 + dy ** 2) ** 0.5, 1e-6)
                perp_x, perp_y = -dy / largo, dx / largo
                offset = radio * 0.55
                xm = (x1 + x2) / 2 + perp_x * offset
                ym = (y1 + y2) / 2 + perp_y * offset
                self.ax.text(xm, ym, str(peso), fontsize=8, color='#37474F',
                             ha='center', va='center', zorder=2,
                             bbox=dict(boxstyle='round,pad=0.12', fc='white',
                                       ec='none', alpha=0.9))

        for nodo, (x, y) in self.coordenadas_grafo.items():
            circulo = patches.Circle((x, y), radio, facecolor=COLOR_NODO,
                                      edgecolor='#455A64', linewidth=1.5, zorder=3)
            self.ax.add_patch(circulo)
            self.ax.text(x, y, nodo, fontsize=10, fontweight='bold',
                         ha='center', va='center', zorder=4)
            self.nodos_parches[nodo] = circulo

        xs = [p[0] for p in self.coordenadas_grafo.values()]
        ys = [p[1] for p in self.coordenadas_grafo.values()]
        margen = radio * 2.5
        ancho = max(xs) - min(xs)
        alto = max(ys) - min(ys)
        self.ax.set_xlim(min(xs) - margen, max(xs) + margen)
        self.ax.set_ylim(min(ys) - margen, max(ys) + margen)
        self.ax.set_aspect('equal')
        self.ax.axis('off')

    def _radio_nodo_grafo(self):
        puntos = list(self.coordenadas_grafo.values())
        if len(puntos) < 2:
            return 0.3
        distancias = []
        for i in range(len(puntos)):
            for j in range(i + 1, len(puntos)):
                x1, y1 = puntos[i]
                x2, y2 = puntos[j]
                d = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                if d > 1e-9:
                    distancias.append(d)
        dist_min = min(distancias) if distancias else 1.0
        return dist_min * 0.32

    def _escala_grafo(self):
        xs = [p[0] for p in self.coordenadas_grafo.values()]
        ys = [p[1] for p in self.coordenadas_grafo.values()]
        return max(max(xs) - min(xs), max(ys) - min(ys), 1)

    def _actualizar_titulo(self, texto=None):
        if texto:
            self.ax.set_title(texto, fontsize=11, pad=8)
        else:
            if self.modo == 'laberinto':
                mensajes = {
                    'esperando_inicio': 'Clic en celda blanca → INICIO (verde)',
                    'esperando_fin':    'Clic en celda blanca → FIN (rojo)',
                    'listo':            'Puntos listos — elige algoritmo y presiona Buscar',
                }
            else:
                mensajes = {
                    'esperando_inicio': 'Clic en un nodo → INICIO (verde)',
                    'esperando_fin':    'Clic en un nodo → FIN (rojo)',
                    'listo':            'Nodos listos — elige algoritmo y presiona Buscar',
                }
            self.ax.set_title(mensajes.get(self.estado, ''), fontsize=11, pad=8)
        self.fig.canvas.draw_idle()

    def _cambiar_algoritmo(self, label):
        self.algoritmo_seleccionado = label

    def _cambiar_modo(self, label):
        if self.animando:
            return
        nuevo_modo = 'laberinto' if label == 'Laberinto' else 'grafo'
        if nuevo_modo == self.modo:
            return
        self.modo = nuevo_modo
        self.inicio = None
        self.fin    = None
        self.estado = 'esperando_inicio'
        if self.modo == 'laberinto':
            self._dibujar_laberinto()
        else:
            self._dibujar_grafo()
        self._actualizar_titulo()

    def _on_click(self, event):
        if self.animando or event.inaxes != self.ax:
            return
        if self.modo == 'laberinto':
            self._on_click_laberinto(event)
        else:
            self._on_click_grafo(event)

    def _on_click_laberinto(self, event):
        c = int(event.xdata)
        f = int(event.ydata)
        if not (0 <= f < self.filas and 0 <= c < self.columnas):
            return
        if self.matriz[f, c] == 1:
            return

        if self.estado == 'esperando_inicio':
            self.inicio = (f, c)
            self.parches[(f, c)].set_facecolor(COLOR_INICIO)
            self.estado = 'esperando_fin'
        elif self.estado == 'esperando_fin':
            if (f, c) == self.inicio:
                return
            self.fin = (f, c)
            self.parches[(f, c)].set_facecolor(COLOR_FIN)
            self.estado = 'listo'

        self._actualizar_titulo()
        self.fig.canvas.draw_idle()

    def _on_click_grafo(self, event):
        if self.estado not in ('esperando_inicio', 'esperando_fin'):
            return
        radio = self._radio_nodo_grafo()
        mejor_nodo, mejor_dist = None, None
        for nodo, (x, y) in self.coordenadas_grafo.items():
            d = ((event.xdata - x) ** 2 + (event.ydata - y) ** 2) ** 0.5
            if mejor_dist is None or d < mejor_dist:
                mejor_nodo, mejor_dist = nodo, d
        if mejor_nodo is None or mejor_dist > radio * 1.8:
            return

        if self.estado == 'esperando_inicio':
            self.inicio = mejor_nodo
            self.nodos_parches[mejor_nodo].set_facecolor(COLOR_INICIO)
            self.estado = 'esperando_fin'
        elif self.estado == 'esperando_fin':
            if mejor_nodo == self.inicio:
                return
            self.fin = mejor_nodo
            self.nodos_parches[mejor_nodo].set_facecolor(COLOR_FIN)
            self.estado = 'listo'

        self._actualizar_titulo()
        self.fig.canvas.draw_idle()

    def _ejecutar(self):
        if self.animando:
            return
        if self.estado != 'listo':
            self._actualizar_titulo('Primero coloca inicio y fin')
            return

        if self.modo == 'laberinto':
            self._ejecutar_laberinto()
        else:
            self._ejecutar_grafo()

    def _ejecutar_laberinto(self):
        for (f, c), rect in self.parches.items():
            if (f, c) not in (self.inicio, self.fin) and self.matriz[f, c] == 0:
                rect.set_facecolor(COLOR_CAMINO)
        self.fig.canvas.draw_idle()

        fn = ALGORITMOS_LABERINTO[self.algoritmo_seleccionado]
        visitados, ruta, costo = fn(self.matriz, self.inicio, self.fin)

        self.animando = True

        for i, (f, c) in enumerate(visitados):
            if (f, c) in (self.inicio, self.fin):
                continue
            self.parches[(f, c)].set_facecolor(COLOR_VISITADO)
            if i % max(1, int(1 / (self.velocidad * 50 + 1))) == 0:
                self._actualizar_titulo(
                    f'{self.algoritmo_seleccionado} — Explorando... ({i+1}/{len(visitados)})')
                plt.pause(self.velocidad)

        if ruta:
            for f, c in ruta:
                if (f, c) not in (self.inicio, self.fin):
                    self.parches[(f, c)].set_facecolor(COLOR_RUTA)
                    plt.pause(self.velocidad * 1.5)
            titulo = (f'{self.algoritmo_seleccionado} — Costo: {costo} | '
                      f'Ruta: {len(ruta)} pasos | Visitados: {len(visitados)} celdas')
            print(f'[Laberinto/{self.algoritmo_seleccionado}] Ruta: {ruta}')
            print(f'[Laberinto/{self.algoritmo_seleccionado}] Costo total: {costo} | '
                  f'Visitados: {len(visitados)}')
        else:
            titulo = f'{self.algoritmo_seleccionado} — No se encontró camino'
            print(f'[Laberinto/{self.algoritmo_seleccionado}] No se encontró camino. '
                  f'Visitados: {len(visitados)}')

        self.animando = False
        self._actualizar_titulo(titulo)

    def _ejecutar_grafo(self):
        for nodo, circulo in self.nodos_parches.items():
            if nodo not in (self.inicio, self.fin):
                circulo.set_facecolor(COLOR_NODO)
        self.fig.canvas.draw_idle()

        fn = ALGORITMOS_GRAFO[self.algoritmo_seleccionado]
        if self.algoritmo_seleccionado == 'A*':
            visitados, ruta, costo = fn(self.adyacencia_grafo, self.coordenadas_grafo,
                                         self.inicio, self.fin)
        else:
            visitados, ruta, costo = fn(self.adyacencia_grafo, self.inicio, self.fin)

        self.animando = True

        for i, nodo in enumerate(visitados):
            if nodo in (self.inicio, self.fin):
                continue
            self.nodos_parches[nodo].set_facecolor(COLOR_VISITADO)
            self._actualizar_titulo(
                f'{self.algoritmo_seleccionado} — Explorando... ({i+1}/{len(visitados)})')
            plt.pause(self.velocidad * 3)

        if ruta:
            for nodo in ruta:
                if nodo not in (self.inicio, self.fin):
                    self.nodos_parches[nodo].set_facecolor(COLOR_RUTA)
                plt.pause(self.velocidad * 3)
            titulo = (f'{self.algoritmo_seleccionado} — Costo: {costo} | '
                      f'Ruta: {" → ".join(ruta)} | Visitados: {len(visitados)}')
            print(f'[Grafo/{self.algoritmo_seleccionado}] Ruta: {" → ".join(ruta)}')
            print(f'[Grafo/{self.algoritmo_seleccionado}] Costo total: {costo} | '
                  f'Visitados: {len(visitados)}')
        else:
            titulo = f'{self.algoritmo_seleccionado} — No se encontró camino'
            print(f'[Grafo/{self.algoritmo_seleccionado}] No se encontró camino. '
                  f'Visitados: {len(visitados)}')

        self.animando = False
        self._actualizar_titulo(titulo)

    def _reset(self):
        if self.animando:
            return
        self.inicio = None
        self.fin    = None
        self.estado = 'esperando_inicio'
        if self.modo == 'laberinto':
            self._dibujar_laberinto()
        else:
            self._dibujar_grafo()
        self._actualizar_titulo()
        self.fig.canvas.draw_idle()


def visualizar_laberinto(matriz, coordenadas_grafo=None, adyacencia_grafo=None):
    VisualizadorLaberinto(matriz, coordenadas_grafo, adyacencia_grafo)