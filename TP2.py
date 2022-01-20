# -*- coding: utf-8 -*-
from collections import deque
import itertools as iter
import random
import math
import copy
import time
import numpy as np

#### Utilities ####

def get_line(filename, line):
    with open(filename, 'r') as f:
        line = next(iter.islice(f, line, line+1), None)
        return line

#### Actual Code ####

class Digraph:
    def __init__(self):
        # Initializes a graph
        # The fields vertices or matrix will be used depending on whether the user
        # chose between adjacency list or matrix
        self.vertices = np.array([])
        self.matrix = np.array([], dtype=np.int32)
        self.matrix_weights = np.array([], dtype=np.float32)
        self.kind = ''
        self.grausFromV = 0
        self.grausToV = 0
        self.n = 0
        self.m = 0
        self.weighted = 0
    
    def create_from_file(self, filename, kind='list'):
        # This function must create a graph by reading a file
        with open(filename, 'r') as f:
            # Gets the number of vertices, sets it in the object then initializes
            # the graus fields
            n = int(f.readline())
            self.n = n
            self.grausFromV = np.zeros(n)
            self.grausToV = np.zeros(n)
            if kind == 'list':
                # If the choice is adjacency list, then the field vertices will store
                # the vertices and the vertices will store the edges that come from
                # or go to them
                self.kind = 'list'
                for i in range(1, n+1):
                    self.vertices = np.append(self.vertices, Vertice(i))

                columns = get_line(filename, 2).split()
                if len(columns) < 3:
                    for line in f.readlines():
                        self.m += 1

                        numbers = line.split()
                        u = int(numbers[0])
                        v = int(numbers[1])

                        self.vertices[u-1].fromV = np.append(self.vertices[u-1].fromV, v)
                        self.grausFromV[u-1] += 1
                        self.grausToV[v-1] += 1
                
                else:
                    self.weighted = 1
                    for line in f.readlines():
                        self.m += 1

                        numbers = line.split()
                        u = int(numbers[0])
                        v = int(numbers[1])
                        w = float(numbers[2])

                        self.vertices[u-1].fromV = np.append(self.vertices[u-1].fromV, v)
                        self.vertices[u-1].weights = np.append(self.vertices[u-1].weights, w)
                        self.grausFromV[u-1] += 1
                        self.grausToV[v-1] += 1
            elif kind == 'matrix':
                # If the choice is adjacency matrix, then the field matrix will be initialize
                # and store the edges that come from or go to some vertice by setting the
                # value 1 to "vertice from" or the value 2 to "vertice to"
                self.kind = 'matrix'
                self.matrix = np.zeros((n, n))
                self.matrix_weights = np.zeros((n, n))

                columns = get_line(filename, 2).split()
                if len(columns) < 3:
                    for line in f.readlines():
                        self.m += 1

                        numbers = line.split()
                        u = int(numbers[0])
                        v = int(numbers[1])

                        self.matrix[u-1,v-1] = 1
                        self.grausFromV[u-1] += 1

                        self.matrix[v-1,u-1] = 2
                        self.grausToV[v-1] += 1
                else:
                    self.weighted = 1
                    for line in f.readlines():
                        self.m += 1

                        numbers = line.split()
                        u = int(numbers[0])
                        v = int(numbers[1])
                        w = float(numbers[2])

                        self.matrix[u-1,v-1] = 1
                        self.grausFromV[u-1] += 1
                        self.matrix_weights[u-1,v-1] = w

                        self.matrix[v-1,u-1] = 2
                        self.grausToV[v-1] += 1
            else:
                raise Exception('Invalid kind.')
    
    def __repr__(self):
        # Creates a print representation to visualize the contents
        if self.kind == 'list':
            vertices = f'number of vertices: {self.n}\n'
            edges = ''

            for v in self.vertices:
                edges += f'edges from vertice {v.id}: {v.fromV}\n'
            
            return vertices + edges
        elif self.kind == 'matrix':
            vertices = f'number of vertices: {self.n}\n'
            edges = ''

            for v in range(self.n):
                edges += f'edges from vertice {v+1}: ['
                for e in range(self.n):
                    if self.matrix[v,e] == 1:
                        edges += f'{e+1}. '
                edges += ']\n'
            
            return vertices + edges
        else:
            raise Exception('This graph was not initialized')

    def bfs(self, u):
        if self.kind=='list':
            marks = np.zeros(self.n)
            parents = np.full(self.n, -1)
            levels = np.full(self.n, -1)
            queue = deque()

            levels[u-1] = 0
            marks[u-1] = 1
            queue.append(u)
            while (queue != deque()):
                v = queue.popleft()
                for w in self.vertices[v-1].fromV:
                    if marks[w-1] != 1:
                        marks[w-1] = 1
                        queue.append(w)
                        parents[w-1] = v
                        levels[w-1] = levels[v-1]+1
            
            with open('bfs.txt', 'w') as f:
                f.write(f'Resultado da BFS feita no vértice {u}:\n')
                f.write(f'Vertice | Parent | Level\n')
                for v in self.vertices:
                    f.write(f'{v.id} | {parents[v.id-1]} | {levels[v.id-1]}\n')
        elif self.kind=='matrix':
            marks = np.zeros(self.n)
            parents = np.full(self.n, -1)
            levels = np.full(self.n, -1)
            queue = deque()

            levels[u-1] = 0
            marks[u-1] = 1
            queue.append(u)
            while (queue != deque()):
                v = queue.popleft()
                for w in range(1, self.n+1):
                    if self.matrix[v-1,w-1] == 1 and marks[w-1] != 1:
                        marks[w-1] = 1
                        queue.append(w)
                        parents[w-1] = v
                        levels[w-1] = levels[v-1]+1
            
            with open('bfs.txt', 'w') as f:
                f.write(f'Resultado da BFS feita no vértice {u}:\n')
                f.write(f'Vertice | Parent | Level\n')
                for v in range(1, self.n+1):
                    f.write(f'{v} | {parents[v-1]} | {levels[v-1]}\n')
        else:
            raise Exception('This graph was not initialized')

    def dfs(self, u):
        if self.kind=='list':
            marks = np.zeros(self.n)
            parents = np.full(self.n, -1)
            levels = np.full(self.n, -1)
            queue = deque()

            levels[u-1] = 0
            queue.append(u)
            while (queue != deque()):
                v = queue.pop()
                if marks[v-1] != 1:
                    marks[v-1] = 1
                    for w in reversed(self.vertices[v-1].fromV):
                        queue.append(w)
                        if marks[w-1] != 1:
                            parents[w-1] = v
                            levels[w-1] = levels[v-1]+1
            
            with open('dfs.txt', 'w') as f:
                f.write(f'Resultado da DFS feita no vértice {u}:\n')
                f.write(f'Vertice | Parent | Level\n')
                for v in self.vertices:
                    f.write(f'{v.id} | {parents[v.id-1]} | {levels[v.id-1]}\n')
        elif self.kind=='matrix':
            marks = np.zeros(self.n)
            parents = np.full(self.n, -1)
            levels = np.full(self.n, -1)
            queue = deque()

            levels[u-1] = 0
            queue.append(u)
            while (queue != deque()):
                v = queue.pop()
                if marks[v-1] != 1:
                    marks[v-1] = 1
                    for w in range(self.n, 0, -1):
                        if self.matrix[v-1, w-1] == 1:
                            queue.append(w)
                            if marks[w-1] != 1:
                                parents[w-1] = v
                                levels[w-1] = levels[v-1]+1
            
            with open('dfs.txt', 'w') as f:
                f.write(f'Resultado da DFS feita no vértice {u}:\n')
                f.write(f'Vertice | Parent | Level\n')
                for v in range(1, self.n+1):
                    f.write(f'{v} | {parents[v-1]} | {levels[v-1]}\n')
        else:
            raise Exception('This graph was not initialized')

class Vertice:
    def __init__(self, id):
        # Creates a vertice where id is the identifier, fromV contains the edges
        # that comes from this Vertice and weighs contains the weight of each
        # edges that comes from this Vertice
        self.id = id
        self.fromV = np.array([], dtype=np.int32)
        self.weights = np.array([], dtype=np.int32)

#### Testing ####

mygraph = Digraph()
mygraph.create_from_file('test.txt', kind='list')
mygraph.dfs(1)
print(mygraph)

#### TAIL ####