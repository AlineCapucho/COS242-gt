from TP2_undirected import Graph, Vertice
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Snippet de cronometragem
# startTime = time.time()
# executionTime = time.time() - startTime
# print(executionTime)

# Perguntas sobre os grafos dados

""" Pergunta 1 """
# Para cada grafo foi executado o seguinte trecho de código, 
# mudando apenas o grafo que está sendo lido.
# mygraph = Graph()
# mygraph.create_from_file('EstudoDeCaso/grafo_W_4_1.txt', kind='list')
# mygraph.dijkstra(1, 10)

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

# O trecho de código a seguir foi utilizado para calcular o
# tempo médio dos cálculos de distâncias e para construir
# alguns gráficos

# df0 = pd.read_csv('grafo_W_2_1_timers.txt', sep=' ')
# print(df0['time'].mean())

# fig, ax = plt.subplots(figsize=(6, 4))
# sns.set_style('whitegrid')
# ax = sns.histplot(x='time', data=df0)
# ax.set_xlabel('Time(s)')
# ax.set_title('Distribution of time taken')

# plt.show()

# fig.savefig('TimeGW21.png', dpi=300)

""" Pergunta 3 """
# Para cada grafo foi executado o seguinte trecho de código,
# mudando apenas o grafo que está sendo lido.
# mygraph = Graph()
# mygraph.create_from_file('EstudoDeCaso/grafo_W_1_1.txt', kind='list')
# mygraph.prim(1)

# Perguntas sobre a rede de colaboradores

""" Pergunta 1 """
# Tentamos utilizar o seguinte trecho de código para responder
# as perguntas sobre a rede de colaboradores, contudo, o código 
# não chegou a terminar a tempo.

# def pesquisadores_dict(filename):
#     with open(filename, 'r') as f:
#         d = {}
#         for line in f.readlines():
#             tmp = line.split(',')
#             tmp[1] = tmp[1].replace('\n', '')
#             d[tmp[1]] = int(tmp[0])
#         return d

# map_table = pesquisadores_dict('EstudoDeCaso/rede_colaboracao_vertices.txt')
# a = map_table['Edsger W. Dijkstra']
# b = map_table['Alan M. Turing']

# mygraph = Graph()
# mygraph.create_from_file('EstudoDeCaso/rede_colaboracao.txt', kind='list')
# mygraph.dijkstraAll(a)