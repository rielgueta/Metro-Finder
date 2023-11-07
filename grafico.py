import numpy
import copy
import time

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
        """
        Crea el gráfico con vertices "vertices" y distancias contenidas en distancias

        :param vertices: El nombre y orden de los vértices del grafo
        :type vertices: list
        :param distancias: Las distancias del grafo, debería tener VN!/(VN-i)!n!
        :type distancias: list
        """
        # Establece los parámetros básicos del grafo
        self.V = vertices
        self.VN = len(vertices)
        self.graph = []
        self.con = [[] for i in range(self.VN)]
        # Establece como distancia tentativa infinito para todos los nodos
        for fila in range(self.VN):
            self.graph.append([])
            for columna in vertices:
                self.graph[fila].append(float("inf"))
        # Establece que la distancia de un nodo con sí mismo es 0
        for n, i in enumerate(self.V):
            self.graph[n][n] = 0

        # Si se especificó el parámetro distancias, se agregan
        if distancias:
            contador = 0
            for n, nodo1 in enumerate(self.V):
                for m, nodo2 in enumerate(self.V[n + 1:]):
                    self.distancia_d(n, m+n+1, distancias[contador])
                    if distancias[contador] not in [0, float("inf")]:
                        temp = self.V.index(nodo2)
                        if n not in self.con[temp]:
                            self.con[temp].append(n)
                        if temp not in self.con[n]:
                            self.con[n].append(temp)

                    contador += 1

    def distancia(self, nodo1, nodo2, dist):
        """

        :param nodo1: El nombre del nodo 1 a conectar
        :type nodo1: str
        :param nodo2: El nombre del nodo 2 a conectar
        :type nodo2: str
        :param dist: La distancia a conectar
        :type dist: int
        """
        # Encuentra la posición de los nodos a conectar
        pos1 = self.V.index(nodo1)
        pos2 = self.V.index(nodo2)
        # Establece la posición
        self.distancia_d(pos1, pos2, dist)

    def distancia_d(self, nodo1, nodo2, dist):
        """
        Establece la distancia en base a la posición de los nodos
        :param nodo1:
        :type nodo1:
        :param nodo2:
        :type nodo2:
        :param dist:
        :type dist:
        """
        self.graph[nodo1][nodo2] = dist
        if nodo2 not in self.con[nodo1] and dist not in [0, float("inf")]:
            self.con[nodo1].append(nodo2)

        self.graph[nodo2][nodo1] = dist
        if nodo1 not in self.con[nodo2] and dist not in [0, float("inf")]:
            self.con[nodo2].append(nodo1)

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
        if inicio == "casa" or fin == "casa":
            return -1, ["pobre"]
        if inicio not in self.V or fin not in self.V:
            return -2, ["Error 2, no existe la estación ingresada"]
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

    def hamilton_greedy(self, inicio):
        in_inicial = self.V.index(inicio)
        camino = [in_inicial]
        costo = 0
        for i in range(self.VN-1):
            encontrado = False
            temp = self.graph[camino[-1]][:]
            while len(temp) > 0:
                min_value = min(temp)
                in_min = self.graph[camino[-1]].index(min_value)
                if in_min not in camino:
                    camino.append(in_min)
                    costo += min_value
                    encontrado = True
                    break
                else:
                    temp.remove(min_value)
            if not encontrado:
                raise Exception("It couldn't find a Hamiltonian cycle")
        if self.graph[in_inicial][camino[-1]] != float("inf"):
            costo += self.graph[in_inicial][camino[-1]]
        else:
            raise Exception("It couldn't find a Hamiltonian cycle")
        camino.append(in_inicial)
        return camino, costo

    def _h_cycle(self, vert):
        """
        Revisa si existe un ciclo hamiltoniano en el grafo por medio de recursividad.
        :param vert: Los vertices a revisar si están conectados
        :type vert: list
        :return: El ciclo hamiltoniano encontrado
        :rtype: list
        """
        # Condicion de salida
        if len(vert) == 1:
            # Si el último vértice está conectado con el primero, devuelve el camino, si no, devuelve una lista vacía
            if self.V.index(vert[0]) in self.con[0]:
                return [self.V.index(vert[0])]
            else:
                return []
        # Por cada vértice en vert
        for ind,verti in enumerate(vert):
            # Calcula si existe un ciclo hamiltoniano en el grafo sin el vértice actual
            camino_al_final = self._h_cycle(vert[0:ind]+vert[ind+1:])
            # Si existe un ciclo hamiltoniano en el grafo sin el vértice actual y el vértice actual está conectado con
            # el primer vértice del camino, devuelve el camino
            if camino_al_final and camino_al_final[0] in self.con[self.V.index(verti)]:
                camino_al_final.insert(0, self.V.index(verti))
                return camino_al_final
        # Si no existe un ciclo hamiltoniano en el grafo sin el vértice actual, devuelve una lista vacía
        return []

    def ciclo_hamiltoniano(self):
        """
        Revisa si existe un ciclo hamiltoniano en el grafo
        :return: El ciclo hamiltoniano encontrado
        :rtype: list
        """
        # Revisa si existe un ciclo hamiltoniano en el grafo
        camino = self._h_cycle(self.V[1:])
        if camino and self.V.index(self.V[0]) in self.con[camino[0]]:
            camino.insert(0, self.V.index(self.V[0]))
            camino.append(self.V.index(self.V[0]))
        else:
            return []
        return camino

    def euler_cycle(self):
        """
        Revisa si existe un ciclo euleriano en el grafo
        :return: El ciclo euleriano encontrado
        :rtype: list
        """
        # Revisa si existe un ciclo euleriano en el grafo
        for i in self.V:
            if len(self.con[self.V.index(i)]) % 2 != 0:
                return False
        return True