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

    def floydWarshall(self, s):
        if self.weighted == 0:
            raise Exception('Floyd-Warshall is not to be used in graphs without weights')
        if self.negative == 0:
            raise Exception('Use Dijkstra in graphs without negative edges.')
        if self.kind == 'list':
            dist = np.full((len(self.vertices), len(self.vertices)), np.inf, dtype=np.float32)
            pred = np.full((len(self.vertices), len(self.vertices)), np.inf, dtype=np.float32)
            for i in range(self.n):
                dist[i][i] = 0

            for i in range(self.n):
                for j in range(self.vertices[i].fromV.size):
                    w = self.vertices[i].fromV[j]
                    dist[i][w-1] = self.vertices[i].weights[j]

            print(dist)

            for k in range(self.n):
                for i in range(self.n):
                    for j in range(self.n):
                        if dist[i][j] > dist[i][k] + dist[k][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]
            print(dist)

            for k in range(self.n):
                for i in range(self.n):
                    for j in range(self.n):
                        if dist[i][j] > dist[i][k] + dist[k][j]:
                            raiseExceptions("Graph has a negative-weight cycle, shortest paths are undefined.")

            # with open('floydWarshallDirected.txt', 'w') as f:
            #     f.write('Resultado de Floyd-Warshall feito no vértice {}:\n'.format(s))
            #     f.write('Vertice | Distance | Path\n')
            #     for v in self.vertices:
            #         f.write('{} | {} | {}\n'.format(v.id, dist[s-1][v.id-1], path[v.id-1]))
        else:
            raise Exception('This graph was not initialized')

    def prim(self, s):
        if self.weighted == 0:
            raise Exception('Prim is not to be used in graphs without weights')
        if self.negative == 1:
            raise Exception('Prim cannot be used in graphs with negative weights')
        if self.kind == 'list':
            cost = np.full(self.n, np.inf, dtype=np.float32)
            V = np.arange(self.n, dtype=np.uint32)
            S = np.array([], dtype=np.uint32)
            cost[s-1] = 0

            parents = np.full(self.n, -1)
            levels = np.full(self.n, -1)
            levels[s-1] = 0
            
            while np.array_equal(V, np.sort(S)) != True:
                diff = np.setdiff1d(V, S, assume_unique=True)
                cost_min = cost[diff].min()
                if cost_min == np.inf:
                    break
                idx = np.where(cost==cost_min)
                u = np.intersect1d(idx[0], diff)[0]
                S = np.append(S, u)
                for i in range(self.vertices[u].fromV.size):
                    w = self.vertices[u].fromV[i]
                    if w-1 not in S:
                        if cost[w-1] > self.vertices[u].weights[i]:
                            cost[w-1] = self.vertices[u].weights[i]
                            parents[w-1] = u+1
                            levels[w-1] = levels[u]+1
            
            with open('prim.txt', 'w') as f:
                for v in self.vertices:
                    f.write('{} | {}\n'.format(v.id, parents[v.id-1]))
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
mygraph.create_from_file('testidgraph.txt', kind='list')

mygraph.floydWarshall(1)

#### TAIL ####