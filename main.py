from grafico import *
import json
import math
import copy


def dijkstra_metro(grafico, inic, fin):
    """
    Una función para encontrar la ruta más corta entre dos estaciones de metro
    :param grafico: El objeto grafo
    :type grafico: Graph
    :param inic: La estación de inicio
    :type inic: str
    :param fin: La estación final
    :type fin: str
    :return:
    :rtype:
    """
    # PRUEBA
    # Importa el archivo con las estaciones
    global datos
    # Crea una copia del grafo para no alterar el original
    grafo1 = copy.deepcopy(grafico)

    # Inicializa las lineas de las estaciones de inicio y final
    for i in range(1, 8):
        if inic in datos[f"linea {i}"]:
            pos_ini = datos["pos ini"][i-1]
            try:
                pos_fin = datos["pos ini"][i]
            except IndexError:
                pos_fin = len(grafo1.V)

            anterior = ""
            for k in grafo1.V[pos_ini:pos_fin]:
                if anterior != "":
                    grafo1.distancia(k, anterior, datos["duracion"][i-1])
                anterior = k

        elif fin in datos[f"linea {i}"]:
            pos_ini = datos["pos ini"][i-1]
            try:
                pos_fin = datos["pos ini"][i]
            except IndexError:
                pos_fin = len(grafo1.V)

            anterior = ""
            for k in grafo1.V[pos_ini:pos_fin - 1]:
                if anterior != "":
                    grafo1.distancia(k, anterior, datos["duracion"][i - 1])
                anterior = k
    # Realiza la búsqueda de la ruta más corta
    return grafo1.dijkstra(inic, fin)

# Constantes
inf = float("inf")
# Importa el archivo con las estaciones
datos = json.load(open("estaciones.json", encoding="utf-8"))
# Crea los vértices con todas las estaciones
vertices = [i for i in datos["linea 1"]]
for i in range(2, 8):
    for j in datos[f"linea {i}"]:
        vertices.append(j)
# Crea una lista que contendrá las distancias
dist = []
# Una variable para el tiempo de combinación de estaciones
combinacion = 5
# Itera por las posibles combinaciones de estaciones
for n, i in enumerate(vertices):
    for m, j in enumerate(vertices[n + 1:]):
        # Si el nombre de ambas estaciones es iguales, les pone una distancia igual a combinación
        if i[0:-2] == j[0:-2]:
            dist.append(combinacion)
        # Si ambas estaciones son combinaciones y pertenecen a la misma línea
        elif i[-2:] == j[-2:] and i[-2] == "L":
            try:
                lin = int(i[-1])
            except ValueError:
                dist.append(inf)
                continue
            # Busca el tiempo asignado a la línea y lo multiplica por su distancia
            dist.append(datos["duracion"][lin-1]*(m+1))
        else:
            # Si no, les pone una distancia infinita
            dist.append(inf)

# Inicializa el grafo
# Sólo con las distancias de las combinaciones
grafo = Graph(vertices, dist)

# Establece un ciclo para que el usuario pueda ingresar las estaciones que quiere obtener la distancia más cercana
condicion = True
while condicion:
    # Pregunta las estaciones de inicio y final
    inicio = input("Ingrese la estación inicial: ")
    # PARA DEBUGGEAR
    if inicio == "gastar la bateria":
        print(grafo.h_cycle(grafo.V[:]))
        continue
    # Para salir del ciclo
    if inicio == "END":
        condicion = False
        continue
    # Intenta imprimir el grafo
    if inicio == "quiero morir":
        grafo.printgraph()
        continue
    fin = input("Ingrese la estación final: ")
    if fin == "END":
        condicion = False
        continue
    # Ejecuta la función dijkstra_metro
    print(dijkstra_metro(grafo, inicio.title(), fin.title()))




