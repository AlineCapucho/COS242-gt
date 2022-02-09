# -*- coding: utf-8 -*-
from collections import deque
import itertools as iter
import numpy as np
import random
import math

#### Utilities ####

def get_line(filename, line):
    # Gets the line with index "line" from a file. Index start at 0
    with open(filename, 'r') as f:
        line = next(iter.islice(f, line, line+1), None)
        return line

#### Actual Code ####

class Graph:
    def __init__(self):
        """Initializes the deques and object variables"""
        self.vertices = []
        self.matrix = []
        self.matrix_weights =[]
        self.kind = ''
        self.graus = []
        self.n = 0 # Number of vertices
        self.m = 0 # Number of edges
        self.weighted = 0 # 0 if the graph does not have weights, 1 otherwise
        self.negative = 0 # 0 if the graph does not have negative weights, 1 otherwise

    def create(self, v, e, kind='list'):
        """Creates a weightless graph"""
        if kind == 'list':
            self.kind = 'list'
            for i in range(1, v+1):
                self.n += 1
                self.graus.append(0)
                self.vertices.append(Vertice(i))
            
            for u, v in e:
                self.m += 1

                self.vertices[u-1].vizinhos.append(v)
                self.graus[u-1] += 1

                self.vertices[v-1].vizinhos.append(u)
                self.graus[v-1] += 1
        elif kind == 'matrix':
            self.kind = 'matrix'

            for i in range(v):
                self.n += 1
                self.graus.append(0)
                self.matrix.append([0 for j in range(v)])

            for u, v in e:
                self.m += 1

                self.matrix[u-1][v-1] = 1
                self.graus[u-1] += 1

                self.matrix[v-1][u-1] = 1
                self.graus[v-1] += 1
        else:
            raise Exception('Invalid kind.')
    
    def create_from_file(self, filename, kind='list'):
        """Creates a graph by reading a file"""
        with open(filename, 'r') as f:
            # Gets the number of vertices, sets it in the object then initializes
            # the graus fields
            n = int(f.readline())
            self.n = n
            if kind == 'list':
                self.kind = 'list'
                for i in range(1, n+1):
                    self.n += 1
                    self.graus.append(0)
                    self.vertices.append(Vertice(i))

                # We check if the graph we are reading has weights by checking if it
                # has a third column
                columns = get_line(filename, 2).split()
                if len(columns) < 3:
                    for line in f.readlines():
                        self.m += 1

                        numbers = line.split()
                        u = int(numbers[0])
                        v = int(numbers[1])

                        self.vertices[u-1].vizinhos.append(v)
                        self.graus[u-1] += 1

                        self.vertices[v-1].vizinhos.append(u)
                        self.graus[v-1] += 1 
                else:
                    self.weighted = 1
                    for line in f.readlines():
                        self.m += 1

                        numbers = line.split()
                        u = int(numbers[0])
                        v = int(numbers[1])
                        w = float(numbers[2])
                        
                        self.vertices[u-1].vizinhos.append(v)
                        self.graus[u-1] += 1
                        self.vertices[u-1].weights.append(w)

                        self.vertices[v-1].vizinhos.append(u)
                        self.graus[v-1] += 1 
                        self.vertices[v-1].weights.append(w)

                        if w < 0:
                            self.negative = 1

            elif kind == 'matrix':
                # If the choice is adjacency matrix, then the field matrix will be initialize
                self.kind = 'matrix'

                for i in range(n):
                    self.n += 1
                    self.graus.append(0)
                    self.matrix.append([0 for j in range(n)])
                    self.matrix_weights.append([0 for j in range(n)])
                
                # We check if the graph we are reading has weights by checking if it
                # has a third column
                columns = get_line(filename, 2).split()
                if len(columns) < 3:
                    for line in f.readlines():
                        self.m += 1

                        numbers = line.split()
                        u = int(numbers[0])
                        v = int(numbers[1])

                        self.matrix[u-1][v-1] = 1
                        self.graus[u-1] += 1

                        self.matrix[v-1][u-1] = 1
                        self.graus[v-1] += 1
                else:
                    self.weighted = 1
                    for line in f.readlines():
                        self.m += 1

                        numbers = line.split()
                        u = int(numbers[0])
                        v = int(numbers[1])
                        w = float(numbers[2])

                        if w < 0:
                            self.negative = 1

                        self.matrix[u-1][v-1] = 1
                        self.graus[u-1] += 1
                        self.matrix_weights[u-1][v-1] = w
                        print(u, v, self.matrix_weights[u-1][v-1])

                        self.matrix[v-1][u-1] = 1
                        self.graus[v-1] += 1
                        self.matrix_weights[v-1][u-1] = w
                        print(v, u, self.matrix_weights[v-1][u-1])

            else:
                raise Exception('Invalid kind.')
    
    def __repr__(self):
        """Creates a print representation to visualize the contents"""
        if self.kind == 'list':
            vertices = 'number of vertices: {}'.format(str(len(self.vertices)))
            edges = ''
            weights = ''

            for v in self.vertices:
                edges += "edges of vertice {}: ".format(str(v.id))
                edges += ''.join('{}, '.format(str(edge)) if edge != v.vizinhos[-1] else \
                    str(edge) for edge in v.vizinhos)
                edges += '\n'
                weights += "weights of edges of vertice {}: ".format(str(v.id))
                weights += ''.join('{}, '.format(str(weight)) if weight != v.weights[-1] else \
                    str(weight) for weight in v.weights)
                weights += '\n'
            
            return vertices + '\n' + edges + '\n' + weights 
        elif self.kind == 'matrix':
            vertices = 'number of vertices: {}'.format(str(len(self.matrix[0])))
            edges = ''
            weights = ''

            for i in range(0, len(self.matrix), 1):
                edges += "edges of vertice {}: ".format(str(i+1))
                weights += "weights of edges of vertice {}: ".format(str(i+1))
                for j in range(0, len(self.matrix[i]), 1):
                    if self.matrix[i][j]:
                        edges += "{}, ".format(str(j+1))
                        weights += "{}, ".format(str(self.matrix_weights[i][j]))
                edges = edges.rstrip(', ')
                edges += "\n"
                weights = weights.rstrip(', ')
                weights += "\n"

            return vertices + '\n' + edges + '\n' + weights
        else:
            raise Exception('This graph was not initialized')

    def bfs(self, b):
        """Makes a breadth-first search on a weightless graph using b as the root.
        No return, creates a bfs.text file with the parent and level of each vertice"""
        if(self.weighted == 0):
            if self.kind == 'list':
                self.bfsMarks = []
                self.bfsPai = []
                self.bfsLevel = []
                self.bfsQueue = deque()

                for i in range(len(self.vertices)):
                    self.bfsMarks.append(0)
                    self.bfsPai.append(-1)
                    self.bfsLevel.append(-1)
                self.bfsMarks[b-1] = 1
                self.bfsLevel[b-1] = 0
                self.bfsQueue.append(b)

                while(self.bfsQueue):
                    v = self.bfsQueue.popleft()
                    vizinhos = self.vertices[v-1].vizinhos

                    for i in range (len(vizinhos)):
                        if self.bfsMarks[vizinhos[i]-1] == 0:
                            self.bfsMarks[vizinhos[i]-1] = 1
                            self.bfsQueue.append(vizinhos[i])
                            self.bfsPai[vizinhos[i]-1] = v
                            self.bfsLevel[vizinhos[i] - 1] = self.bfsLevel[self.bfsPai[vizinhos[i] - 1] - 1] + 1

                with open('bfs.txt', 'w') as f:
                    f.write("A seguir está uma representação de uma bfs realizada no vértice pedido."+
                    " Cada\nlinha é composta por três números, onde o primeiro número representa"+\
                        " um\nvértice, o segundo número quem é o pai desse vértice e o terceiro"+\
                        " número qual\no nível desse vértice. Um vértice que possui pai -1"+\
                        " significa um vértice raiz\nde uma árvore geradora. Um vértice que"+\
                        " possui nível -1 significa um vértice\ndesconexo do componente"+\
                        " conexo em que foi realizado a bfs.\n\n")
                    for i in range(len(self.vertices)):
                        f.write(str(i+1) + ' ' + str(self.bfsPai[i]) + ' ' + str(self.bfsLevel[i]) + '\n')

            elif self.kind == 'matrix':
                self.bfsMarks = []
                self.bfsPai = []
                self.bfsLevel = []
                self.bfsQueue = deque()

                for i in range(len(self.matrix[0])):
                    self.bfsMarks.append(0)
                    self.bfsPai.append(-1)
                    self.bfsLevel.append(-1)
                self.bfsMarks[b-1] = 1
                self.bfsLevel[b-1] = 0
                self.bfsQueue.append(b)

                while(self.bfsQueue):
                    v = self.bfsQueue.popleft()
                    for i in range(len(self.matrix[0])):
                        if self.matrix[v-1][i] == 1:
                            if self.bfsMarks[i] == 0:
                                self.bfsMarks[i] = 1
                                self.bfsQueue.append(i+1)
                                self.bfsPai[i] = v
                                self.bfsLevel[i] = self.bfsLevel[self.bfsPai[i] - 1] + 1
                
                with open('bfs.txt', 'w') as f:
                    f.write("A seguir está uma representação de uma bfs realizada no vértice pedido."+
                    " Cada\nlinha é composta por três números, onde o primeiro número representa"+\
                        " um\nvértice, o segundo número quem é o pai desse vértice e o terceiro"+\
                        " número qual\no nível desse vértice. Um vértice que possui pai -1"+\
                        " significa um vértice raiz\nde uma árvore geradora. Um vértice que"+\
                        " possui nível -1 significa um vértice\ndesconexo do componente"+\
                        " conexo em que foi realizado a bfs.\n\n")
                    for i in range(len(self.matrix[0])):
                        f.write(str(i+1) + ' ' + str(self.bfsPai[i]) + ' ' + str(self.bfsLevel[i]) + '\n')
        else:
            raise Exception('Invalid graph, must be weigthless.')

    def __bfsConexos__(self, b):
        """Makes a breadth-first search on a weightless graph using b as the root.
        Returns a list with all the marked vertices in that search"""
        if(self.weighted == 0):
            if self.kind == 'list':
                self.bfsMarks = []
                self.bfsQueue = deque()

                for i in range(len(self.vertices)):
                    self.bfsMarks.append(0)
                self.bfsMarks[b-1] = 1
                self.bfsQueue.append(b)

                while(self.bfsQueue):
                    v = self.bfsQueue.popleft()
                    vizinhos = self.vertices[v-1].vizinhos

                    for i in range (len(vizinhos)):
                        if self.bfsMarks[vizinhos[i]-1] == 0:
                            self.bfsMarks[vizinhos[i]-1] = 1
                            self.bfsQueue.append(vizinhos[i])

                return self.bfsMarks

            elif self.kind == 'matrix':
                self.bfsMarks = []
                self.bfsQueue = deque()

                for i in range(len(self.matrix[0])):
                    self.bfsMarks.append(0)
                self.bfsMarks[b-1] = 1
                self.bfsQueue.append(b)

                while(self.bfsQueue):
                    v = self.bfsQueue.popleft()
                    for i in range(len(self.matrix[0])):
                        if self.matrix[v-1][i] == 1:
                            if self.bfsMarks[i] == 0:
                                self.bfsMarks[i] = 1
                                self.bfsQueue.append(i+1)
                
                return self.bfsMarks
        else:
            raise Exception('Invalid graph, must be weigthless.')
    
    def __bfsD__(self, b):
        """Makes a breadth-first search on a weightless graph using b as the root.
        Returns a list with the levels of each verticle"""
        if(self.weighted == 0):
            if self.kind == 'list':
                self.bfsMarks = []
                self.bfsPai = []
                self.bfsLevel = []
                self.bfsQueue = deque()

                for i in range(len(self.vertices)):
                    self.bfsMarks.append(0)
                    self.bfsPai.append(-1)
                    self.bfsLevel.append(-1)
                self.bfsMarks[b-1] = 1
                self.bfsLevel[b-1] = 0
                self.bfsQueue.append(b)

                while(self.bfsQueue):
                    v = self.bfsQueue.popleft()
                    vizinhos = self.vertices[v-1].vizinhos

                    for i in range (len(vizinhos)):
                        if self.bfsMarks[vizinhos[i]-1] == 0:
                            self.bfsMarks[vizinhos[i]-1] = 1
                            self.bfsQueue.append(vizinhos[i])
                            self.bfsPai[vizinhos[i]-1] = v
                            self.bfsLevel[vizinhos[i] - 1] = self.bfsLevel[self.bfsPai[vizinhos[i] - 1] - 1] + 1

                return self.bfsLevel
            elif self.kind == 'matrix':
                self.bfsMarks = []
                self.bfsPai = []
                self.bfsLevel = []
                self.bfsQueue = deque()

                for i in range(len(self.matrix[0])):
                    self.bfsMarks.append(0)
                    self.bfsPai.append(-1)
                    self.bfsLevel.append(-1)
                self.bfsMarks[b-1] = 1
                self.bfsLevel[b-1] = 0
                self.bfsQueue.append(b)

                while(self.bfsQueue):
                    v = self.bfsQueue.popleft()
                    for i in range(len(self.matrix[0])):
                        if self.matrix[v-1][i] == 1:
                            if self.bfsMarks[i] == 0:
                                self.bfsMarks[i] = 1
                                self.bfsQueue.append(i+1)
                                self.bfsPai[i] = v
                                self.bfsLevel[i] = self.bfsLevel[self.bfsPai[i] - 1] + 1
                
                return self.bfsLevel
        else:
            raise Exception('Invalid graph, must be weigthless.')

    def dfs(self, b):
        """Makes a depth-first search on a weightless graph using b as the root.
        No return, creates a dfs.text file with the parent and level of each vertice"""
        if(self.weighted == 0):
            if self.kind == 'list':
                self.dfsMarks = []
                self.dfsPai = []
                self.dfsLevel = []
                self.dfsStack = deque()

                for i in range(len(self.vertices)):
                    self.dfsMarks.append(0)
                    self.dfsPai.append(-1)
                    self.dfsLevel.append(-1)
            
                self.dfsLevel[b-1] = 0
                self.dfsStack.appendleft(b)

                while(self.dfsStack):
                    v = self.dfsStack.popleft()
                    vizinhos = self.vertices[v-1].vizinhos
                    if(self.dfsMarks[v-1] == 0):
                        self.dfsMarks[v-1] = 1
                        for i in range (len(vizinhos)-1, -1, -1):
                            self.dfsStack.appendleft(vizinhos[i])
                            if(self.dfsMarks[vizinhos[i]-1] == 0):
                                self.dfsPai[vizinhos[i]-1] = v
                                self.dfsLevel[vizinhos[i] - 1] = self.dfsLevel[self.dfsPai[vizinhos[i] - 1] - 1] + 1
                
                with open('dfs.txt', 'w') as f:
                    f.write("A seguir está uma representação de uma dfs realizada no vértice pedido."+
                    " Cada\nlinha é composta por três números, onde o primeiro número representa"+\
                        " um\nvértice, o segundo número quem é o pai desse vértice e o terceiro"+\
                        " número qual\no nível desse vértice. Um vértice que possui pai -1"+\
                        " significa um vértice raiz\nde uma árvore geradora. Um vértice que"+\
                        " possui nível -1 significa um vértice\ndesconexo do componente"+\
                        " conexo em que foi realizado a dfs.\n\n")
                    for i in range(len(self.vertices)):
                        f.write(str(i+1) + ' ' + str(self.dfsPai[i]) + ' ' + str(self.dfsLevel[i]) + '\n')

            elif self.kind == 'matrix':
                self.dfsMarks = []
                self.dfsPai = []
                self.dfsLevel = []
                self.dfsStack = deque()

                for i in range(len(self.matrix[0])):
                    self.dfsMarks.append(0)
                    self.dfsPai.append(-1)
                    self.dfsLevel.append(-1)

                self.dfsLevel[b-1] = 0
                self.dfsStack.appendleft(b)

                while(self.dfsStack):
                    v = self.dfsStack.popleft()
                    if(self.dfsMarks[v-1] == 0):
                        self.dfsMarks[v-1] = 1
                        for i in range(len(self.matrix[0])-1, -1, -1):
                            if self.matrix[v-1][i] == 1:
                                self.dfsStack.appendleft(i+1)
                                if(self.dfsMarks[i] == 0):
                                    self.dfsPai[i] = v
                                    self.dfsLevel[i] = self.dfsLevel[self.dfsPai[i] - 1] + 1

                with open('dfs.txt', 'w') as f:
                    f.write("A seguir está uma representação de uma dfs realizada no vértice pedido."+
                    " Cada\nlinha é composta por três números, onde o primeiro número representa"+\
                        " um\nvértice, o segundo número quem é o pai desse vértice e o terceiro"+\
                        " número qual\no nível desse vértice. Um vértice que possui pai -1"+\
                        " significa um vértice raiz\nde uma árvore geradora. Um vértice que"+\
                        " possui nível -1 significa um vértice\ndesconexo do componente"+\
                        " conexo em que foi realizado a dfs.\n\n")
                    for i in range(len(self.matrix[0])):
                        f.write(str(i+1) + ' ' + str(self.dfsPai[i]) + ' ' + str(self.dfsLevel[i]) + '\n')
        else:
            raise Exception('Invalid graph, must be weigthless.')

    def dijkstra(self, v1, v2):
        """Runs dijkstra on positively-weighted graph from v1 to v2
        Returns the distance and minimum path between v1 and v2"""
        if self.weighted == 0:
            raise Exception('Dijkstra is not to be used in graphs without weights')
        if self.negative == 1:
            raise Exception('Dijkstra cannot be used in graphs with negative weights')
        if self.kind == 'list':
            print("dijkstra between two vertices")
        else:
            raise Exception('This graph was not initialized')

    def dijkstraAll(self, s):
        """Runs dijkstra on positively-weighted graph using s as the root.
        Returns the distance and minimum path between s and all other vertices"""
        if self.weighted == 0:
            raise Exception('Dijkstra is not to be used in graphs without weights')
        if self.negative == 1:
            raise Exception('Dijkstra cannot be used in graphs with negative weights')
        if self.kind == 'list':
            dist = np.full(len(self.vertices), np.inf, dtype=np.float32)
            V = np.arange(len(self.vertices), dtype=np.uint32)
            S = np.array([], dtype=np.uint32)
            dist[s-1] = 0

            parents = np.full(len(self.vertices), -1)
            levels = np.full(len(self.vertices), -1)
            levels[s-1] = 0
            
            while np.array_equal(V, np.sort(S)) != True:
                diff = np.setdiff1d(V, S, assume_unique=True)
                dist_min = dist[diff].min()
                if dist_min == np.inf:
                    break
                idx = np.where(dist==dist_min)
                u = np.intersect1d(idx[0], diff)[0]
                S = np.append(S, u)
                # para cada vizinho v de u
                for i in range(0, len(self.vertices[u].vizinhos), 1):
                    w = self.vertices[u].vizinhos[i]
                    print(u, w)
                    print(S)
                    if w not in S:
                        parents[w-1] = u+1
                        levels[w-1] = levels[u]+1
                    if dist[w-1] > dist[u] + self.vertices[u].weights[i]:
                        dist[w-1] = dist[u] + self.vertices[u].weights[i]
            
            with open('dijkstra.txt', 'w') as f:
                f.write('Resultado de Dijsktra feito no vértice {}:\n'.format(s))
                # f.write('Vertice | Parent | Level\n')
                # for v in self.vertices:
                #     f.write('{} | {} | {}\n'.format(v.id, parents[v.id-1], levels[v.id-1]))
                f.write('Vertice | Distance | Path\n')
                for v in self.vertices:
                    f.write('{} | {} | {}\n'.format(v.id, dist[v.id-1], path[v.id-1]))
        else:
            raise Exception('This graph was not initialized')

    def distancia(self, v1, v2):
        """"Determines the distance between vertices v1 and v2"""
        bfsResult = self.__bfsD__(v1)
        level = bfsResult

        if (level[v2 - 1] == 0):
            with open('distancia.txt', 'w') as f:
                f.write(str(float('inf')) + '\n')
        else:
            with open('distancia.txt', 'w') as f:
                f.write(str(level[v2 - 1]) + '\n')
        
    def diametro(self):
        if(self.weighted == 0):
            # Determines the diameter of a given graph by calculating the diameter in the
            # biggest connected component
            if (self.n > 1000):
                self.diametro2()
            else:
                conexos_list = self.conexos()
                conexos_dict = {i:conexos_list.count(i) for i in set(conexos_list)}

                connected = max(conexos_dict, key=conexos_dict.get)

                biggest_connected = [i+1 for i in range(len(conexos_list)) if conexos_list[i] == connected]

                bfsResults = [self.__bfsD__(i) for i in biggest_connected]
                maxlevels = [max(levels) for levels in bfsResults]

                with open('diametro.txt', 'w') as f:
                    f.write("O diâmetro máximo do grafo é {}".format(max(maxlevels)) + '\n')
        else:
            raise Exception('Invalid graph, must be weigthless.')
    
    def diametro2(self):
        if(self.weighted == 0):
            # Determines the diameter of a given graph by randomly selecting k = log_2 n
            # vertices, calculating the diameter in these vertices and choosing the biggest one

            k = math.floor(math.log2(self.n))
            choices = []
            for i in range(k):
                choice = random.randint(1, self.n)
                while (choice in choices):
                    choice = random.randint(1, self.n)
                choices.append(choice)

            bfsResults = [self.__bfsD__(i) for i in choices]
            maxlevels = [max(levels) for levels in bfsResults]
            print(maxlevels)

            with open('diametro.txt', 'w') as f:
                f.write("O diâmetro máximo do grafo é {}".format(max(maxlevels)) + '\n')
        else:
            raise Exception('Invalid graph, must be weigthless.')

    def conexos(self):
        """Determines the connected components of a weightless graph"""
        if(self.weighted == 0):
            if(self.kind == 'list'):
                aux = 1
                marked = []
                for i in range(len(self.vertices)):
                    marked.append(0)

                for i in range (len(marked)):
                    if marked[i] == 0:
                        bfsResults = self.__bfsConexos__(i+1)
                        for j in range (len(bfsResults)):
                            if bfsResults[j] == 1:
                                marked[j] = aux
                        aux += 1

                return marked

            elif(self.kind == 'matrix'):
                aux = 1
                marked = []
                for i in range(len(self.matrix[0])):
                    marked.append(0)

                for i in range (len(marked)):
                    if marked[i] == 0:
                        bfsResults = self.__bfsConexos__(i+1)
                        for j in range (len(bfsResults)):
                            if bfsResults[j] == 1:
                                marked[j] = aux
                        aux += 1

                return marked
        else:
            raise Exception('Invalid graph, must be weigthless.')

    def info(self, filename):
        # This functions write in a file named filename information about the graph
        if self.kind in ['list', 'matrix']:
            with open(filename, 'w') as f:
                info0 = "O grafo possui {} vertices e {} arestas.\n"\
                    .format(str(self.n), str(self.m))

                gmin = min(self.graus)
                gmean = int(sum(self.graus)/self.n) # Media aritmetica dos graus
                gmedian = sorted(self.graus)[int(self.n/2)] # Grau central em uma lista ordenada
                gmax = max(self.graus)

                info1 = "Com respeito aos graus dos vertices do grafo temos que:\nGrau minimo:" \
                    + " {}\nGrau maximo: {}\nGrau medio: {}\nMediana do grau: {}\n".format(\
                        str(gmin), str(gmax), str(gmean), str(gmedian))

                info2 = "A seguir estão os componentes conexos do grafo em questão:\n"

                conexos_list = self.conexos()
                conexos_dict = {}

                for i in range(len(conexos_list)):
                    key = str(conexos_list[i])
                    if (str(conexos_list[i]) in conexos_dict.keys()):
                        conexos_dict[key].append(i+1)
                    else:
                        conexos_dict[key] = [i+1]
                
                conexos_dict = sorted(conexos_dict.items(), key=lambda x: len(x[1]), reverse=True)

                print(conexos_dict)

                count = 0
                for key, values in conexos_dict:
                    info2 += "Componente {} possui {} vértices e é composto pelos vértices: "\
                        .format(str(count), str(len(values)))
                    
                    for v in values:
                        info2 += "{}, ".format(str(v))
                    info2 = info2.rstrip(', ')
                    info2 += "\n"

                    count += 1
                
                text = info0 + info1 + info2
                f.write(text)
        else:
            raise Exception('Invalid kind.')

    def prim(self, s):
        if self.weighted == 0:
            raise Exception('Prim is not to be used in graphs without weights')
        if self.negative == 1:
            raise Exception('Prim cannot be used in graphs with negative weights')
        if self.kind == 'list':
            cost = np.full(len(self.vertices), np.inf, dtype=np.float32)
            V = np.arange(len(self.vertices), dtype=np.uint32)
            S = np.array([], dtype=np.uint32)
            cost[s-1] = 0

            parents = np.full(len(self.vertices), -1)
            levels = np.full(len(self.vertices), -1)
            levels[s-1] = 0
            
            while np.array_equal(V, np.sort(S)) != True:
                diff = np.setdiff1d(V, S, assume_unique=True)
                cost_min = cost[diff].min()
                if cost_min == np.inf:
                    break
                idx = np.where(cost==cost_min)
                u = np.intersect1d(idx[0], diff)[0]
                S = np.append(S, u)
                for i in range(len(self.vertices[u].vizinhos)):
                    w = self.vertices[u].vizinhos[i]
                    if cost[w-1] > self.vertices[u].weights[i]:
                        cost[w-1] = self.vertices[u].weights[i]
                        parents[w-1] = u+1
                        levels[w-1] = levels[u]+1
            
            with open('prim.txt', 'w') as f:
                f.write('Árvore geradora mínima (MST) calculada com Prim\nfeito no vértice {} '.format(s))
                f.write('com peso total {}:\n'.format(cost.sum()))
                f.write('Vertice | Parent | Level\n')
                for v in self.vertices:
                    f.write('{} | {} | {}\n'.format(v.id, parents[v.id-1], levels[v.id-1]))
        else:
            raise Exception('This graph was not initialized')

class Vertice:
    def __init__(self, id):
        # Creates a vertice where id is the identifier, fromV contains the edges
        # that comes from this Vertice and weighs contains the weight of each
        # edges that comes from this Vertice
        self.id = id
        self.vizinhos = deque()
        self.weights = deque()

#### Testing ####

mygraph = Graph()
mygraph.create_from_file('test.txt', kind='list')

print(mygraph.prim(1))
#### TAIL ####
