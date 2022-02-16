from TP2_undirected import Graph, Vertice
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Snippet de cronometragem
# startTime = time.time()
# executionTime = time.time() - startTime
# print(executionTime)

# Perguntas sobre os grafos dados

""" Pergunta 1 """
# Para cada grafo foi executado o seguinte trecho de código, 
# mudando apenas o grafo que está sendo lido.
mygraph = Graph()
mygraph.create_from_file('EstudoDeCaso/grafo_W_1_1.txt', kind='list')
mygraph.dijkstra(1, 5)