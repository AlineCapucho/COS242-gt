from TP1 import Graph, Vertice
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

""" Estudo de Casos Pergunta 1 """
# mygraph = Graph()
# mygraph.create_from_file('grafo_4.txt', kind='matrix')

# Esse while loop é para manter o código rodando enquanto eu verifico o consumo de memória
# c = 1
# while True:
#     c = 1

""" Estudo de Casos Pergunta 2 """
# mygraph = Graph()
# mygraph.create_from_file('grafo_5.txt', kind='list')

# Os tempos de execução das bfs foram calculados para diferentes vértices e armazenados em um txt
# A forma como fizemos isso está exemplificada no código a seguir. No caso de grafos com pelo
# menos 1000 vértices, não foi necessário calcular o mod do número do vértice que a bfs será
# realizada.
# with open('bfstimersgrafo5matrix.txt', 'a') as f:
#     for i in range(1, 1000+1):
#         # A linha abaixo é para quando o grafo tem pelo menos 1000 vértices
#         v = i
#         # As três linhas abaixo são para quando o grafo tem menos de 1000 vértices
#         # v = i % 100
#         # if (v == 0):
#         #     v = 100
#         startTime = time.time()
#         mygraph.bfs(v)
#         executionTime = time.time() - startTime
#         print("Tempo de execução da bfs: {} segundos".format(str(executionTime)))
#         f.write('{} {}\n'.format(v, executionTime))

""" Estudo de Casos Pergunta 3 """
# mygraph = Graph()
# mygraph.create_from_file('grafo_1.txt', kind='list')

# Os tempos de execução das dfs foram calculados para diferentes vértices e armazenados em um txt
# A forma como fizemos isso está exemplificada no código a seguir.
# No caso do grafo 2 que possui perto de 1000 vértice, fomos até onde possível e recomeçamos até
# completar 1000 bfs realizadas.
# with open('dfstimersgrafo1list.txt', 'a') as f:
#     for i in range(1, 1000+1):
#         # A linha abaixo é para quando o grafo tem pelo menos 1000 vértices
#         v = i
#         # As três linhas abaixo são para o grafo 1
#         v = i % 100
#         if (v == 0):
#             v = 100
#         startTime = time.time()
#         mygraph.dfs(v)
#         executionTime = time.time() - startTime
#         print("Tempo de execução da dfs: {} segundos".format(str(executionTime)))
#         f.write('{} {}\n'.format(v, executionTime))

""" Estudo de Casos Pergunta 4 """
# Para cada grafo foi utilizado este mesmo código, mudando apenas o grafo que está sendo lido.
# mygraph = Graph()
# mygraph.create_from_file('grafo_2.txt', kind='list')
# for v in [1, 2, 3]:
#     mygraph.dfs(v)
#     with open('dfs.txt', 'r') as f:
#         for i in range(7):
#             f.readline()
#         for u in [10, 20, 30]:
#             for i in range(10):
#                 line = f.readline().split(' ')
#             pai = line[1]
#             print(f"O pai do vértice {u} quando a bfs é realizada no vértice {v} é o "+\
#                 "vértice {pai}.")

""" Estudo de Casos Pergunta 5 """
# Para cada grafo foi utilizado este mesmo código, mudando apenas o grafo que está sendo lido.
# mygraph = Graph()
# mygraph.create_from_file('grafo_2.txt', kind='list')
# mygraph.distancia(10, 20)
# mygraph.distancia(10, 30)
# mygraph.distancia(20, 30)

""" Estudo de Casos Pergunta 6 """
# Para cada grafo foi utilizado este mesmo código, mudando apenas o grafo que está sendo lido.
# mygraph = Graph()
# mygraph.create_from_file('grafo_2.txt', kind='list')
# conexos_list = mygraph.conexos()
# conexos_dict = {i:conexos_list.count(i) for i in set(conexos_list)}
# biggest_connected = max(conexos_dict, key=conexos_dict.get)
# smallest_connected = min(conexos_dict, key=conexos_dict.get)
# length = len(set(conexos_list))
# print(f"O grafo possui {length} componentes conexas.")
# print(f"A maior componentes conexa possui {conexos_dict[biggest_connected]} vértices.")
# print(f"A menor componentes conexa possui {conexos_dict[smallest_connected]} vértices.")

""" Estudo de Casos Pergunta 7 """
# mygraph = Graph()
# mygraph.create_from_file("grafo_6.txt", kind='list')
# mygraph.diametro()

""" Calculando a média """
# O código a seguir pode ser facilmente modificado para calcular o tempo médio de uma busca
# para diferentes arquivos de tempo.
# df0 = pd.read_csv('dfstimersgrafo6list.txt', sep=' ')
# mean = df0['time'].mean()
# print(f"O tempo médio de uma DFS é {mean} segundos")

""" Gerando os gráficos """

# fig, ax = plt.subplots()

# df0 = pd.read_csv('bfstimersgrafo1.txt', sep=' ')
# print(df0)

# # Essa linha é usada quando deseja-se o tempo em milisegundos
# df0['time'] = df0['time'] * 1000

# ax.scatter(df0['vertice'], df0['time'], c=df0['vertice'], alpha=0.5)
# # ax.hist(df0['time'], bins=30)

# ax.set_title('Time required for the BFS in each vertice')
# ax.set_xlabel('Vertice')
# ax.set_ylabel('Time required (ms)') # Alterne entre s ou ms dependendo do que desejar
# ax.tick_params(which='minor', width=0.75, length=2.5)
# # ax.set_xlim(0, 1000)
# # ax.set_yticks(np.arange(0, 7, 0.5))
# fig.set_size_inches([8, 6])

# plt.show()

# fig.savefig('TimePerVertice G1L.png', dpi=300)

### TAIL ###