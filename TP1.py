from collections import deque

#### Actual Code ####

class Graph:
    def __init__(self):
        # Initially, just initialize the deque and does nothing more
        self.vertices = deque()
        self.matrix = deque()
        self.kind = ''

    def create(self, v, e, kind='list'):
        # This function must create the graph
        if kind == 'list':
            self.kind = 'list'
            for i in range(1, v+1):
                self.vertices.append(Vertice(i))
            
            for u, v in e:
                self.vertices[u-1].vizinhos.append(v)
                self.vertices[u-1].grau += 1

                self.vertices[v-1].vizinhos.append(u)
                self.vertices[v-1].grau += 1
        elif kind == 'matrix':
            self.kind = 'matrix'

            for i in range(v):
                self.matrix.append(deque(0 for j in range(v)))

            for u, v in e:
                print(u, v)
                print(self.matrix[u-1][v-1])
                self.matrix[u-1][v-1] = 1
                print(self.matrix[v-1][u-1])
                self.matrix[v-1][u-1] = 1
            
            for elem in self.matrix:
                print(elem)
        else:
            raise Exception('Unvalid kind.')
    
    def create_from_file(self, filename):
        # This function must create a graph by reading a file
        with open(filename, 'r') as f:
            ver = int(f.readline())
            for i in range(1, ver+1):
                self.vertices.append(Vertice(i))
            
            for line in f.readlines():
                edge = [int(v) for v in line if v not in [' ', '\n']]
                self.vertices[edge[0]-1].vizinhos.append(edge[1])
                self.vertices[edge[0]-1].grau += 1

                self.vertices[edge[1]-1].vizinhos.append(edge[0])
                self.vertices[edge[1]-1].grau += 1
    
    def __repr__(self):
        # Creates a print representation to visualize the contents
        if self.kind == 'list':
            vertices = 'number of vertices: {}'.format(str(len(self.vertices)))
            edges = ''

            for v in self.vertices:
                edges += "edges of vertice {} : ".format(str(v.id))
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

class Vertice:
    def __init__(self, id):
        self.id = id
        self.vizinhos = deque()
        self.grau = 0
        self.nivel = 0

#### Testing ####

""" Testing the create function """
vertices = [1, 2, 3, 4, 5]
edges = [(1, 2), (1, 3), (2, 5), (2, 4)]

mygraph = Graph()
mygraph.create(5, edges, kind='matrix')
print(mygraph)

""" Testing the create_from_file function """
# mygraph = Graph()
# mygraph.create_from_file('test.txt')
# print(mygraph)

#### TAIL ####