import streamlit as st
import cv2
from PIL import Image
import numpy as np
from SudokuBoard import SudokuBoard
from Graph import Graph

g = Graph() # inicjalizuje graf

uploaded_file = st.sidebar.file_uploader(label='Upload your sudoku', type=["jpg","jpeg","png"]) # odpowiada za przesyłanie planszy sudoku 
greedy_btn = st.button('Greedy coloring') # przycisk odpowiedzialny za wywołanie funkcji kolorującej graf algorytmem zachłannym
backtrack_btn = st.button('Backtracking coloring')

if uploaded_file is not None: # jeżeli plansza została załadowana
    image = Image.open(uploaded_file)
    image_array = np.asarray(image) 

    sudoku_board = SudokuBoard(3, image_array) # inicjalizuje instancję klasy SudokuBoard
    sudoku_board.process_board_image() # przetwarza obraz aby ułatwić OCR'ce działanie
    sudoku_board.split_board_image() # dzieli planszę na pojedyńcze komórki

    board = sudoku_board.create_board() # reprezentuje planszę jako macierz numpy 
    g.from_sudoku_board(board, 'grid') # tworzy graf na podstawie planszy

    st.sidebar.image(sudoku_board.processed_board_image, caption='Uploaded sudoku') # wyświetla zdjęcie planszy

    st.sidebar.write('Detected sudoku')
    st.sidebar.write(board) # wyświetla wynik OCR'ki

    if greedy_btn:
        g.standard_greedy_coloring()
        st.sidebar.write('Solved sudoku')
        st.sidebar.write(sudoku_board.map_solution_from_colors(g.node_colors))

    if backtrack_btn:
        g.backtracking_coloring(g.node_colors)
        st.sidebar.write('Solved sudoku')
        st.sidebar.write(sudoku_board.map_solution_from_colors(g.node_colors))
        
else: 
    g.from_adjacency_list({0:[1,2,4,5],1:[0,2], 2:[0,1,3],3:[2,4],4:[3,0],5:[0],6:[2],7:[1]}) # tworzy graf na podstawie listy sąsiedztwa, wstępnie wpisywana jest z palca 

    if greedy_btn:
        g.standard_greedy_coloring()

    if backtrack_btn:
        g.backtracking_coloring(g.node_colors)

g.display_graph_streamlit() # wyświetla graf







    
