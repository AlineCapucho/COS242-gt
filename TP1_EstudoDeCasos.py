from TP1 import Graph, Vertice

""" Estudo de Casos Pergunta 1 """
mygraph = Graph()
mygraph.create_from_file('grafo_4.txt', kind='matrix')

c = 1
while True:
    c = 1

""" Estudo de Casos Pergunta 2 """
# mygraph = Graph()
# mygraph.create_from_file('grafo_1.txt', kind='list')

# Os tempos de execução das bfs foram calculados para diferentes vértices e armazenados em um txt
# A forma como fizemos isso está exemplificada no código a seguir. No caso de grafos com pelo
# menos 1000 vértices, não foi necessário calcular o mod do número do vértice que a bfs será
# realizada.
# with open('bfstimersgrafo1.txt', 'a') as f:
#     for i in range(1, 1000+1):
#         v = i % 100
#         if (v == 0):
#             v = 100
#         startTime = time.time()
#         mygraph.bfs(v)
#         executionTime = time.time() - startTime
#         print("Tempo de execução da bfs: {} segundos".format(str(executionTime)))
#         f.write('{} {}\n'.format(v, executionTime))

""" Gerando os gráficos """

# fig, ax = plt.subplots()

# df0 = pd.read_csv('bfstimersgrafo6.txt', sep=' ')

# df0['time'] = df0['time'] * 1000

# # ax.bar(df0['vertice'], df0['time'])
# ax.hist(df0['time'], bins=30)

# ax.set_title('Time required for the BFS in each vertice')
# ax.set_xlabel('Vertice')
# ax.set_ylabel('Time required (ms)')
# ax.tick_params(which='minor', width=0.75, length=2.5)
# # ax.set_xlim(0, 1000)
# # ax.set_yticks(np.arange(0, 7, 0.5))
# fig.set_size_inches([8, 6])

# plt.show()

### TAIL ###