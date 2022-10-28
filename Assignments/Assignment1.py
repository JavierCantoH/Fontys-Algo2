import PySimpleGUI as sg
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

class Graph(object):
    def __init__(self, vertices):
        self.adjMatrix = []
        for i in range(vertices):
            self.adjMatrix.append([0 for i in range(vertices)])
        self.vertices = vertices

    def addSingleEdge(self, v1, v2):
        if v1 == v2:
            print("Same vertex %d and %d" % (v1, v2))
        else:
            self.adjMatrix[v1][v2] = 1
            self.adjMatrix[v2][v1] = 1
    
    def addEdges(self, probability):
        for node in range(self.vertices):
                if probability == 100:
                    for otherNode in range(self.vertices):
                        self.addSingleEdge(node, otherNode)
                elif getProbability(probability) == True:
                    randomNode = random.choice(range(self.vertices))
                    self.addSingleEdge(node, randomNode)
    
    def drawGraph(self):
        A = np.array(self.adjMatrix)
        G = nx.from_numpy_matrix(A)
        print(np.matrix(A))
        nx.draw(G, node_color='lightblue')
        plt.show()

    # TODO week 2: finish and change this func or find a better solution
    def printVertexCover(self):
        # Initialize all vertices as not visited.
        visited = [False] * (self.vertices)
        # Consider all edges one by one
        for u in range(self.vertices):
            # An edge is only picked when both visited[u] and visited[v] are false
            if not visited[u]:
                # Go through all adjacents of u and pick the first not yet visited vertex (We are basically picking an edge (u, v) from remaining edges.
                for v in self.adjMatrix[u]:
                    if not visited[v]:
                        # Add the vertices (u, v) to the result set. We make the vertex u and v visited so that all edges from/to them would be ignored
                        visited[v] = True
                        visited[u] = True
                        break
        # Print the vertex cover
        for j in range(self.vertices):
            if visited[j]:
                print(j, end = ' ')           
        print()

def getProbability(probability):
        p = float(probability / 100)
        return random.random() < p

# TODO week 1 DFS option 2
def DFS2(graph, start, visited):
    # Set current node as visited
    visited[start] = True
    # For every node of the graph
    for node in range(graph.vertices):
        # If some node is adjacent to the current node and it has not already been visited
        if (graph.adjMatrix[start][node] == 1 and (not visited[node])):
            DFS2(graph, node, visited)

# TODO week 1: fix DFS
def DFS(graph, start, visited):
    # mark current node as visited
    visited[start] = True
    # do for every edge (v, u)
    for node in graph.adjMatrix[start]:
        # `u` is not visited
        if not visited[node]:
            DFS(graph, node, visited)

# TODO week 1: FIX Check if the graph is connected or not
def isGraphConnected(graph):
    # do for every vertex
    for i in range(graph.vertices):
        # to keep track of whether a vertex is visited or not
        visited = [False] * graph.vertices
        # start DFS from the first vertex
        DFS(graph, i, visited)
        # If DFS traversal doesn't visit all vertices, then the graph is not strongly connected
        for b in visited:
            if not b:
                return False
    return True

layout = [
        [sg.Text("Enter the number of nodes:")],    
        [sg.Input(key='-nodes-')],
        [sg.Text("Enter the probability (%) to generate the edges:")],    
        [sg.Input(key='-probability-')],
        [sg.Button("Generate Graph")],
        [sg.Button("Make it a connected graph")],
        [sg.Text("Enter the size for vertex cover (should be less tha the number of vertices):")],    
        [sg.Input(key='-vertexcover-')],
        [sg.Button("Brute Vertex Cover")],
    ]

window = sg.Window("Algorithms Assignmet 1", layout)

numberOfNodes: int
probability: int
g: Graph

#TODO fix closing window PySimpleGUI
while True:
    event, values = window.read(timeout=10)
    if event == sg.WIN_CLOSED:
        break
    elif event == "Generate Graph":
        numberOfNodes = int(values['-nodes-'])
        probability = int(values['-probability-'])
        g = Graph(numberOfNodes)
        g.addEdges(probability)
        #g.drawGraph()
    elif event == "Make it a connected graph":
        #TODO
        print(isGraphConnected(g))
        #g.drawGraph()
    elif event == "Brute Vertex Cover":
        #TODO
        g.printVertexCover()
        #g.drawGraph()
window.close()