import PySimpleGUI as sg
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class Graph(object):

    def __init__(self, size):
        self.adjMatrix = []
        for i in range(size):
            self.adjMatrix.append([0 for i in range(size)])
        self.size = size

    def add_edge(self, v1, v2):
        if v1 == v2:
            print("Same vertex %d and %d" % (v1, v2))
        self.adjMatrix[v1][v2] = 1
        self.adjMatrix[v2][v1] = 1
    
    def draw_graph(self):
        A = np.array(self.adjMatrix)
        G = nx.from_numpy_matrix(A)
        nx.draw(G, node_color='lightblue')
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
        numberOfNodes = values['-nodes-']
        probability = values['-probability-']
        g = Graph(int(numberOfNodes))
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(1, 2)
        g.add_edge(2, 0)
        g.add_edge(2, 3)
        g.draw_graph()
    
    # TODO:
    elif event == "Make it a connected graph":
       print("todo")

window.close()