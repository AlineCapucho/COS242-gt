from TP2_undirected import Graph, Vertice
import random
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
# mygraph = Graph()
# mygraph.create_from_file('EstudoDeCaso/grafo_W_1_1.txt', kind='list')
# mygraph.dijkstra(1, 5)

""" Pergunta 2 """
# Para cada grafo foi executado o seguinte trecho de código,
# mudando apenas o grafo que está sendo lido.
# mygraph = Graph()
# mygraph.create_from_file('EstudoDeCaso/grafo_W_3_1.txt', kind='list')
# print(mygraph.n)
# with open('grafo_W_3_1_timers.txt', 'a') as f:
#     chosen = []
#     for i in range(100):
#         choice = random.randint(1, mygraph.n)
#         if choice in chosen:
#             while (choice in chosen):
#                 choice = random.randint(1, mygraph.n)
#             chosen.append(choice)
#         else:
#             chosen.append(choice)
#         choice = chosen[-1]
#         print(choice)

#         executionTime = 0
#         if mygraph.weighted == 0:
#             print('BFS')
#             startTime = time.time()
#             mygraph.bfs(choice)
#             executionTime = time.time() - startTime
#         elif mygraph.weighted == 1 and mygraph.negative == 0:
#             print('Dijsktra')
#             startTime = time.time()
#             mygraph.dijkstraAll(choice)
#             executionTime = time.time() - startTime
#         print("Tempo de execução para encontrar as distancias: {} segundos".format(executionTime))
#         f.write('{} {}\n'.format(choice, executionTime))

""" Pergunta 3 """
mygraph = Graph()
mygraph.create_from_file('EstudoDeCaso/grafo_W_3_1.txt', kind='list')
mygraph.prim(1)