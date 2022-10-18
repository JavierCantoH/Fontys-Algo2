# REFERENCES
# https://networkx.org/documentation/stable/auto_examples/graph/plot_erdos_renyi.html
# https://networkx.org/documentation/stable/reference/randomness.html
# https://pypi.org/project/PySimpleGUI/
# https://blog.finxter.com/sample-a-random-number-from-a-probability-distribution-in-python/
# https://stackoverflow.com/questions/62893202/fully-connect-an-unconnected-graph-in-networkx

from os import PRIO_PGRP
import time
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import networkx as nx
import random
from itertools import combinations, groupby

# TODO: find two disconnected subgraphs, select an arbitrary vertex in each of them and add an edge between those two vertices.
def connectSubgraphs(graph):
    components = dict(enumerate(nx.connected_components(graph)))
    components_combs = combinations(components.keys(), r=2)

    for _, node_edges in groupby(components_combs, key=lambda x: x[0]):
        node_edges = list(node_edges)
        random_comps = random.choice(node_edges)
        source = random.choice(list(components[random_comps[0]]))
        target = random.choice(list(components[random_comps[1]]))
        graph.add_edge(source, target)
    plt.figure(figsize=(12,6))
    nx.draw(graph, node_size=100, node_color='lightgreen')
    plt.show()

# TODO: use the probability for the number of edges
def generateGraph(numberOfNodes, probability, comesFromConnectSubgraphs):
    print(probability)
    n = int(numberOfNodes) # nodes
    e = ((int(probability) * (n-1)) / 100) * (n-1) # edges
    seed = 20160 # seed random number generators for reproducibility

    G = nx.gnm_random_graph(n, e, seed=seed) 
    if comesFromConnectSubgraphs:
        return G
    else:
        nx.draw(G, node_size= 100, node_color='lightblue')
        plt.show()


layout = [
        [sg.Text("Enter the number of nodes:")],    
        [sg.Input(key='-nodes-')],
        [sg.Text("Enter the probability (%) to generate the edges:")],    
        [sg.Input(key='-probability-')],
        [sg.Button("Generate Graph")],
        [sg.Button("Make it a connected graph")],
    ]

window = sg.Window("Algorithms Assignmet 1", layout)

while True:
    event, values = window.read(timeout=10)
    if event == sg.WIN_CLOSED:
        break

    elif event == "Generate Graph":
        window["Generate Graph"].update(disabled=True)
        numberOfNodes = values['-nodes-']
        probability = values['-probability-']
        generateGraph(numberOfNodes, probability, False)
        time.sleep(1)
        window["Generate Graph"].update(disabled=False)
    
    elif event == "Make it a connected graph":
        window["Make it a connected graph"].update(disabled=True)
        numberOfNodes = values['-nodes-']
        probability = values['-probability-']
        connectSubgraphs(generateGraph(numberOfNodes, probability, True))
        time.sleep(1)
        window["Make it a connected graph"].update(disabled=False)

window.close()