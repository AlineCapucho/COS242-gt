# -*- coding: utf-8 -*-
from collections import deque
import itertools as iter
from logging import raiseExceptions
import random
import math
import copy
import time
import numpy as np

#### Utilities ####

def get_line(filename, line):
    # Gets the line with index "line" from a file. Index start at 0
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
        self.kind = ''
        self.grausFromV = 0
        self.grausToV = 0
        self.n = 0
        self.m = 0
        self.weighted = 0 # 0 if the digraph does not have weights, 1 otherwise
        self.negative = 0 # 0 if the digraph does not have negative weights, 1 otherwise
    
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

                # We check if the digraph we are reading has weights by checking if it
                # has a third column
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
                        
                        if w < 0:
                            self.negative = 1

                        self.vertices[u-1].fromV = np.append(self.vertices[u-1].fromV, v)
                        self.vertices[u-1].weights = np.append(self.vertices[u-1].weights, w)
                        self.grausFromV[u-1] += 1
                        self.grausToV[v-1] += 1
            elif kind == 'matrix':
                # If the choice is adjacency matrix, then the field matrix will be initialize
                # and store the edges that come from or go to some vertice by setting the
                # value 1 to "edge from" or the value 2 to "edge to"
                self.kind = 'matrix'
                self.matrix = np.zeros((n, n))
                self.matrix_weights = np.zeros((n, n))

                # We check if the digraph we are reading has weights by checking if it
                # has a third column
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

                        if w < 0:
                            self.negative = 1

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
            vertices = 'number of vertices: {}\n'.format(self.n)
            edges = ''

            for v in self.vertices:
                edges += 'edges from vertice {}: {}\n'.format(v.id, v.fromV)
            
            return vertices + edges
        else:
            raise Exception('This graph was not initialized')

    def floydWarshall(self, s, d):
        if self.weighted == 0:
            raise Exception('Floyd-Warshall is not to be used in graphs without weights')
        if self.negative == 0:
            raise Exception('Use Dijkstra in graphs without negative edges.')
        if self.kind == 'list':
            dist = np.full((len(self.vertices), len(self.vertices)), np.inf, dtype=np.float128)
            for i in range(self.n):
                dist[i][i] = 0
           
            for i in range(self.n):
                for j in range(self.vertices[i].fromV.size):
                    w = self.vertices[i].fromV[j]
                    dist[i][w-1] = self.vertices[i].weights[j]

            for k in range(self.n):
                for i in range(self.n):
                    for j in range(self.n):
                        if dist[i][j] > dist[i][k] + dist[k][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]
                print(k)
                print(dist)

            for k in range(self.n):
                print(k)
                for i in range(self.n):
                    for j in range(self.n):
                        if dist[i][j] > dist[i][k] + dist[k][j]:
                            raiseExceptions("Graph has a negative-weight cycle, shortest paths are undefined.")

            with open('fdDirected.txt', 'w') as f:
                f.write('Resultado de Floyd-Warshall entre os vértice {} e {}:\n'.format(s, d))
                f.write('Distância: {}\n'.format(dist[s-1][d-1]))

        else:
            raise Exception('This graph was not initialized')

class Vertice:
    def __init__(self, id):
        # Creates a vertice where id is the identifier, fromV contains the edges
        # that comes from this Vertice and weighs contains the weight of each
        # edges that comes from this Vertice
        self.id = id
        self.fromV = np.array([], dtype=np.uint32)
        self.weights = np.array([], dtype=np.uint32)

#### Testing ####

mygraph = Digraph()
mygraph.create_from_file('estudos_tp2/grafo_W_4_0.txt', kind='list')

mygraph.floydWarshall(1,10)

#### TAIL ####