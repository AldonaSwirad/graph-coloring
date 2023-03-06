import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

class Graph():
    def __init__(self, adjacency_list=None, type=None):
        ''' Tworzy graf wykorzystując podaną listę sąsiedztwa, tworzy wybrany graf sudoku w zależnosci od parametru type '''

        # Tworzy pusty graf
        if adjacency_list == None and type == None:
            self.adjacency_list = {}
            self.G = nx.Graph()
        
        # Tworzy graf dużego sudoku
        elif adjacency_list == None and type == 'sudoku9x9':
            self.adjacency_list = {}
            self.G = nx.sudoku_graph(3)
            #self.pos = dict(zip(list(self.G.nodes()), nx.grid_2d_graph(3 * 3, 3 * 3)))
            self.pos = nx.circular_layout(self.G)
            for node, nodes_dict in self.G.adjacency():
                self.adjacency_list[node] = list(nodes_dict.keys())

        # Tworzy graf małego sudoku
        elif adjacency_list == None and type == 'sudoku4x4':
            self.adjacency_list = {}
            self.G = nx.sudoku_graph(2)
            #self.pos = dict(zip(list(self.G.nodes()), nx.grid_2d_graph(2 * 2, 2 * 2)))
            self.pos = nx.circular_layout(self.G)
            for node, nodes_dict in self.G.adjacency():
                self.adjacency_list[node] = list(nodes_dict.keys())
                
        else:
            # Tworzy graf wykorzystując podaną listę sąsiedztwa
            self.G = nx.Graph()
            self.adjacency_list = adjacency_list

    def add_node(self, node):
        ''' Dodaje wierzchołek do listy sąsiedztwa '''

        if node not in self.adjacency_list.keys():
            self.adjacency_list[node] = []

    def add_edge(self, edge):
        ''' Dodaje krawędź do listy sąsiedztwa '''

        edge = set(edge)
        node1, node2 = tuple(edge)
        for x, y in [(node1, node2), (node2, node1)]:
            if x in self.adjacency_list:
                self.adjacency_list[x].append(y)
            else:
                self.adjacency_list[x] = [y]

    def get_adjacency_matrix(self):
        ''' Zwraca macierz sąsiedztwa jako numpy array '''

        return nx.to_numpy_array(self.G)

    def display_graph_streamlit(self):
        ''' Wyświetla graf w streamlicie '''

        nx.draw(self.G, self.pos, with_labels=True)
        st.pyplot(plt)

    def display_graph_notebook(self):
        ''' Wyświetla graf w notebooku, chyba bo nie testowałem'''
        
        nx.draw(self.G, self.pos, with_labels=True)
        plt.show()

    def display_all_nodes(self):
        ''' Wypisuje wszystkie wierzchołki '''

        print(self.adjacency_list.keys())

    def display_adjacency_list(self):
        '''Wypisuje listę sąsiedztwa '''

        for node in self.adjacency_list.keys():
            print(f'{node} : {self.adjacency_list[node]}')



