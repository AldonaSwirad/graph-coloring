import pyautogui as pg

def auto_solver(solution):
    for row, id in enumerate(solution):
        if id % 2 == 0:
            for cell in row:
                pg.press(f'{cell}')
                pg.press('right')
            
        elif id % 2 == 1:
            for cell in reversed(row):
                pg.press(f'{cell}')
                pg.press('left')

        pg.press('down')
