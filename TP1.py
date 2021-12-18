from collections import deque
import math
import copy

#### Actual Code ####

class Graph:
    def __init__(self):
        # Initially, just initialize the deque and does nothing more
        self.vertices = deque()
        self.matrix = deque()
        self.kind = ''
        self.graus = deque()
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
                self.matrix.append(deque(0 for j in range(v)))

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
                    self.matrix.append(deque(0 for j in range(ver)))
                
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
                for i in range(len(self.matrix[0])):
                    f.write(str(i+1) + ' ' + str(self.bfsPai[i]) + ' ' + str(self.bfsLevel[i]) + '\n')

    def dfs(self, b):
        if self.kind == 'list':
            self.dfsMarks = []
            self.dfsPai = []
            self.dfsLevel = []
            self.dfsStack = deque()

            for i in range(len(self.vertices)):
                self.dfsMarks.append(0)
                self.dfsPai.append(0)
                self.dfsLevel.append(0)
        
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

            return [self.dfsPai, self.dfsLevel]

        elif self.kind == 'matrix':
            self.dfsMarks = []
            self.dfsPai = []
            self.dfsLevel = []
            self.dfsStack = deque()

            for i in range(len(self.matrix[0])):
                self.dfsMarks.append(0)
                self.dfsPai.append(0)
                self.dfsLevel.append(0)

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

            return [self.dfsPai, self.dfsLevel]

    def distancia(self, v1, v2):
        bfsResult = self.bfs(v1)
        level = bfsResult[1]

        if (level[v2 - 1] == 0):
            with open('distancia.txt', 'w') as f:
                f.write(str(float('inf')) + '\n')
        else:
            with open('distancia.txt', 'w') as f:
                f.write(str(level[v2 - 1]) + '\n')
        
    def diametro(self):
        bfsResult = self.bfs(1)
        level = bfsResult[1]
        bfsResult = self.bfs(level.index(max(level))+1)
        level = bfsResult[1]

        with open('diametro.txt', 'w') as f:
            f.write(str(max(level)) + '\n')

    def conexos(self):
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
        if self.kind == 'list':
            self.bfsMarks = []
            self.bfsQueue = deque()

            for i in range(len(self.vertices)):
                self.bfsMarks.append(0)
            self.bfsMarks[b-1] = 1
            self.bfsQueue.append(b)

            while(self.bfsQueue):
                v = self.bfsQueue.pop()
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
                v = self.bfsQueue.pop()
                for i in range(len(self.matrix[0])):
                    if self.matrix[v-1][i] == 1:
                        if self.bfsMarks[i] == 0:
                            self.bfsMarks[i] = 1
                            self.bfsQueue.append(i+1)
            
            return self.bfsMarks

    def info(self, filename):
        # This functions write in a file named filename information about the graph
        if self.kind in ['list', 'matrix']:
            with open(filename, 'w') as f:
                info0 = "O grafo possui {} vertices e {} arestas.\n"\
                    .format(str(self.n), str(self.m))
                print('graus: {}'.format(str(self.graus)))
                gmin = min(self.graus)
                gmean = int(sum(self.graus)/self.n) # Media aritmetica dos graus
                gmedian = sorted(self.graus)[int(self.n/2)] # Grau central em uma lista ordenada
                gmax = max(self.graus)

                info1 = "Com respeito aos graus dos vertices do grafo temos que:\nGrau minimo:" \
                    + " {}\nGrau maximo: {}\nGrau medio: {}\nMediana do grau: {}".format(\
                        str(gmin), str(gmax), str(gmean), str(gmedian))
                
                text = info0 + info1
                f.write(text)
        else:
            raise Exception('Invalid kind.')

class Vertice:
    def __init__(self, id):
        self.id = id
        self.vizinhos = deque()
        self.level = 0

#### Testing ####

""" Testing the create function """
# vertices = [1, 2, 3, 4, 5, 6, 7, 8]
# edges = [(1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (3, 8), (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)]

# mygraph = Graph()
# mygraph.create(8, edges, kind='list')
# # print(mygraph)

# mygraph.search(1)

""" Testing the create_from_file function """
mygraph = Graph()
mygraph.create_from_file('test2.txt', kind='matrix')
print(mygraph)

""" Testing the search function """
mygraph.bfs(1)

""" Testing the info function """
mygraph.info('info.txt')

""" Testing the connected graphs function """
print(mygraph.conexos())
#### TAIL ####