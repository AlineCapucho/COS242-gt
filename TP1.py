from collections import deque

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
            raise Exception('Unvalid kind.')
    
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
                    u = int(line[0])
                    v = int(line[2])

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
                    u = int(line[0])
                    v = int(line[2])

                    self.matrix[u-1][v-1] = 1
                    self.graus[u-1] += 1

                    self.matrix[v-1][u-1] = 1
                    self.graus[v-1] += 1
            else:
                raise Exception('Unvalid kind.')
    
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

class Vertice:
    def __init__(self, id):
        self.id = id
        self.vizinhos = deque()
        self.nivel = 0

#### Testing ####

""" Testing the create function """
# vertices = [1, 2, 3, 4, 5]
# edges = [(1, 2), (1, 3), (2, 5), (2, 4)]

# mygraph = Graph()
# mygraph.create(5, edges, kind='list')
# print(mygraph)

""" Testing the create_from_file function """
mygraph = Graph()
mygraph.create_from_file('test.txt', kind='list')
print(mygraph)

#### TAIL ####