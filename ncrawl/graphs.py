from __future__ import unicode_literals
from copy import deepcopy
import networkx as nx
from ncrawl import models


class TopologyGraph(object):
    def __init__(self, **kwargs):
        try:
            self.query_set = models.Adjacency.objects.filter(**kwargs)
        except:
            raise
        self.graph = nx.MultiDiGraph()
        for adj in self.query_set:
            self.graph.add_node(adj.source.node.hostname, icon='router')
            self.graph.add_node(adj.target.node.hostname, icon='router')
            self.graph.add_edge(adj.source.node.hostname, adj.target.node.hostname,
                                source_interface=adj.source.name, target_interface=adj.target.name,
                                distance=30, bandwidth=10)
        # self.graph = self.digraph.to_undirected(reciprocal=True)
        # self.graph = nx.MultiGraph()
        # self.graph.add_nodes_from(self.digraph)
        # self.graph.add_edges_from((u, v, key, data)
        #                           for u, nbrs in self.digraph.adjacency_iter()
        #                           for v, keydict in nbrs.items()
        #                           for key, data in keydict.items())
        # self.graph.graph = self.digraph.graph
        # self.graph.node = self.digraph.node

    def layout(self):
        nodes, links = list(), list()
        # spring = nx.spring_layout(self.graph, scale=2000)
        for n in self.graph.nodes_iter():
            node = {'name': n}
            node.update(self.graph.node[n])
            # node.update({'x': spring[n][0], 'y': spring[n][1]})
            nodes.append(node)
        for e in self.graph.edges_iter(data=True):
            link = {'source': e[0], 'target': e[1]}
            link.update(e[2])
            links.append(link)
        return {'nodes': nodes, 'links': links}
