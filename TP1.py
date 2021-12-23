# -*- coding: utf-8 -*-
from collections import deque
import random
import math
import copy
import time
# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#### Actual Code ####

class Graph:
    def __init__(self):
        # Initially, just initialize the deque and does nothing more
        self.vertices = []
        self.matrix = []
        self.kind = ''
        self.graus = []
        self.n = 0 # Number of vertices
        self.m = 0 # Number of edges

    def create(self, v, e, kind='list'):
        # This function must create the graph
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
        # This function must create a graph by reading a file
        with open(filename, 'r') as f:
            ver = int(f.readline())
            if kind == 'list':
                self.kind = 'list'
                for i in range(1, ver+1):
                    self.n += 1
                    self.graus.append(0)
                    self.vertices.append(Vertice(i))
                
                for line in f.readlines():
                    self.m += 1

                    numbers = line.split()
                    u = int(numbers[0])
                    v = int(numbers[1])

                    self.vertices[u-1].vizinhos.append(v)
                    self.graus[u-1] += 1

                    self.vertices[v-1].vizinhos.append(u)
                    self.graus[v-1] += 1
            elif kind == 'matrix':
                self.kind = 'matrix'
                for i in range(ver):
                    self.n += 1
                    self.graus.append(0)
                    self.matrix.append([0 for j in range(ver)])
                
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
                raise Exception('Invalid kind.')
    
    def __repr__(self):
        # Creates a print representation to visualize the contents
        if self.kind == 'list':
            vertices = 'number of vertices: {}'.format(str(len(self.vertices)))
            edges = ''

            for v in self.vertices:
                edges += "edges of vertice {}: ".format(str(v.id))
                edges += ''.join('{}, '.format(str(edge)) if edge != v.vizinhos[-1] else \
                    str(edge) for edge in v.vizinhos)
                edges += '\n'
            
            return vertices + '\n' + edges
        elif self.kind == 'matrix':
            vertices = 'number of vertices: {}'.format(str(len(self.matrix[0])))
            edges = ''

            for i, u in enumerate(self.matrix):
                edges += "edges of vertice {}: ".format(str(i+1))

                for j, v in enumerate(u):
                    if v:
                        edges += "{}, ".format(str(j+1))
                edges = edges.rstrip(', ')
                edges += "\n"

            return vertices + '\n' + edges
        else:
            raise Exception('This graph was not initialized')

    def bfs(self, b):
        # Makes a breadth-first search on the graph using b as the root
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

    def dfs(self, b):
        # Makes a depth-first search on the graph using b as the root
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

    def distancia(self, v1, v2):
        # Determines the distance between two vertices
        bfsResult = self.__bfsD__(v1)
        level = bfsResult

        if (level[v2 - 1] == 0):
            with open('distancia.txt', 'w') as f:
                f.write(str(float('inf')) + '\n')
        else:
            with open('distancia.txt', 'w') as f:
                f.write(str(level[v2 - 1]) + '\n')
        
    def diametro(self):
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

    def diametro2(self):
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

    def conexos(self):
        # Determines the connected components of a given graph
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

    def __bfsConexos__(self, b):
        #  Makes a breadth-first search on the graph using b as the root
        # returns a list with all the marked vertices in that search
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

    def __bfsD__(self, b):
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

class Vertice:
    def __init__(self, id):
        self.id = id
        self.vizinhos = deque()

#### Testing ####

""" Testing the create function """
# vertices = [1, 2, 3, 4, 5, 6, 7, 8]
# edges = [(1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (3, 8), (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)]

# mygraph = Graph()
# mygraph.create(8, edges, kind='list')
# # print(mygraph)

# mygraph.search(1)

""" Testing the create_from_file function """
# mygraph = Graph()
# mygraph.create_from_file('test.txt', kind='list')
# print(mygraph)

""" Testing the search function """
# mygraph.diametro()

""" Testing the diametro_txt function """
# mygraph = Graph()
# mygraph.create_from_file('grafo_6.txt', kind='list')
# mygraph.diametro()
# mygraph.diametro_txt('bfstimersgrafo6.txt')

""" Testing the info function """
# mygraph.info('info.txt')

""" Testing the connected graphs function """
# print(mygraph.conexos())

""" Estudo de Casos Pergunta 2 """
# mygraph = Graph()
# mygraph.create_from_file('grafo_1.txt', kind='list')

# Os tempos de execução das bfs foram calculados para diferentes vértices e armazenados em um txt
# A forma como fizemos isso está exemplificada no código a seguir. No caso de grafos com pelo
# menos 1000 vértices, não foi necessário calcular o mod do número do vértice que a bfs será
# realizada.
# with open('bfstimersgrafo1.txt', 'a') as f:
#     for i in range(1, 1000+1):
#         v = i % 100
#         if (v == 0):
#             v = 100
#         startTime = time.time()
#         mygraph.bfs(v)
#         executionTime = time.time() - startTime
#         print("Tempo de execução da bfs: {} segundos".format(str(executionTime)))
#         f.write('{} {}\n'.format(v, executionTime))

""" Gerando os gráficos """

# fig, ax = plt.subplots()

# df0 = pd.read_csv('bfstimersgrafo6.txt', sep=' ')

# df0['time'] = df0['time'] * 1000

# # ax.bar(df0['vertice'], df0['time'])
# ax.hist(df0['time'], bins=30)

# ax.set_title('Time required for the BFS in each vertice')
# ax.set_xlabel('Vertice')
# ax.set_ylabel('Time required (ms)')
# ax.tick_params(which='minor', width=0.75, length=2.5)
# # ax.set_xlim(0, 1000)
# # ax.set_yticks(np.arange(0, 7, 0.5))
# fig.set_size_inches([8, 6])

# plt.show()

#### TAIL ####