import numpy as np
import sys
import pickle as pkl
import networkx as nx
import scipy.sparse as sp


def parse_index_file(filename):
    index = []
    for line in open(filename):
        index.append(int(line.strip()))
    return index

def load_pubmed_data():
    # load the data: x, tx, allx, graph
    # 加载特征文件
    feature = np.genfromtxt("data/pubmed10/feature_div_length10.txt",dtype=np.dtype(float))
    features = sp.csr_matrix(feature, dtype=np.float32)
    #加载图文件
    with open("data/pubmed10/graph10.txt", 'r', encoding='utf-8') as f:
        graph = f.readlines()
        for k in range(0, len(graph)):
            graph[k] = graph[k].strip('\n').split(' ')
            graph[k] = tuple(int(m) for m in graph[k])

    G = nx.Graph()
    G.add_nodes_from([i for i in range(features.shape[0])])#先加入节点个数
    G.add_edges_from(graph)
    adj = sp.csr_matrix(nx.adjacency_matrix(G))  # 读取图，变成邻接矩阵，cs_matrix类型

    # ori_adj = copy.deepcopy(adj.todense())
    features = sp.vstack(features).tolil()

    return adj, features


def load_data(dataset):
    # load the data: x, tx, allx, graph
    names = ['x', 'tx', 'allx', 'graph']
    objects = []
    for i in range(len(names)):
        with open("data/ind.{}.{}".format(dataset, names[i]), 'rb') as f:
            if sys.version_info > (3, 0):
                objects.append(pkl.load(f, encoding='latin1'))
            else:
                objects.append(pkl.load(f))
    x, tx, allx, graph = tuple(objects)
    test_idx_reorder = parse_index_file("data/ind.{}.test.index".format(dataset))
    test_idx_range = np.sort(test_idx_reorder)

    if dataset == 'citeseer':
        # Fix citeseer dataset (there are some isolated nodes in the graph)
        # Find isolated nodes, add them as zero-vecs into the right position
        test_idx_range_full = range(min(test_idx_reorder), max(test_idx_reorder)+1)
        tx_extended = sp.lil_matrix((len(test_idx_range_full), x.shape[1]))
        tx_extended[test_idx_range-min(test_idx_range), :] = tx
        tx = tx_extended

    features = sp.vstack((allx, tx)).tolil()
    features[test_idx_reorder, :] = features[test_idx_range, :]
    adj = nx.adjacency_matrix(nx.from_dict_of_lists(graph))

    return adj, features
