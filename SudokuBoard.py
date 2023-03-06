import cv2
import numpy as np
import pytesseract 

# ścieżka do pliku exe OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\wilko\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

class SudokuBoard():
    def __init__(self, image):
        self.board_image = image
        
        self.BOARD_WIDTH = 2 * image.shape[1]
        self.BOARD_HEIGHT = 2 * image.shape[0]
        self.cell_size = self.BOARD_HEIGHT // 9
        self.cell_images = []

    def process_board_image(self):

        resized_board_img = cv2.resize(self.board_image, (self.BOARD_WIDTH, self.BOARD_HEIGHT)) 
        gray_board_img = cv2.cvtColor(resized_board_img, cv2.COLOR_RGB2GRAY)
        _,binary_board_img = cv2.threshold(gray_board_img, 127,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        line_coord_x = self.BOARD_WIDTH // 3
        line_coord_y = self.BOARD_HEIGHT // 3

        cv2.line(binary_board_img, (0,line_coord_y), (self.BOARD_WIDTH, line_coord_y), (255,255,255), 20)
        cv2.line(binary_board_img, (0,line_coord_y*2),(self.BOARD_WIDTH, line_coord_y*2),(255,255,255), 20)

        cv2.line(binary_board_img, (line_coord_x,0), (line_coord_x, self.BOARD_HEIGHT), (255,255,255), 20)
        cv2.line(binary_board_img, (line_coord_x*2,0), (line_coord_x*2, self.BOARD_HEIGHT), (255,255,255), 20)

        self.processed_board_image = binary_board_img
    
    def split_board_image(self):

        y_start = 0
        y_end = self.BOARD_HEIGHT // 9

        x_start = 0
        x_end = self.BOARD_WIDTH // 9

        for i in range(1,10):
            for j in range(1,10):
                self.cell_images.append(self.processed_board_image[y_start : y_end, x_start : x_end])
                x_start += self.cell_size
                x_end += self.cell_size
            
            x_start = 0
            x_end = self.cell_size

            y_start += self.cell_size
            y_end += self.cell_size
    
    def create_board(self):
        board = []

        for image in self.cell_images:
            ocr_result = pytesseract.image_to_string(image, config='--psm 13 --oem 3 -c tessedit_char_whitelist=123456789')
            if ocr_result != '':
                board.append(int(ocr_result))
            else: 
                board.append(0)

        board = np.array(board)
        board = board.reshape((9,9))

        return board

        