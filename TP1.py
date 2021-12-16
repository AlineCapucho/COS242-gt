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

    def create(self, v, e, kind='list'):
        # This function must create the graph
        if kind == 'list':
            self.kind = 'list'
            for i in range(1, v+1):
                self.graus.append(0)
                self.vertices.append(Vertice(i))
            
            for u, v in e:
                self.vertices[u-1].vizinhos.append(v)
                self.graus[u-1] += 1

                self.vertices[v-1].vizinhos.append(u)
                self.graus[v-1] += 1
        elif kind == 'matrix':
            self.kind = 'matrix'

            for i in range(v):
                self.graus.append(0)
                self.matrix.append(deque(0 for j in range(v)))

            for u, v in e:
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
                    self.graus.append(0)
                    self.vertices.append(Vertice(i))
                
                for line in f.readlines():
                    numbers = line.split()
                    u = int(numbers[0])
                    v = int(numbers[1])

                    self.vertices[u-1].vizinhos.append(v)
                    self.graus[u-1] += 1

                    self.vertices[v-1].vizinhos.append(u)
                    self.graus[u-1] += 1
            elif kind == 'matrix':
                self.kind = 'matrix'
                for i in range(ver):
                    self.graus.append(0)
                    self.matrix.append(deque(0 for j in range(ver)))
                
                for line in f.readlines():
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
            self.bfsNivel = []
            self.bfsQueue = deque()

            for i in range(len(self.vertices)):
                self.bfsMarks.append(0)
                self.bfsPai.append(0)
                self.bfsNivel.append(0)
            self.bfsMarks[b-1] = 1
            self.bfsQueue.append(b)

            while(self.bfsQueue):
                v = self.bfsQueue.pop()
                vizinhos = self.vertices[v-1].vizinhos

                for i in range (len(vizinhos)):
                    if self.bfsMarks[vizinhos[i]-1] == 0:
                        self.bfsMarks[vizinhos[i]-1] = 1
                        self.bfsQueue.append(vizinhos[i])
                        self.bfsPai[vizinhos[i]-1] = v
                        self.bfsNivel[vizinhos[i] - 1] = self.bfsNivel[self.bfsPai[vizinhos[i] - 1] - 1] + 1

            return [self.bfsPai, self.bfsNivel]

        elif self.kind == 'matrix':
            self.bfsMarks = []
            self.bfsPai = []
            self.bfsNivel = []
            self.bfsQueue = deque()

            for i in range(len(self.matrix[0])):
                self.bfsMarks.append(0)
                self.bfsPai.append(0)
                self.bfsNivel.append(0)
            self.bfsMarks[b-1] = 1
            self.bfsQueue.append(b)

            while(self.bfsQueue):
                v = self.bfsQueue.pop()
                for i in range(len(self.matrix[0])):
                    if self.matrix[v-1][i] == 1:
                        if self.bfsMarks[i] == 0:
                            self.bfsMarks[i] = 1
                            self.bfsQueue.append(i+1)
                            self.bfsPai[i] = v
                            self.bfsNivel[i] = self.bfsNivel[self.bfsPai[i] - 1] + 1
            
            return [self.bfsPai, self.bfsNivel]

        else:
            raise Exception('Invalid kind.')

    def dfs(self, b):
        if self.kind == 'list':
            self.dfsMarks = []
            self.dfsPai = []
            self.dfsNivel = []
            self.dfsStack = deque()

            for i in range(len(self.vertices)):
                self.dfsMarks.append(0)
                self.dfsPai.append(0)
                self.dfsNivel.append(0)
        
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
                            self.dfsNivel[vizinhos[i] - 1] = self.dfsNivel[self.dfsPai[vizinhos[i] - 1] - 1] + 1

            return [self.dfsPai, self.dfsNivel]

        elif self.kind == 'matrix':
            self.dfsMarks = []
            self.dfsPai = []
            self.dfsNivel = []
            self.dfsStack = deque()

            for i in range(len(self.matrix[0])):
                self.dfsMarks.append(0)
                self.dfsPai.append(0)
                self.dfsNivel.append(0)

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
                                self.dfsNivel[i] = self.dfsNivel[self.dfsPai[i] - 1] + 1

            return [self.dfsPai, self.dfsNivel]

        else:
            raise Exception('Invalid kind.')

    def distancia(self, v1, v2):
        bfsResult = self.bfs(v1)
        nivel = bfsResult[1]

        if (nivel[v2 - 1] == 0):
            return math.inf
        else:
            return nivel[v2 - 1]

    def diametro(self):
        bfsResult = self.bfs(1)
        nivel = bfsResult[1]
        bfsResult = self.bfs(nivel.index(max(nivel))+1)
        nivel = bfsResult[1]
        return max(nivel)

class Vertice:
    def __init__(self, id):
        self.id = id
        self.vizinhos = deque()
        self.nivel = 0

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

print(mygraph.bfs(1))

#### TAIL ####