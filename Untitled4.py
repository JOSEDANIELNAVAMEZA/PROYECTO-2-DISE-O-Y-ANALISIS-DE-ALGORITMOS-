#!/usr/bin/env python
# coding: utf-8

# In[ ]:



#JOSÉ DANIEL NAVA MEZA
# Clase Arista

class Arista(object):
    """
    Clase Arista
    Generación y manejo de Aristas para su uso en Grafos
    Parametros
    ----------
    u : Nodo
        Nodo source de la Arista
    v : Nodo
        Nodo target de la Arista
    attrs : dict
        diccionario de atributos de la Arista
    Atributos
    ---------
    u : Nodo
        Nodo source de la Arista
    v : Nodo
        Nodo target de la Arista
    id : tuple
        (u.id, i.id). Tupla de ids de los Nodos de la Arista
    attrs : dict
        diccionario de atributos de la Arista
    """
    def __init__(self, u, v, attrs=None):
        self.u = u
        self.v = v
        self.id = (u.id, v.id)
        self.attrs = attrs

    def __eq__(self, other):
        """
        Comparación de igualdad entre Aristas
        Parametros
        ----------
        other : Arista
            Arista con la que se realiza la comparación
        Returns
        -------
        True o False : bool
            True si las Aristas son iguales, False de otro modo.
        """
        return self.u == other.u and self.v == other.v

    def __repr__(self):
        """
        Asigna representación repr a los Nodos
        Returns
        -------
        str
            representación en str de los Nodos
        """
        return repr(self.id)


# In[ ]:



# JOSÉ DANIEL NAVA MEZA
# Generador de grafos métodos de generacion


import sys
import random

from grafo import Grafo
from arista import Arista
from nodo import Nodo

def grafoMalla(m, n, dirigido=False):
    """
    Genera grafo de malla
    :param m: número de columnas (> 1)
    :param n: número de filas (> 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    if m < 2 or n < 2:
        print("Error. m y n, deben ser mayores que 1", file=sys.stderr)
        exit(-1)

    total_nodes = m*n
    last_col = m - 1
    last_row = n - 1
    g = Grafo(id=f"grafoMalla_{m}_{n}", dirigido=dirigido)
    nodos = g.V

    # agregar nodos
    for id in range(total_nodes):
        g.add_nodo(Nodo(id))

    # agregar aristas
    # primera fila
    g.add_arista(Arista(nodos[0], nodos[1]))
    g.add_arista(Arista(nodos[0], nodos[m]))
    for node in range(1, m - 1):
        g.add_arista(Arista(nodos[node], nodos[node - 1]))
        g.add_arista(Arista(nodos[node], nodos[node + 1]))
        g.add_arista(Arista(nodos[node], nodos[node + m]))
    g.add_arista(Arista(nodos[m-1], nodos[m-2]))
    g.add_arista(Arista(nodos[m-1], nodos[m - 1 + m]))

    # filas [1 : n - 2]
    for node in range(m, total_nodes - m):
        col = node % m
        g.add_arista(Arista(nodos[node], nodos[node - m]))
        g.add_arista(Arista(nodos[node], nodos[node + m]))
        if col == 0:
            g.add_arista(Arista(nodos[node], nodos[node + 1]))
        elif col == last_col:
            g.add_arista(Arista(nodos[node], nodos[node - 1]))
        else:
            g.add_arista(Arista(nodos[node], nodos[node + 1]))
            g.add_arista(Arista(nodos[node], nodos[node - 1]))

    # última fila (n - 1)
    col_0 = total_nodes - m
    col_1 = col_0 + 1
    last_node = total_nodes - 1
    g.add_arista(Arista(nodos[col_0], nodos[col_1]))
    g.add_arista(Arista(nodos[col_0], nodos[col_0 - m]))
    for node in range(col_1, last_node):
        g.add_arista(Arista(nodos[node], nodos[node - 1]))
        g.add_arista(Arista(nodos[node], nodos[node + 1]))
        g.add_arista(Arista(nodos[node], nodos[node - m]))
    g.add_arista(Arista(nodos[last_node], nodos[last_node - m]))
    g.add_arista(Arista(nodos[last_node], nodos[last_node - 1]))

    return g

def grafoErdosRenyi(n, m, dirigido=False, auto=False):
    """
    Genera grafo aleatorio con el modelo Erdos-Renyi
    :param n: número de nodos (> 0)
    :param m: número de aristas (>= n-1)
    :param dirigido: el grafo es dirigido?
    :param auto: permitir auto-ciclos?
    :return: grafo generado
    """
    if m < n-1 or n < 1:
        print("Error: n > 0 y m >= n - 1", file=sys.stderr)
        exit(-1)

    g = Grafo(id=f"grafoErdos_Renyi_{n}_{m}")
    nodos = g.V

    # crear nodos
    for nodo in range(n):
        g.add_nodo(Nodo(nodo))

    # crear aristas
    rand_node = random.randrange
    for arista in range(m):
        while True:
            u = rand_node(n)
            v = rand_node(n)
            if u == v and not auto:
                continue
            if g.add_arista(Arista(nodos[u], nodos[v])):
                break

    return g

def grafoGilbert(n, p, dirigido=False, auto=False):
    """
    Genera grafo aleatorio con el modelo Gilbert
    :param n: número de nodos (> 0)
    :param p: probabilidad de crear una arista (0, 1)
    :param dirigido: el grafo es dirigido?
    :param auto: permitir auto-ciclos?
    :return: grafo generado
    """
    if p > 1 or p < 0 or n < 1:
        print("Error: 0 <= p <= 1 y n > 0", file=sys.stderr)
        exit(-1)

    g = Grafo(id=f"grafoGilbert_{n}_{int(p * 100)}", dirigido=dirigido)
    nodos = g.V

    # crear nodos
    for nodo in range(n):
        g.add_nodo(Nodo(nodo))


    # crear pares de nodos, diferente generador dependiendo del parámetro auto
    if auto:
        pairs = ((u, v) for u in nodos.keys() for v in nodos.keys())
    else:
        pairs = ((u, v) for u in nodos.keys() for v in nodos.keys() if u != v)

    # crear aristas
    for u, v in pairs:
        add_prob = random.random()
        if add_prob <= p:
            g.add_arista(Arista(nodos[u], nodos[v]))

    return g

def grafoGeografico(n, r, dirigido=False, auto=False):
    """
    Genera grafo aleatorio con el modelo geográfico simple
    Se situan todos los nodos con coordenadas dentro de un rectangulo unitario
    Se crean aristas de un nodo a todos los que estén a una distancia <= r de
        un nodo en particular
    :param n: número de nodos (> 0)
    :param r: distancia máxima para crear un nodo (0, 1)
    :param dirigido: el grafo es dirigido?
    :param auto: permitir auto-ciclos?
    :return: grafo generado
    """
    if r > 1 or r < 0 or n < 1:
        print("Error: 0 <= r <= 1 y n > 0", file=sys.stderr)
        exit(-1)

    coords = dict()
    g = Grafo(id=f"grafoGeografico_{n}_{int(r * 100)}", dirigido=dirigido)
    nodos = g.V

    # crear nodos
    for nodo in range(n):
        g.add_nodo(Nodo(nodo))
        x = round(random.random(), 3)
        y = round(random.random(), 3)
        coords[nodo] = (x, y)

    # crear aristas
    r **= 2
    for u in nodos:
        vs = (v for v in nodos if u != v)
        # si auto es true, se agrega la arista del nodo u a sí mismo
        if auto:
            g.add_arista(Arista(nodos[u], nodos[u]))
        # se agregan todos los nodos dentro de la distancia r
        for v in vs:
            dist = (coords[u][0] - coords[v][0]) ** 2                     + (coords[u][1] - coords[v][1]) ** 2
            if dist <= r:
                g.add_arista(Arista(nodos[u], nodos[v]))

    return g

def grafoBarabasiAlbert(n, d, dirigido=False, auto=False):
    """
    Genera grafo aleatorio con el modelo Barabasi-Albert
    :param n: número de nodos (> 0)
    :param d: grado máximo esperado por cada nodo (> 1)
    :param dirigido: el grafo es dirigido?
    :param auto: permitir auto-ciclos?
    :return: grafo generado
    """
    if n < 1 or d < 2:
        print("Error: n > 0 y d > 1", file=sys.stderr)
        exit(-1)

    g = Grafo(id=f"grafoBarabasi_{n}_{d}", dirigido=dirigido)
    nodos = g.V
    nodos_deg = dict()

    # crear nodos
    for nodo in range(n):
        g.add_nodo(Nodo(nodo))
        nodos_deg[nodo] = 0

    # agregar aristas al azar, con cierta probabilidad
    for nodo in nodos:
        for v in nodos:
            if nodos_deg[nodo] == d:
                break
            if nodos_deg[v] == d:
                continue
            p = random.random()
            equal_nodes = v == nodo
            if equal_nodes and not auto:
                continue

            if p <= 1 - nodos_deg[v] / d                and g.add_arista(Arista(nodos[nodo], nodos[v])):
                nodos_deg[nodo] += 1
                if not equal_nodes:
                        nodos_deg[v] += 1

    return g

def grafoDorogovtsevMendes(n, dirigido=False):
    """
    Genera grafo aleatorio con el modelo Barabasi-Albert
    :param n: número de nodos (≥ 3)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    Crear 3 nodos y 3 aristas formando un triángulo. Después, para cada nodo
    adicional, se selecciona una arista al azar y se crean aristas entre el nodo
    nuevo y los extremos de la arista seleccionada.
    """
    if n < 3:
        print("Error: n >= 3", file=sys.stderr)
        exit(-1)

    g = Grafo(id=f"grafoDorogovtsev_{n}", dirigido=dirigido)
    nodos = g.V
    aristas = g.E

    # crear primeros tres nodos y sus correspondientes aristas
    for nodo in range(3):
        g.add_nodo(Nodo(nodo))
    pairs = ((u, v) for u in nodos for v in nodos if u != v)
    for u, v in pairs:
        g.add_arista(Arista(nodos[u], nodos[v]))

    # crear resto de nodos
    for nodo in range(3, n):
        g.add_nodo(Nodo(nodo))
        u, v = random.choice(list(aristas.keys()))
        g.add_arista(Arista(nodos[nodo], nodos[u]))
        g.add_arista(Arista(nodos[nodo], nodos[v]))

    return g


# In[ ]:



# JOSÉ DANIEL NAVA MEZA
# Clase Grafo 

import sys
from arista import Arista

class Grafo(object):
    """
    Clase Grafo.
    Generación y manejo de Grafos
    Parametros
    ----------
    id : str
        id o nombre del Grafo
    dirigido : bool
        True si el Grafo es dirigido, de otro modo, False
    Atributos
    ---------
    id : str
        id o nombre del Grafo
    dirigido : bool
        True si el Grafo es dirigido, de otro modo, False
    V : dict
        Diccionario de Nodos o Vertices del Grafo.
        key: Nodo.id
        value: Nodo
    E : dict
        Diccionario de Aristas (edges) del Grafo
        key: Arista.id
        value: Arista
    """
    def __init__(self, id='grafo', dirigido=False):
        self.id =       id
        self.dirigido = dirigido
        self.V =        dict()
        self.E =        dict()
        self.attr =     dict()

    def __repr__(self):
        """
        Asigna representación repr a los Grafos
        Returns
        -------
        str
            representación en str de los Grafos
        """
        return str("id: " + str(self.id) + '\n'
                   + 'nodos: ' + str(self.V.values()) + '\n'
                   + 'aristas: ' + str(self.E.values()))

    def add_nodo(self, nodo):
        """
        Agrega objeto nodo al grafo
        Parametros
        ----------
        nodo : Nodo
            objeto Nodo que se va a agregar a self.V
        Returns
        -------
        None
        """
        self.V[nodo.id] = nodo

    def add_arista(self, arista):
        """
        Agrega arista al grafo si esta no existe de antemano en dicho grafo.
        Parametros
        ----------
        arista : Arista
            objeto Arista que se va agregar a self.E
        Returns
        -------
        True o False : bool
            True si se agrego la arista, de otro modo, False
        """
        if self.get_arista(arista.id):
            return False

        self.E[arista.id] = arista
        return True

    def get_arista(self, arista_id):
        """
        Revisa si la arista ya existe en el grafo
        Parametros
        ----------
        arista_id : Arista.id
            atributo id de un objeto de la clase Arista
        Returns
        -------
        True o False : bool
            True si la arista existe, de otro modo, Falso
        """
        if self.dirigido:
            return arista_id in self.E
        else:
            u, v = arista_id
            return (u, v) in self.E or (v, u) in self.E

    def to_graphviz(self, filename):
        """
        Exporta grafo a formato graphvizDOT
        Parametros
        ----------
        filename : file
            Nombre de archivo en el que se va a escribir el grafo
        Returns
        -------
        None
        """
        edge_connector = "--"
        graph_directive = "graph"
        if self.dirigido:
            edge_connector = "->"
            graph_directive = "digraph"

        with open(filename, 'w') as f:
            f.write(f"{graph_directive} {self.id} " + " {\n")
            for nodo in self.V:
                f.write(f"{nodo};\n")
            for arista in self.E.values():
                f.write(f"{arista.u} {edge_connector} {arista.v};\n")
            f.write("}")

    def BFS(self, s):
        """
        Crea un nuevo grafo de tipo árbol mediante el algoritmo "breadth first
            search"
        Parametros
        ----------
        s : Nodo
            nodo raíz del árbol que se va a generar
        Returns
        -------
        bfs : Grafo
            árbol generado
        """
        if not s.id in self.V:
            print("Error, node not in V", file=sys.stderr)
            exit(-1)

        bfs = Grafo(id=f"BFS_{self.id}", dirigido=self.dirigido)
        discovered = set()
        bfs.add_nodo(s)
        L0 = [s]
        discovered = set()
        added = [s.id]

        while True:
            L1 = []
            for node in L0:
                aristas = [ids_arista for ids_arista in self.E
                            if node.id in ids_arista]

                for arista in aristas:
                    v = arista[1] if node.id == arista[0] else arista[0]

                    if v in discovered:
                        continue

                    bfs.add_nodo(self.V[v])
                    bfs.add_arista(self.E[arista])
                    discovered.add(v)
                    L1.append(self.V[v])

            L0 = L1
            if not L0:
                break

        return bfs

    def DFS_R(self, u):
        """
        Crea un nuevo grafo de tipo árbol mediante el algoritmo "depth first
            search".
        Usa una función recursiva
        Parametros
        ----------
        u : Nodo
            nodo raíz del árbol que se va a generar
        Returns
        -------
        dfs : Grafo
            árbol generado
        """
        dfs = Grafo(id=f"DFS_R_{self.id}", dirigido=self.dirigido)
        discovered = set()
        self.DFS_rec(u, dfs, discovered)

        return dfs

    def DFS_rec(self, u, dfs, discovered):
        """
        Función recursiva para agregar nodos y aristas al árbol DFS
        Parametros
        ----------
        u : Nodo
            nodo actual, en el que se continúa la búsqueda a lo profundo
        dfs : Grafo
            Grafo que contendrá al árbol de búsquedo a lo produndo.
        discovered : set
            nodos que ya han sido descubiertos
        Returns
        -------
        None
        """
        dfs.add_nodo(u)
        discovered.add(u.id)
        aristas = (arista for arista in self.E if u.id in arista)

        for arista in aristas:
            v = arista[1]
            if not self.dirigido:
                v = arista[0] if u.id == arista[1] else arista[1]
            if v in discovered:
                continue
            dfs.add_arista(self.E[arista])
            self.DFS_rec(self.V[v], dfs, discovered)

    def DFS_I(self, s):
        dfs = Grafo(id=f"DFS_I_{self.id}", dirigido=self.dirigido)
        discovered = {s.id}
        dfs.add_nodo(s)
        u = s.id
        frontera = []
        while True:
            # añadir a frontera todos los nodos con arista a u
            aristas = (arista for arista in self.E if u in arista)
            for arista in aristas:
                v = arista[1] if u == arista[0] else arista[0]
                if v not in discovered:
                    frontera.append((u, v))

            # si la frontera está vacía, salir del loop
            if not frontera:
                break

            # sacar nodo de la frontera
            parent, child = frontera.pop()
            if child not in discovered:
                dfs.add_nodo(self.V[child])
                arista = Arista(self.V[parent], self.V[child])
                dfs.add_arista(arista)
                discovered.add(child)

            u = child

        return dfs


# In[ ]:



# JOSÉ DANIEL NAVA MEZA 
# Clase Nodo

class Nodo(object):
    """
    Clase Nodo.
    Generación y manejo de Nodos para su uso en Grafos
    Parametros
    ----------
    id : str
        id o nombre del Nodo
    Atributos
    ----------
    id : int
        identificador del Nodo
    """
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        """
        Comparación de igualdad entre Nodos
        Parametros
        ----------
        other : Nodo
            Nodo con el que se realiza la comparación
        Returns
        -------
        True o False : bool
            True si los Nodos son iguales, False de otro modo.
        """
        return self.id == other.id

    def __repr__(self):
        """
        Asigna representación repr a los Nodos
        Returns
        -------
        str
            representación en str de los Nodos
        """
        return repr(self.id)

    def __hash__(self):
        return hash(self.id)


# In[ ]:



#JOSÉ DANIEL NAVA MEZA 
# Main. Generador de Grafos y árboles DFS y BFS. Proyecto SEGUNDA PARTE.BFS DFS


from time import perf_counter

from grafo import Grafo
from arista import Arista
from nodo import Nodo
from generador_grafos import grafoMalla,                              grafoErdosRenyi,                              grafoGilbert,                              grafoGeografico,                              grafoBarabasiAlbert,                              grafoDorogovtsevMendes


def main():
    path = "/home/daniel/garbage/grafos/500/"

    nodos = 500
    nodos_malla = (25, 20)

    m_erdos = 2000
    p_gilbert = 0.2
    r_geografico = 0.2
    d_barabasi = 7

    g = grafoMalla(*nodos_malla)
    g.to_graphviz(path + g.id + ".gv")
    bfs = g.BFS(Nodo(0))
    bfs.to_graphviz(path + bfs.id + ".gv")
    dfs = g.DFS_R(Nodo(0))
    dfs.to_graphviz(path + dfs.id + ".gv")
    dfs_i = g.DFS_I(Nodo(0))
    dfs_i.to_graphviz(path + dfs_i.id + ".gv")

    g = grafoErdosRenyi(nodos, m_erdos)
    g.to_graphviz(path + g.id + ".gv")
    bfs = g.BFS(Nodo(0))
    bfs.to_graphviz(path + bfs.id + ".gv")
    dfs = g.DFS_R(Nodo(0))
    dfs.to_graphviz(path + dfs.id + ".gv")
    dfs_i = g.DFS_I(Nodo(0))
    dfs_i.to_graphviz(path + dfs_i.id + ".gv")

    g = grafoGilbert(nodos, p_gilbert, dirigido=False, auto=False)
    g.to_graphviz(path + g.id + ".gv")
    bfs = g.BFS(Nodo(0))
    bfs.to_graphviz(path + bfs.id + ".gv")
    dfs = g.DFS_R(Nodo(0))
    dfs.to_graphviz(path + dfs.id + ".gv")
    dfs_i = g.DFS_I(Nodo(0))
    dfs_i.to_graphviz(path + dfs_i.id + ".gv")

    g = grafoGeografico(nodos, r_geografico)
    g.to_graphviz(path + g.id + ".gv")
    bfs = g.BFS(Nodo(0))
    bfs.to_graphviz(path + bfs.id + ".gv")
    dfs = g.DFS_R(Nodo(0))
    dfs.to_graphviz(path + dfs.id + ".gv")
    dfs_i = g.DFS_I(Nodo(0))
    dfs_i.to_graphviz(path + dfs_i.id + ".gv")

    g = grafoBarabasiAlbert(nodos, d_barabasi, auto=False)
    g.to_graphviz(path + g.id + ".gv")
    bfs = g.BFS(Nodo(0))
    bfs.to_graphviz(path + bfs.id + ".gv")
    dfs = g.DFS_R(Nodo(0))
    dfs.to_graphviz(path + dfs.id + ".gv")
    dfs_i = g.DFS_I(Nodo(0))
    dfs_i.to_graphviz(path + dfs_i.id + ".gv")

    g = grafoDorogovtsevMendes(nodos, dirigido=False)
    g.to_graphviz(path + g.id + ".gv")
    bfs = g.BFS(Nodo(0))
    bfs.to_graphviz(path + bfs.id + ".gv")
    dfs = g.DFS_R(Nodo(0))
    dfs.to_graphviz(path + dfs.id + ".gv")
    dfs_i = g.DFS_I(Nodo(0))
    dfs_i.to_graphviz(path + dfs_i.id + ".gv")

if __name__ == "__main__":
    main()

