from multiprocessing import Pool
import time
import itertools
import matplotlib.pyplot as plt
import networkx as nx


def chunks(l, n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x


def _betmap(G_normalized_weight_sources_tuple):
    """Pool for multiprocess only accepts functions with one argument.
    This function uses a tuple as its only argument. We use a named tuple for
    python 3 compatibility, and then unpack it when we send it to
    `betweenness_centrality_source`
    """
    return nx.betweenness_centrality_source(*G_normalized_weight_sources_tuple)


def betweenness_centrality_parallel(G, processes=None):
    """Parallel betweenness centrality  function"""
    p = Pool(processes=processes)
    node_divisor = len(p._pool) * 4
    node_chunks = list(chunks(G.nodes(), int(G.order() / node_divisor)))
    num_chunks = len(node_chunks)
    bt_sc = p.map(_betmap,
                  zip([G] * num_chunks,
                      [True] * num_chunks,
                      [None] * num_chunks,
                      node_chunks))

    # Reduce the partial solutions
    bt_c = bt_sc[0]
    for bt in bt_sc[1:]:
        for n in bt:
            bt_c[n] += bt[n]
    return bt_c


if __name__ == "__main__":
    G = nx.read_gpickle("github_users.p")

    bt = betweenness_centrality_parallel(G)
    print("\t\tBetweenness centrality for node 0: %.5f" % (bt[0]))
    # print('Finished Loading')
    # print(list(nx.betweenness_centrality(G).values()))
    # Plot the degree distribution of the GitHub collaboration network
    # plt.hist(list(nx.degree_centrality(G).values()))
    # plt.show()

    # Plot the degree distribution of the GitHub collaboration network
    # plt.hist(list(nx.betweenness_centrality(G).values()))
    # plt.show()