import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot

G = nx.DiGraph()
G.add_edges_from([(0,1), (0,2), (1,1), (1,2)])
write_dot(G,'graph.dot')