from collections import deque

#### Actual Code ####

class Graph:
    def __init__(self):
        # Initially, just initialize the deque and does nothing more
        self.vertices = deque()

    def create(self, v, e):
        # This function must create the graph
        for i in range(1, v+1):
            self.vertices.append(Vertice(i))
        
        for u, v in e:
            self.vertices[u-1].vizinhos.append(v)
            self.vertices[u-1].grau += 1

            self.vertices[v-1].vizinhos.append(u)
            self.vertices[v-1].grau += 1
    
    def __repr__(self):
        # Creates a print representation to visualize the contents
        vertices = 'number of vertices: {}'.format(str(len(self.vertices)))
        edges = ''

        for v in self.vertices:
            edges += "edges of vertice {} : ".format(str(v.id))
            edges += ''.join('{}, '.format(str(edge)) if edge != v.vizinhos[-1] else \
                str(edge) for edge in v.vizinhos)
            edges += '\n'
        
        return vertices + '\n' + edges

class Vertice:
    def __init__(self, id):
        self.id = id
        self.vizinhos = deque()
        self.grau = 0
        self.nivel = 0

#### Testing ####

vertices = [1, 2, 3, 4, 5]
edges = [(1, 2), (1, 3), (2, 5), (2, 4)]

mygraph = Graph()
mygraph.create(5, edges)
print(mygraph)

#### TAIL ####