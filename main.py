from grafico import *
import json
import math
import copy


def dijkstra_metro(grafico, inic, fin):
    """

    :param grafico: El objeto grafo
    :type grafico: Graph
    :param inic: La estación de inicio
    :type inic: str
    :param fin: La estación final
    :type fin: str
    :return:
    :rtype:
    """
    global datos
    grafo1 = copy.deepcopy(grafico)

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

    return grafo1.dijkstra(inic, fin)


inf = float("inf")
datos = json.load(open("estaciones.json", encoding="utf-8"))
vertices = [i for i in datos["linea 1"]]
for i in range(2, 8):
    for j in datos[f"linea {i}"]:
        vertices.append(j)

dist = []
linea_actual = 1
combinacion = 5

for n, i in enumerate(vertices):
    for m, j in enumerate(vertices[n + 1:]):
        if i[0:-2] == j[0:-2]:
            dist.append(combinacion)
        elif i[-2:] == j[-2:] and i[-2] == "L":
            try:
                lin = int(i[-1])
            except ValueError:
                dist.append(inf)
                continue
            dist.append(datos["duracion"][lin-1]*(m+1))
        else:
            dist.append(inf)

grafo = Graph(vertices, dist)

condicion = True
while condicion:
    inicio = input("Ingrese la estación inicial: ")
    if inicio == "END":
        condicion = False
        continue
    fin = input("Ingrese la estación final: ")
    if fin == "END":
        condicion = False
        continue
    print(dijkstra_metro(grafo, inicio.title(), fin.title()))




