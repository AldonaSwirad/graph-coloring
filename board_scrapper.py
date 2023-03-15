import pyautogui as pg
from mss import mss
from time import sleep
import keyboard
import cv2 
import numpy as np

screenshoter = mss()
screenshot_roi = {'top': 205, 'left':363, 'width':497, 'height':497}
screen_number = 1

sleep(4)

while True:
    screenshot = screenshoter.grab(screenshot_roi)
    screenshot = np.array(screenshot)

    cv2.imwrite(rf'C:\Users\wilko\Desktop\Studia\Projekty studia\Optymalizacja dyskretna - Sudoku\Dane\Pierdoly\training_data\board_images\{screen_number}.png', screenshot)
    #pg.mouseInfo()
    pg.leftClick(465, 170)
    pg.leftClick(859, 702)
    sleep(0.5)
    
    screen_number += 1

    if keyboard.is_pressed('q'):
        break


