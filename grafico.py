import numpy
import copy


class Graph:
    """
    Un grafo, es decir una estructura de datos con vértices y aristas con un determinado peso

    :param V: Una lista con los vértices del grafo (es importante el orden)
    :type V: list
    :param VN: la cantidad de vértices
    :type VN: int
    :param graph: Una matriz con las conecciones del grafo y su peso, teoricamente debería ser simétrica
    :type graph: list
    """
    def __init__(self, vertices, distancias=None):
        if distancias is None:
            distancias = []
        self.V = vertices
        self.VN = len(vertices)
        self.graph = []
        for fila in range(self.VN):
            self.graph.append([])
            for columna in vertices:
                self.graph[fila].append("inf")
        for n, i in enumerate(self.V):
            self.graph[n][n] = 0

        if distancias:
            nodo1 = 0
            nodo2 = 1
            for individual in distancias:
                try:
                    self.distancia_d(nodo1, nodo2, individual)
                    nodo2 += 1
                except IndexError:
                    nodo1 += 1
                    nodo2 = nodo1 + 1
                    self.distancia_d(nodo1, nodo2, individual)
                    nodo2 += 1

    def distancia(self, nodo1, nodo2, dist):
        pos1 = self.V.index(nodo1)
        pos2 = self.V.index(nodo2)
        self.graph[pos1][pos2] = dist
        self.graph[pos2][pos1] = dist

    def distancia_d(self, nodo1, nodo2, dist):
        self.graph[nodo1][nodo2] = dist
        self.graph[nodo2][nodo1] = dist

    def printgraph(self):
        cad = "\t\t"
        for i in self.V:
            cad += i + "\t\t\t"
        print(cad)
        for i in range(self.VN):
            cadenita = self.V[i] + "\t\t"
            for j in self.graph[i]:
                cadenita += str(j) + "\t\t\t"
            print(cadenita)

    def dijkstra(self, inicio, fin=""):
        """
        Algoritmo para calcular la menor distancia entre 2 puntos

        :param inicio: el nodo inicial
        :type inicio: str
        :param fin: el nodo final, defaults to ""
        :type fin: str, optional
        :return: las distancias, los caminos más cortos
        :rtype: tuple
        """
        # Establecemos las distancias iniciales como infinito
        distancias = [float("inf") for i in self.V]
        # La distancia del punto con si mismo es 0
        distancias[self.V.index(inicio)] = 0
        # Crea una lista con los nodos que visitará
        nodos_por_visitar = copy.deepcopy(self.V)
        # Crea una lista para las rutas más óptimas
        camino = [[] for rutas in self.V]

        # Mientras queden nodos por visitar
        while len(nodos_por_visitar) != 0:
            # Este fragmento es para encontrar la menor distancia entre los nodos que no ha visitado
            dist_minima = float("inf")
            nodo_actual = ""
            for nodo in nodos_por_visitar:
                if dist_minima > distancias[self.V.index(nodo)]:
                    dist_minima = distancias[self.V.index(nodo)]
                    nodo_actual = nodo
            # Si no encontró ningún nodo con una distancia accesible, devuelve -1 y una lista vaía
            if dist_minima == float("inf"):
                return -1, []
            # Luego encuentra el índice del nodo en el que va a ejecutar el programa
            ind_nodo_actual = self.V.index(nodo_actual)
            # por cada uno de los nodos
            for n, nodo_prov in enumerate(self.V):
                # Guarda la distancia entre el nodo actual y el nodo que está comparando
                distancia_cache = self.graph[ind_nodo_actual][n]
                # Si los nodos están conectados y ambos están en nodos_por_visitar
                if distancia_cache not in [0, float("inf")] and nodo_prov in nodos_por_visitar:
                    # Si la distancia del nodo provisional es mayor a la suma de la distancia entre el nodo actual y
                    # el origen más la distancia del nodo provisional y el nodo actual, guarda la nueva distancia
                    if distancias[n] > distancias[ind_nodo_actual] + distancia_cache:
                        distancias[n] = distancias[ind_nodo_actual] + distancia_cache
                        camino[n] = copy.deepcopy(camino[ind_nodo_actual])
                        # Guarda el camino provisional más corto
                        camino[n].append(nodo_actual)
            # Si se estableció un nodo final, revisa si el nodo final es el nodo actual
            if fin != "" and nodo_actual == fin:
                # Guarda la destinación final y rompe el ciclo
                camino[self.V.index(fin)].append(fin)
                break
            # elimina el nodo actual de la lista de nodos por visitar
            nodos_por_visitar.pop(nodos_por_visitar.index(nodo_actual))
        # Si se estableció un nodo final, devuelve sólo la información de ese nodo
        if fin != "":
            return distancias[self.V.index(fin)], camino[self.V.index(fin)]
        # Se añaden a todos los caminos, la destinación final
        for n, nodo_prov in distancias:
            nodo_prov.append(self.V[n])

        return distancias, camino




