import PySimpleGUI as sg
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class Graph(object):

    def __init__(self, vertices):
        self.adjMatrix = []
        for i in range(vertices):
            self.adjMatrix.append([0 for i in range(vertices)])
        self.vertices = vertices

    def add_edge(self, v1, v2):
        if v1 == v2:
            print("Same vertex %d and %d" % (v1, v2))
        self.adjMatrix[v1][v2] = 1
        self.adjMatrix[v2][v1] = 1
    
    def draw_graph(self):
        A = np.array(self.adjMatrix)
        G = nx.from_numpy_matrix(A)
        print(np.matrix(A))
        nx.draw(G, node_color='lightblue')
        plt.show()

    # TODO: finish and change this func or find a better solution
    def printVertexCover(self):
        
        # Initialize all vertices as not visited.
        visited = [False] * (self.vertices)
        
        # Consider all edges one by one
        for u in range(self.vertices):
            
            # An edge is only picked when
            # both visited[u] and visited[v]
            # are false
            if not visited[u]:
                
                # Go through all adjacents of u and
                # pick the first not yet visited
                # vertex (We are basically picking
                # an edge (u, v) from remaining edges.
                for v in self.adjMatrix[u]:
                    if not visited[v]:
                        
                        # Add the vertices (u, v) to the
                        # result set. We make the vertex
                        # u and v visited so that all
                        # edges from/to them would
                        # be ignored
                        visited[v] = True
                        visited[u] = True
                        break

        # Print the vertex cover
        for j in range(self.vertices):
            if visited[j]:
                print(j, end = ' ')
                
        print()

# Function to perform DFS traversal on the graph on a graph
def DFS(graph, v, visited):
 
    # mark current node as visited
    visited[v] = True
 
    # do for every edge (v, u)
    for u in graph.adjMatrix[v]:
        # `u` is not visited
        if not visited[u]:
            DFS(graph, u, visited)
 
 
# Check if the graph is strongly connected or not
def isStronglyConnected(graph):
 
    # do for every vertex
    for i in range(graph.vertices):
 
        # to keep track of whether a vertex is visited or not
        visited = [False] * graph.vertices
 
        # start DFS from the first vertex
        DFS(graph, i, visited)
 
        # If DFS traversal doesn't visit all vertices,
        # then the graph is not strongly connected
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

while True:
    event, values = window.read(timeout=10)
    if event == sg.WIN_CLOSED:
        break

    elif event == "Generate Graph":
        numberOfNodes = values['-nodes-']
        probability = values['-probability-']
        g = Graph(int(numberOfNodes))
        # TODO: generate random edges with the probability
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(1, 2)
        g.add_edge(2, 0)
        g.add_edge(2, 3)
        g.draw_graph()
    
    elif event == "Make it a connected graph":
        numberOfNodes = values['-nodes-']
        probability = values['-probability-']
        vertices = int(numberOfNodes)
        g = Graph(vertices)
        # TODO: generate random edges with the probability
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(1, 2)
        g.add_edge(2, 0)
        g.add_edge(2, 3)
        # TODO: MAKE IT WORK
        print(isStronglyConnected(g))
        g.draw_graph()
    
    elif event == "Brute Vertex Cover":
        numberOfNodes = values['-nodes-']
        probability = values['-probability-']
        numberVertexCover = values['-vertexcover-']
        g = Graph(int(numberOfNodes))
        # TODO: generate random edges with the probability
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(0, 3)
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        g.add_edge(2, 3)
        g.printVertexCover()
        g.draw_graph()

window.close()