import streamlit as st
import cv2
from PIL import Image
import numpy as np
from SudokuBoard import SudokuBoard
from Graph import Graph

g = Graph() # inicjalizuje graf

uploaded_file = st.sidebar.file_uploader(label='Upload your sudoku board', type=["jpg","jpeg","png"]) # odpowiada za przesyłanie planszy sudoku 
if uploaded_file is not None: # jeżeli plansza została załadowana
    image = Image.open(uploaded_file)
    image_array = np.asarray(image) 

    sudoku_board = SudokuBoard(2, image_array) # inicjalizuje instancję klasy SudokuBoard
    sudoku_board.process_board_image() # przetwarza obraz aby ułatwić OCR'ce działanie
    sudoku_board.split_board_image() # dzieli planszę na pojedyńcze komórki

    board = sudoku_board.create_board() # reprezentuje planszę jako macierz numpy 
    g.from_sudoku_board(board, 'grid') # tworzy graf na podstawie planszy

    st.sidebar.image(image, caption='Uploaded sudoku') # wyświetla zdjęcie planszy

    st.sidebar.write(board) # wyświetla wynik OCR'ki

else: 
    g.from_adjacency_list({0:[1,2,4],1:[0,2], 2:[0,1,3],3:[2,4],4:[3,0]}) # tworzy graf na podstawie listy sąsiedztwa, wstępnie wpisywana jest z palca 

g.display_graph_streamlit() # wyświetla graf

greedy_btn = st.button('Greedy coloring') # przycisk odpowiedzialny za wywołanie funkcji kolorującej graf algorytmem zachłannym

if greedy_btn:
    g.standard_greedy_coloring()

    
